// Official SDK owns OAuth, identity verification, refresh and revocation.
// IPC returns session metadata and model output only, never credentials.
import {createChatGPT} from './vendor/sign-in-with-chatgpt-devkit/packages/local/dist/index.js';
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import {fileURLToPath} from 'node:url';
import {dirname, join} from 'node:path';
const root = dirname(fileURLToPath(import.meta.url));
const emit = value => process.stdout.write(JSON.stringify(value) + '\n');
function protect(mode, data) {
  return new Promise((resolve, reject) => {
    const proc = spawn('powershell.exe', ['-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',join(root,'credential-protection.ps1'),'-Mode',mode], {windowsHide:true, stdio:['pipe','pipe','pipe']});
    let output = '';
    proc.stdout.on('data', b => output += b.toString());
    proc.stderr.resume();
    proc.on('error', () => reject(new Error('Windows credential protection is unavailable.')));
    proc.on('close', code => code === 0 ? resolve(Buffer.from(output.trim(), 'base64')) : reject(new Error('Windows credential protection failed.')));
    proc.stdin.end(Buffer.from(data).toString('base64'));
  });
}
const client = createChatGPT({appName:'Mysterious Hearts',appId:'mysterious-hearts',redirectPort:0,
  sendHostId:true,storageDir:join(root,'.chatgpt'),
  credentialEncryption:{id:'windows-dpapi-current-user-v1',isAvailable:()=>process.platform==='win32',
    encrypt: text=>protect('encrypt',Buffer.from(text,'utf8')),
    decrypt: async bytes=>(await protect('decrypt',bytes)).toString('utf8')},
  openBrowser: url=>emit({event:'browser',url})});
const lines=createInterface({input:process.stdin});
lines.on('line', async line=>{
  let msg;
  try {
    msg=JSON.parse(line);
    let result;
    switch(msg.method) {
      case 'status': result=await client.getSession(); break;
      case 'signin': result=await client.signIn(); break;
      case 'cancel': client.cancelSignIn(); result={}; break;
      case 'disconnect': await client.disconnect(); result=await client.getSession(); break;
      case 'models': result=await client.listModels(); break;
      case 'generate': {
        const {messages,model,schema}=msg.params;
        const instructions=messages.filter(m=>m.role==='system').map(m=>m.content).join('\n')+
          '\nReturn only a JSON object conforming to this schema, without Markdown fences:\n'+JSON.stringify(schema);
        result=await client.streamResponse({model,instructions,input:messages.filter(m=>m.role!=='system'),signal:AbortSignal.timeout(220000)});
        break;
      }
      default: throw new Error('Unsupported account operation.');
    }
    emit({id:msg.id,result});
  } catch(error) {
    // Only the SDK's deliberately sanitized messages cross the bridge.
    emit({id:msg?.id,error:{code:error?.code ?? 'connection_error',message:error?.toJSON ? error.toJSON().message : 'The ChatGPT connection could not complete this operation.'}});
  }
});
lines.on('close',()=>{client.cancelSignIn();process.exit(0);});
