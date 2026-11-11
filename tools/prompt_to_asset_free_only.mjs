// Defense in depth for the project's offline prompt-to-asset MCP process.
// The source patch also removes provider tools and rejects non-inline modes.
import http from 'node:http';
import https from 'node:https';
import {syncBuiltinESMExports} from 'node:module';

const denied = () => { throw new Error('Mysterious Hearts: prompt-to-asset is local-only. Network generation and external sign-in are disabled.'); };
globalThis.fetch = async () => denied();
for (const client of [http, https]) {
  client.request = denied;
  client.get = denied;
}
syncBuiltinESMExports();
process.env.MH_MEDIA_FREE_ONLY = '1';
process.env.P2A_MAX_SPEND_USD_PER_RUN = '0';
