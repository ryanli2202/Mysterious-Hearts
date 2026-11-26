"""Non-blocking Windows MP3 effects and new-text notification tracking."""
import ctypes
import logging
import sys
import tempfile
import wave
from array import array
from pathlib import Path


class SoundSystem:
    def __init__(self):
        self.enabled = True
        self._aliases = {}
        self._state = None
        self._counts = {}
        self._mci = None
        self._typing = False
        self._voicemail = None
        self._voicemail_character = None
        self._campaign_voice = None
        self._campaign_volume = 70
        self._campaign_pcm = None
        self._campaign_cache = None
        self._arcade_wave = {}
        self._arcade_cache = None
        if sys.platform == 'win32':
            self._mci = ctypes.WinDLL('winmm').mciSendStringW
            self._mci.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
            self._mci.restype = ctypes.c_uint
            for effect in ('sent', 'received', 'typing', 'tone_chime', 'tone_soft'):
                filename = f'{effect}.wav' if effect.startswith('tone_') else 'typing.mp3' if effect == 'typing' else f'message {effect}.mp3'
                path = Path(__file__).resolve().parent / 'assets' / 'sounds' / filename
                alias = f'mh_{effect}_{id(self)}'
                # The multimedia driver supports per-alias volume for WAV as
                # well as MP3; waveaudio's driver rejects setaudio volume.
                media_type = 'mpegvideo'
                if path.is_file() and not self._mci(f'open "{path}" type {media_type} alias {alias}', None, 0, None):
                    self._aliases[effect] = alias
                else:
                    logging.warning('Could not load %s sound', effect)

    def play(self, effect):
        if effect in self._arcade_wave:
            import phone_personalization
            if self._arcade_wave[effect] != phone_personalization.preferences()['notification_volume']:
                self._mci(f'close {self._aliases.pop(effect)}', None, 0, None)
                del self._arcade_wave[effect]
        if self.enabled and effect.startswith('arcade_') and effect not in self._aliases and self._mci:
            allowed = {'tap', 'flip', 'card', 'drop', 'slide', 'merge', 'eat', 'rotate',
                       'clear', 'bounce', 'score', 'win', 'lose', 'match', 'reveal',
                       'invalid', 'brick', 'note0', 'note1', 'note2', 'note3'}
            if effect[7:] not in allowed:
                return
            path = Path(__file__).resolve().parent / 'assets' / 'sounds' / 'arcade' / f'{effect[7:]}.wav'
            alias = f'mh_{effect}_{id(self)}'
            if path.is_file() and not self._mci(f'open "{path}" type mpegvideo alias {alias}', None, 0, None):
                self._aliases[effect] = alias
            elif path.is_file():
                # Some Windows installations lack the MCI multimedia driver.
                # Waveaudio works there, but needs PCM scaling for per-effect volume.
                self._load_arcade_wave(effect, path, alias)
        alias = self._aliases.get(effect)
        if self.enabled and alias:
            if effect not in self._arcade_wave:
                self._volume(alias, 'typing_volume' if effect == 'typing' else 'notification_volume')
            # No "wait": playback returns immediately and never blocks the UI.
            self._mci(f'play {alias} from 0', None, 0, None)

    def _load_arcade_wave(self, effect, path, alias):
        import phone_personalization
        level = phone_personalization.preferences()['notification_volume']
        try:
            if self._arcade_cache is None:
                self._arcade_cache = tempfile.TemporaryDirectory(prefix='mh-arcade-', ignore_cleanup_errors=True)
            scaled = Path(self._arcade_cache.name) / path.name
            with wave.open(str(path), 'rb') as source:
                params = source.getparams()
                samples = array('h', source.readframes(source.getnframes()))
            for i, sample in enumerate(samples): samples[i] = int(sample * level / 100)
            with scaled.open('wb') as stream, wave.open(stream, 'wb') as target:
                target.setparams(params)
                target.writeframes(samples.tobytes())
            if not self._mci(f'open "{scaled}" type waveaudio alias {alias}', None, 0, None):
                self._aliases[effect] = alias
                self._arcade_wave[effect] = level
        except (OSError, wave.Error):
            logging.warning('Could not load %s sound', effect)

    def stop_arcade(self):
        for effect, alias in self._aliases.items():
            if effect.startswith('arcade_'):
                self._mci(f'stop {alias}', None, 0, None)

    def _volume(self, alias, key):
        import phone_personalization
        level = phone_personalization.preferences()[key] * 10
        self._mci(f'setaudio {alias} volume to {level}', None, 0, None)

    def toggle(self):
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_voicemail()
            self.stop_campaign_voice()
            for alias in self._aliases.values():
                self._mci(f'stop {alias}', None, 0, None)
        elif self._typing:
            self._play_typing()

    @staticmethod
    def voicemail_path(who):
        # Character IDs are filenames, never arbitrary paths.
        if not who or not all(c.isascii() and (c.isalnum() or c == '_') for c in who):
            return None
        path = Path(__file__).resolve().parent / 'assets' / 'sounds' / 'voicemails' / f'{who}.mp3'
        return path if path.is_file() else None

    def play_voicemail(self, who):
        path = self.voicemail_path(who)
        if not path:
            raise ValueError('No voicemail recording available yet.')
        if not self.enabled:
            raise ValueError('Turn sound on in phone Settings to listen to voicemail.')
        if self._mci is None:
            raise ValueError('Voicemail playback requires Windows audio.')
        self.stop_voicemail()
        alias = f'mh_voicemail_{id(self)}'
        if self._mci(f'open "{path}" type mpegvideo alias {alias}', None, 0, None):
            raise ValueError('Could not open this voicemail recording.')
        self._voicemail = alias
        self._voicemail_character = who
        self._volume(alias, 'voicemail_volume')
        if self._mci(f'play {alias} from 0', None, 0, None):
            self.stop_voicemail()
            raise ValueError('Could not play this voicemail recording.')

    def voicemail_playing(self, who=None):
        if who is not None and who != self._voicemail_character:
            return False
        if not self._voicemail:
            return False
        result = ctypes.create_unicode_buffer(32)
        error = self._mci(f'status {self._voicemail} mode', result, len(result), None)
        if not error and result.value == 'playing':
            return True
        self.stop_voicemail()
        return False

    def stop_voicemail(self):
        if self._voicemail:
            self._mci(f'close {self._voicemail}', None, 0, None)
            self._voicemail = None
            self._voicemail_character = None

    def _play_typing(self):
        alias = self._aliases.get('typing')
        if self.enabled and alias:
            self._volume(alias, 'typing_volume')
            self._mci(f'play {alias} from 0 repeat', None, 0, None)

    def play_campaign_voice(self, path, volume=70, pcm_path=None):
        """A separate non-blocking channel; never reuse music/SFX/voicemail."""
        self.stop_campaign_voice()
        if not self.enabled or not volume:return False
        if self._mci is None:raise ValueError('Voice playback is unavailable; captions remain available.')
        root=Path(__file__).resolve().parent/'assets/sounds/campaigns'
        path=Path(path).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError('Recording unavailable; captions remain available.')
        alias=f'mh_campaign_{id(self)}'
        error=self._mci(f'open "{path}" type mpegvideo alias {alias}',None,0,None)
        if error:
            if pcm_path is not None:
                pcm_path=Path(pcm_path).resolve()
                if pcm_path.is_relative_to(root.resolve()) and pcm_path.is_file():
                    return self._play_campaign_pcm(pcm_path,volume)
            raise ValueError('Could not open recording; captions remain available.')
        self._campaign_voice=alias
        self.set_campaign_volume(volume)
        if self._mci(f'play {alias} from 0',None,0,None):
            self.stop_campaign_voice()
            raise ValueError('Could not play recording; captions remain available.')
        return True

    def set_campaign_volume(self, volume):
        level=max(0,min(100,int(float(volume))))
        previous=self._campaign_volume
        self._campaign_volume=level
        if self._campaign_voice:
            if self._campaign_pcm is not None:
                if level==previous:return
                position=ctypes.create_unicode_buffer(32)
                self._mci(f'status {self._campaign_voice} position',position,len(position),None)
                playing=self.campaign_voice_playing()
                source=self._campaign_pcm
                if playing and source is not None:
                    try:start=int(position.value)
                    except ValueError:start=0
                    self.stop_campaign_voice();self._play_campaign_pcm(source,level,start)
            else:self._mci(f'setaudio {self._campaign_voice} volume to {level*10}',None,0,None)

    def _play_campaign_pcm(self, source, volume, start=0):
        """Waveaudio fallback with per-clip volume, never global device volume."""
        if self._campaign_cache is None:
            cache_root=Path(__file__).resolve().parent/'.sound-cache'
            cache_root.mkdir(exist_ok=True)
            self._campaign_cache=tempfile.TemporaryDirectory(prefix='campaign-',dir=cache_root,ignore_cleanup_errors=True)
        scaled=Path(self._campaign_cache.name)/'voice.wav'
        try:
            with wave.open(str(source),'rb') as stream:
                params=stream.getparams()
                if stream.getsampwidth()!=2:raise ValueError('Unsupported PCM recording.')
                samples=array('h',stream.readframes(stream.getnframes()))
            samples=array('h',(int(sample*volume/100) for sample in samples))
            with wave.open(str(scaled),'wb') as target:
                target.setparams(params);target.writeframes(samples.tobytes())
        except (OSError,wave.Error) as exc:raise ValueError('Could not prepare recording; captions remain available.') from exc
        alias=f'mh_campaign_{id(self)}'
        if self._mci(f'open "{scaled}" type waveaudio alias {alias}',None,0,None):
            raise ValueError('Could not open recording; captions remain available.')
        self._campaign_voice=alias;self._campaign_pcm=source;self._campaign_volume=volume
        self._mci(f'set {alias} time format milliseconds',None,0,None)
        if self._mci(f'play {alias} from {start}',None,0,None):
            self.stop_campaign_voice();raise ValueError('Could not play recording; captions remain available.')
        return True

    def campaign_voice_playing(self):
        if not self._campaign_voice:return False
        result=ctypes.create_unicode_buffer(32)
        error=self._mci(f'status {self._campaign_voice} mode',result,len(result),None)
        if not error and result.value=='playing':return True
        self.stop_campaign_voice();return False

    def stop_campaign_voice(self):
        if self._campaign_voice:
            self._mci(f'close {self._campaign_voice}',None,0,None)
            self._campaign_voice=None
            self._campaign_pcm=None

    def set_typing(self, active):
        """Loop for the current text generation, including across mute changes."""
        if active == self._typing:
            return
        self._typing = active
        if active:
            self._play_typing()
        elif alias := self._aliases.get('typing'):
            self._mci(f'stop {alias}', None, 0, None)

    def observe(self, state):
        """Notify once per incoming batch, never for old saves or spoken lines."""
        counts = {}
        for key, route in state.get('routes', {}).items():
            counts[('route', key)] = sum(
                m.get('role') == 'assistant' and m.get('channel') == 'text'
                for m in route.get('history', []))
        for key, group in state.get('groups', {}).items():
            if group.get('channel') == 'text':
                counts[('group', key)] = sum(
                    m.get('speaker') != 'Narrator' and not m.get('speaker', '').endswith(' (You)')
                    for m in group.get('history', []))
        changed = [key for key, count in counts.items() if count > self._counts.get(key, 0)]
        incoming = self._state is state and bool(changed)
        if self._state is not state:self.stop_campaign_voice()
        self._state, self._counts = state, counts
        if incoming:
            import phone_personalization
            tones = state.get('phone_personalization', {}).get('tones', {})
            audible = [tones.get(key, 'Default') if kind == 'route' else 'Default' for kind, key in changed]
            tone = next((tone for tone in audible if tone != 'Silent'), 'Silent')
            if tone == 'Default': self.play('received')
            elif tone != 'Silent' and self.enabled and phone_personalization.preferences()['notification_volume']:
                self.play('tone_'+tone.lower())

    def close(self):
        self.stop_voicemail()
        self.stop_campaign_voice()
        if self._campaign_cache is not None:
            cache_root=Path(__file__).resolve().parent/'.sound-cache'
            if Path(self._campaign_cache.name).resolve().is_relative_to(cache_root.resolve()):
                try:self._campaign_cache.cleanup()
                except OSError:logging.warning('Campaign audio cache could not be removed.')
            self._campaign_cache=None
        self._typing = False
        for alias in self._aliases.values():
            self._mci(f'close {alias}', None, 0, None)
        self._aliases.clear()
        self._arcade_wave.clear()
        if self._arcade_cache is not None:
            self._arcade_cache.cleanup()
            self._arcade_cache = None
