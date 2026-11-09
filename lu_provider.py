"""Connect to the model loaded by Locally Uncensored's LU Engine."""
import json
import os
import ctypes
from ctypes import wintypes
from pathlib import Path
import urllib.error
import urllib.request

ENDPOINT = os.environ.get('LU_ENGINE_URL', 'http://127.0.0.1:8129').rstrip('/')
MODEL_FILE = 'Qwen3.5-9B-abliterated.Q4_K_M.gguf'
ROOT = Path(__file__).resolve().parent
TOKEN_FILE = ROOT / '.lu-token'


def protect(value, mode):
    class Blob(ctypes.Structure):
        _fields_ = [('size', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_ubyte))]
    buffer = (ctypes.c_ubyte * len(value)).from_buffer_copy(value)
    source, output = Blob(len(value), buffer), Blob()
    crypt = ctypes.WinDLL('crypt32', use_last_error=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    function = crypt.CryptProtectData if mode == 'encrypt' else crypt.CryptUnprotectData
    function.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    function.restype = wintypes.BOOL
    if not function(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(output)):
        raise RuntimeError('Windows could not protect the LU API token. Please configure it again.')
    try:
        return ctypes.string_at(output.data, output.size)
    finally:
        kernel.LocalFree(output.data)


def save_token(token):
    if not token.strip():
        raise ValueError('Copy the Local API token from Locally Uncensored first.')
    encrypted = protect(token.strip().encode('utf-8'), 'encrypt')
    temp = TOKEN_FILE.with_suffix('.tmp')
    temp.write_bytes(encrypted)
    os.replace(temp, TOKEN_FILE)


def get_token():
    token = os.environ.get('LU_API_TOKEN', '').strip()
    if token:
        return token
    if TOKEN_FILE.exists():
        return protect(TOKEN_FILE.read_bytes(), 'decrypt').decode('utf-8')
    raise RuntimeError('Set up the Local API in Locally Uncensored, then paste its token using AI & account > Set LU API token.')


def request(path, body=None, timeout=300):
    req = urllib.request.Request(ENDPOINT + path,
        data=None if body is None else json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + get_token()})
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(req, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise RuntimeError('LU rejected the API token. Copy its current Local API token into AI & account > Set LU API token.') from exc
        raise RuntimeError(f'LU Engine returned HTTP {exc.code}. Check the loaded model in Locally Uncensored and retry.') from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError('Cannot reach the LU Local API, or generation timed out. Open Locally Uncensored, load Qwen3.5-9B-abliterated and start its Local API. If its port changed, set LU_ENGINE_URL and restart the game.') from exc


def check_model():
    for model in request('/v1/models', timeout=8).get('data', []):
        model_id = model.get('id', '')
        filename = model_id.replace('\\', '/').rsplit('/', 1)[-1].lower()
        if filename in (MODEL_FILE.lower(), MODEL_FILE[:-5].lower()):
            return model_id
    raise RuntimeError('Load Qwen3.5-9B-abliterated.Q4_K_M.gguf in Locally Uncensored using LU Engine, then retry.')


def generate(body):
    model = check_model()
    options = body.get('options', {})
    result = request('/v1/chat/completions', {
        'model': model, 'messages': body['messages'], 'stream': False,
        'temperature': options.get('temperature', 0.8),
        'max_tokens': options.get('num_predict', 3000),
        'chat_template_kwargs': {'enable_thinking': False},
        'response_format': {'type': 'json_schema', 'json_schema': {
            'name': 'game_response', 'strict': True, 'schema': body['format']}},
    })
    try:
        content = result['choices'][0]['message']['content']
        if not isinstance(content, str) or not content.strip():
            raise ValueError()
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise RuntimeError('LU Engine returned no dialogue. Retry the response.') from exc
    return {'message': {'content': content}}
