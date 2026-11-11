// Integration contract: free local exports work; API/account routes fail closed.
// Oracle: the user's free/no-sign-in requirement and FREE_MEDIA_PLUGINS.md.
// No provider, model, or MCP response is mocked. Outputs use a fresh test directory.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawn, spawnSync } from 'node:child_process';
import { createInterface } from 'node:readline';
import { createRequire } from 'node:module';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const config = JSON.parse(fs.readFileSync(path.join(root, 'tools/media_plugins.runtime.json')));
const tmp = path.join(root, '.test-tmp/media');
fs.mkdirSync(tmp, { recursive: true });
const output = fs.mkdtempSync(path.join(tmp, 'p2a-'));
const allowed = ['asset_capabilities', 'asset_generate_logo', 'asset_generate_app_icon',
  'asset_generate_favicon', 'asset_save_inline_svg', 'asset_validate',
  'asset_brand_bundle_parse', 'asset_export_bundle', 'asset_sprite_sheet', 'asset_nine_slice'];
const child = spawn(config.python, [path.join(root, 'tools/media_tools.py'), 'p2a'], {
  cwd: root, env: { ...process.env, OPENAI_API_KEY: 'FAKE-TEST-CREDENTIAL-DO-NOT-USE' },
  stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true,
});
let serial = 0;
const pending = new Map();
let stderr = '';
child.stderr.on('data', chunk => { stderr += chunk; });
createInterface({ input: child.stdout }).on('line', line => {
  const message = JSON.parse(line);
  const item = pending.get(message.id);
  if (item) {
    clearTimeout(item.timer);
    pending.delete(message.id);
    message.error ? item.reject(new Error(JSON.stringify(message.error))) : item.resolve(message.result);
  }
});
child.on('exit', code => {
  for (const item of pending.values()) { clearTimeout(item.timer); item.reject(new Error(`MCP exited ${code}: ${stderr}`)); }
  pending.clear();
});
function request(method, params = {}) {
  const id = ++serial;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`Timed out: ${method}`)); }, 45000);
    pending.set(id, { resolve, reject, timer });
    child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
}
const call = (name, args) => request('tools/call', { name, arguments: args });
const body = result => result.content.filter(c => c.type === 'text').map(c => c.text).join('\n');
const files = directory => fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
  const absolute = path.join(directory, entry.name);
  return entry.isDirectory() ? files(absolute) : [absolute];
});
try {
  const handshake = await request('initialize', {
    protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'mh-free-media-check', version: '1.0.0' },
  });
  assert.ok(handshake.serverInfo.name, 'Real MCP handshake must complete');
  child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
  const listing = await request('tools/list');
  assert.deepEqual(listing.tools.map(t => t.name).sort(), [...allowed].sort(), 'Only the ten approved tools are exposed');
  for (const tool of listing.tools.filter(t => t.name.startsWith('asset_generate_'))) {
    assert.deepEqual(tool.inputSchema.properties.mode.enum, ['inline_svg'], 'Discovery must not advertise paid modes');
  }
  const plan = await call('asset_generate_logo', { brief: 'A simple magenta heart silhouette with no text', output_dir: output });
  assert.equal(plan.isError, undefined, body(plan));
  assert.equal(JSON.parse(body(plan)).mode, 'inline_svg', 'Default must remain local even with a fake inherited provider key');
  for (const mode of ['api', 'external_prompt_only']) {
    const rejected = await call('asset_generate_logo', { brief: 'Policy verification', mode });
    assert.equal(rejected.isError, true, `${mode} must be rejected`);
    assert.match(body(rejected), /Only inline_svg mode is enabled/, 'Reject at the policy gate, not through a network failure');
  }
  const disabled = await call('asset_train_brand_lora', { brief: 'Policy verification' });
  assert.equal(disabled.isError, true);
  assert.match(body(disabled), /Disabled by project free-only policy/);
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="#db2777" d="M256 256H768V768H256Z"/></svg>';
  const saved = await call('asset_save_inline_svg', { svg, asset_type: 'favicon', output_dir: output, app_name: 'Install test', theme_color: '#182232' });
  assert.equal(saved.isError, undefined, body(saved));
  const generated = files(output);
  const master = generated.find(f => path.basename(f) === 'icon.svg');
  assert.ok(master, 'Export must actually persist the SVG');
  assert.match(fs.readFileSync(master, 'utf8'), /#db2777/i);
  const png = generated.find(f => path.basename(f) === 'favicon-32.png');
  assert.ok(png, 'A real 32px raster export is required');
  const require = createRequire(path.join(config.prompt_runtime, 'package.json'));
  const sharp = require('sharp');
  const decoded = await sharp(png).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  assert.equal(decoded.info.width, 32);
  assert.equal(decoded.info.height, 32);
  const center = (16 * 32 + 16) * 4;
  assert.deepEqual([...decoded.data.subarray(center, center + 4)], [219, 39, 119, 255], 'Raster center must preserve the input colour');
  assert.equal(decoded.data[3], 0, 'Raster corner must remain transparent');
  const guard = spawnSync(config.node, ['--import', pathToFileURL(path.join(root, 'tools/prompt_to_asset_free_only.mjs')).href, '--input-type=module', '-e',
    "import assert from 'node:assert/strict'; import http from 'node:http'; await assert.rejects(fetch('http://127.0.0.1:9/'), /disabled/i); assert.throws(() => http.get('http://127.0.0.1:9/'), /disabled/i); console.log('network-blocked');"],
    { encoding: 'utf8', cwd: root, windowsHide: true });
  assert.equal(guard.status, 0, guard.stderr);
  assert.match(guard.stdout, /network-blocked/);
  console.log(JSON.stringify({ passed: true, checks: ['MCP handshake', 'ten-tool allowlist', 'inline-only discovery', 'local default', 'API rejection', 'external-mode rejection', 'hidden-tool rejection', 'SVG persistence', 'PNG dimensions/colour/transparency', 'network guard'], output }, null, 2));
} finally {
  child.stdin.end();
}
