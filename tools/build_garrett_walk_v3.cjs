// Animate imagegen-authored cutout parts with a periodic two-leg walk rig.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const sharp=require(path.join(process.env.USERPROFILE,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'));
const fullerArms=process.argv.includes('--fuller-arms');
const slim=process.argv.includes('--slim')||fullerArms;
const out=path.resolve(`assets/sprites/chibi-preview/garrett-${fullerArms?'v5':slim?'v4':'v3'}`);
const N=24,delay=40,stance=.6,stride=14,ground=61;
const mod=x=>((x%1)+1)%1;
function foot(p){p=mod(p);if(p<stance)return {x:24+7-stride*p/stance,y:58};const t=(p-stance)/(1-stance);return {x:17+14*(t*t*(3-2*t)),y:58-6*Math.sin(Math.PI*t)};}
function knee(hip,ankle){const dx=ankle.x-hip.x,dy=ankle.y-hip.y,d=Math.hypot(dx,dy);assert(d<20,'Leg target reachable');const h=Math.sqrt(100-d*d/4);return {x:(hip.x+ankle.x)/2+dy/d*h,y:(hip.y+ankle.y)/2-dx/d*h};}
function state(p){const bob=.65*Math.cos(4*Math.PI*p);const hip={x:24,y:40+bob};const near=foot(p),far=foot(p+.5);return {hip,near,far,nk:knee(hip,near),fk:knee(hip,far),bob};}
async function main(){
 fs.mkdirSync(out,{recursive:true});
 if(fullerArms)fs.copyFileSync(path.resolve('assets/sprites/chibi-preview/garrett-v4/body-source.png'),path.join(out,'body-source.png'));
 const source=slim?path.resolve('assets/sprites/chibi-preview/garrett-v3/parts-source.png'):path.join(out,'parts-source.png');if(process.argv[2]&&!slim)fs.copyFileSync(process.argv[2],source);
 const grid=await sharp(source).resize(1536,1024,{fit:'fill',kernel:'nearest'}).png().toBuffer();
 const names=['body','upper-arm','forearm','thigh','calf','shoe'],parts={};
 for(let i=0;i<6;i++){
  const {data,info}=await sharp(grid).extract({left:i%3*512,top:Math.floor(i/3)*512,width:512,height:512}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let x0=512,y0=512,x1=0,y1=0;
  for(let y=0;y<512;y++)for(let x=0;x<512;x++)if(data[(y*512+x)*4+3]>128){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}
  const png=await sharp(data,{raw:info}).extract({left:x0,top:y0,width:x1-x0+1,height:y1-y0+1}).png().toBuffer();
  fs.writeFileSync(path.join(out,names[i]+'.png'),png);parts[names[i]]='data:image/png;base64,'+png.toString('base64');
 }
 if(slim){
  const {data,info}=await sharp(path.join(out,'body-source.png')).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let x0=info.width,y0=info.height,x1=0,y1=0;
  for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++)if(data[(y*info.width+x)*4+3]>128){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}
  const png=await sharp(data,{raw:info}).extract({left:x0,top:y0,width:x1-x0+1,height:y1-y0+1}).png().toBuffer();
  fs.writeFileSync(path.join(out,'body.png'),png);parts.body='data:image/png;base64,'+png.toString('base64');
 }
 const img=(name,x,y,w,h)=>`<image href="${parts[name]}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="none"/>`;
 function segment(name,a,b,w,pad=1.3){const angle=Math.atan2(-(b.x-a.x),b.y-a.y)*180/Math.PI,len=Math.hypot(b.x-a.x,b.y-a.y);return `<g transform="translate(${a.x} ${a.y}) rotate(${angle})">${img(name,-w/2,-pad,w,len+2*pad)}</g>`;}
 function arm(p,bob,far){const shoulder={x:slim?(far?25:23):(far?26:21),y:29+bob},angle=.38*Math.cos(2*Math.PI*p)*(far?1:-1);const elbow={x:shoulder.x+Math.sin(angle)*7,y:shoulder.y+Math.cos(angle)*7};const wrist={x:elbow.x+Math.sin(angle+.16)*6,y:elbow.y+Math.cos(angle+.16)*6};return segment('upper-arm',shoulder,elbow,fullerArms?4.5:slim?3.5:5,1)+segment('forearm',elbow,wrist,fullerArms?4.2:slim?3.2:4.7,.5);}
 function leg(hip,k,f,p){let s=segment('thigh',hip,k,5.5)+segment('calf',k,f,4.6);p=mod(p);const roll=p<.08?-12*(1-p/.08):p>.52&&p<.6?14*(p-.52)/.08:0;const pivot=roll>0?6:-2;s+=`<g transform="translate(${f.x} ${f.y}) translate(${pivot} 3) rotate(${roll}) translate(${-pivot} -3)">${img('shoe',-2,-1,8,4)}</g>`;return s;}
 const frames=[],tracks=[];
 for(let i=0;i<=N;i++){
  const p=i===N?.25:i/N,s=state(p);
  if(i===N){s.bob=0;s.hip={x:24,y:40};s.near={x:25,y:58};s.far={x:23,y:58};s.nk=knee(s.hip,s.near);s.fk=knee(s.hip,s.far);}
  else tracks.push(s);
  const far=`<g filter="url(#far)">${arm(p,s.bob,true)}${leg(s.hip,s.fk,s.far,p+.5)}</g>`;
  const body=img('body',slim?10.5:11.5,2+s.bob,25,39);
  // Keep the head scale fixed; fit the new torso to a 9px side-profile rig.
  const fittedBody=slim?`<g clip-path="url(#head)">${body}</g><g clip-path="url(#torso)"><g transform="translate(24 0) scale(1.3 1) translate(-24 0)">${body}</g></g>`:body;
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="192" height="256" viewBox="0 0 48 64"><defs><clipPath id="head"><rect width="48" height="${26+s.bob}"/></clipPath><clipPath id="torso"><rect y="${26+s.bob}" width="48" height="38"/></clipPath><filter id="far"><feComponentTransfer><feFuncR type="linear" slope=".70"/><feFuncG type="linear" slope=".70"/><feFuncB type="linear" slope=".74"/></feComponentTransfer></filter></defs>${far}${leg(s.hip,s.nk,s.near,p)}${fittedBody}${arm(p,s.bob,false)}</svg>`;
  frames.push(await sharp(Buffer.from(svg)).resize(48,64,{kernel:'nearest'}).png().toBuffer());
 }
 // Periodic position and stance translation checks include the loop seam.
 assert.deepEqual(state(0),state(1));
 for(let i=1;i<14;i++){const a=foot((i-1)/N),b=foot(i/N);assert(Math.abs(b.x-a.x+stride/(stance*N))<1e-9);assert.equal(b.y,58);}
 const jumps=tracks.map((s,i)=>Math.hypot(s.near.x-tracks[(i+1)%N].near.x,s.near.y-tracks[(i+1)%N].near.y));
 assert(jumps[N-1]<=Math.max(...jumps.slice(0,-1)),'Loop seam must not be the largest foot jump');
 assert(Math.min(...tracks.map(s=>s.near.y))<=52.1,'Swing foot lifts at least 5.9 pixels');
 const idle=frames.pop();
 const all=[];
 for(const direction of ['right','left']){
  await (direction==='left'?sharp(idle).flop():sharp(idle)).png().toFile(path.join(out,`idle-${direction}.png`));
  const list=await Promise.all(frames.map(f=>direction==='left'?sharp(f).flop().png().toBuffer():f));all.push(...list);
  for(let i=0;i<N;i++)fs.writeFileSync(path.join(out,`walk-${direction}-${String(i+1).padStart(2,'0')}.png`),list[i]);
  const raw=await Promise.all(list.map(f=>sharp(f).resize(192,256,{kernel:'nearest'}).flatten({background:'#172131'}).removeAlpha().raw().toBuffer()));
  await sharp(Buffer.concat(raw),{raw:{width:192,height:256*N,channels:3,pageHeight:256}}).gif({delay:Array(N).fill(delay),loop:0,dither:0}).toFile(path.join(out,`walk-${direction}.gif`));
  const m=await sharp(path.join(out,`walk-${direction}.gif`),{animated:true}).metadata();assert.equal(m.pages,N);assert.equal(m.delay.reduce((a,b)=>a+b),960);
 }
 await sharp({create:{width:384,height:384,channels:4,background:'#00000000'}}).composite(all.map((input,i)=>({input,left:i%8*48,top:Math.floor(i/8)*64}))).png().toFile(path.join(out,'sprite-sheet.png'));
 await sharp(path.join(out,'sprite-sheet.png')).resize(1152,1152,{kernel:'nearest'}).flatten({background:'#172131'}).toFile(path.join(out,'contact-sheet.png'));
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({character:'garrett',frameWidth:48,frameHeight:64,columns:8,rows:6,groundY:ground,anchor:[24,ground],animations:{'walk-right':{startFrame:0,count:N,durationMs:delay},'walk-left':{startFrame:24,count:N,durationMs:delay}},cycleMs:960,suggestedSpeedPixelsPerSecond:stride/(stance*.96),method:'Periodic cutout skeletal walk; 60% stance, 40% swing, 6px foot lift, alternating legs and counter-swing arms.',left:'Mirrored right; asymmetric costume details mirror.',idle:'../garrett-v2/manifest.json',status:'External animation preview; not connected to game movement.'},null,2)+'\n');
 fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({frameCountPerDirection:N,cycleMs:960,periodicSeam:true,stanceTranslation:'constant backwards velocity relative to torso',minimumSwingFootY:Math.min(...tracks.map(s=>s.near.y)),seamFootDelta:jumps[N-1],maximumOtherFootDelta:Math.max(...jumps.slice(0,-1)),allLegTargetsReachable:true},null,2)+'\n');
 console.log('PASS: 24 frames per direction, 960ms timing, reachable legs, lifted swing foot, constant stance velocity, periodic seam.');
}
main().catch(e=>{console.error(e);process.exitCode=1});
