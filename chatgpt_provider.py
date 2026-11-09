"""Private stdio bridge to OpenAI's official local sign-in SDK."""
import atexit
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import uuid
import webbrowser
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SETTINGS = ROOT / 'ai_settings.json'

class StorageBusy(RuntimeError):
    pass

def settings():
    if not SETTINGS.exists(): return {'provider': 'lu', 'model': ''}
    try:
        value = json.loads(SETTINGS.read_text(encoding='utf-8'))
        if value.get('provider') not in ('lu','ollama','chatgpt') or not isinstance(value.get('model',''),str):
            raise ValueError()
        return value
    except (ValueError, OSError):
        raise RuntimeError('AI settings could not be read. Choose an AI provider in AI & account.')

def save_settings(provider, model=''):
    if provider not in ('lu','ollama','chatgpt') or (provider == 'chatgpt' and not model):
        raise ValueError('Choose an available model first.')
    temp = SETTINGS.with_suffix('.tmp')
    temp.write_text(json.dumps({'provider':provider,'model':model}),encoding='utf-8')
    os.replace(temp,SETTINGS)

class Bridge:
    def __init__(self):
        self.proc=None; self.lock=threading.Lock(); self.pending={}
    def start(self):
        if self.proc and self.proc.poll() is None: return
        bundled=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
        node=str(bundled) if bundled.exists() else shutil.which('node')
        if not node or not (ROOT/'vendor/sign-in-with-chatgpt-devkit/packages/local/dist/index.js').exists():
            raise RuntimeError('ChatGPT sign-in components are missing. See README.md setup instructions.')
        self.proc=subprocess.Popen([node,str(ROOT/'chatgpt_bridge.mjs')],cwd=ROOT,stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,encoding='utf-8',
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        threading.Thread(target=self.read,args=(self.proc,),daemon=True).start()
    def read(self, proc):
        try:
            for line in proc.stdout:
                data=json.loads(line)
                if data.get('event')=='browser':
                    url=data.get('url',''); parsed=urlparse(url)
                    if parsed.scheme=='https' and parsed.hostname=='auth.openai.com': webbrowser.open(url)
                    continue
                with self.lock: target=self.pending.get(data.get('id'))
                if target: target.put(data)
        except (ValueError, OSError): pass
        finally:
            with self.lock:
                for target in self.pending.values():
                    target.put({'error':{'message':'ChatGPT connection closed. Open AI & account and try again.'}})
    def call(self,method,params=None,timeout=240):
        ident=str(uuid.uuid4()); target=queue.Queue()
        with self.lock:
            self.start(); self.pending[ident]=target
            try:
                self.proc.stdin.write(json.dumps({'id':ident,'method':method,'params':params or {}})+'\n'); self.proc.stdin.flush()
            except (OSError, BrokenPipeError):
                self.pending.pop(ident,None)
                raise RuntimeError('ChatGPT connection closed. Please retry.')
        try:
            result=target.get(timeout=timeout)
            if 'error' in result:
                error = result['error']
                error_type = StorageBusy if error.get('code') == 'storage_busy' else RuntimeError
                raise error_type(error.get('message', 'ChatGPT request failed.'))
            return result['result']
        except queue.Empty: raise RuntimeError('ChatGPT timed out. Check the account connection and retry.')
        finally:
            with self.lock: self.pending.pop(ident,None)
    def close(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()

bridge=Bridge()
atexit.register(bridge.close)

def generate(body):
    config=settings()
    if not config.get('model'): raise RuntimeError('Select a ChatGPT model in AI & account.')
    params = {'model':config['model'],'messages':body['messages'],'schema':body['format']}
    try:
        result = bridge.call('generate', params)
    except StorageBusy:
        # The SDK timed out acquiring its credential lock before submitting the request.
        result = bridge.call('generate', params)
    return {'message':{'content':result['text']}}
