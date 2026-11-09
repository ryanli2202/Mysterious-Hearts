// Package the imagegen polish pass into aligned, side-scrolling animation assets.
const fs=require('node:fs'),path=require('node:path');
const sharp=require(path.join(process.env.USERPROFILE,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'));
const dir=path.resolve('assets/sprites/chibi-preview/garrett-v2');
async function main(){
 fs.mkdirSync(dir,{recursive:true});
 const source=path.join(dir,'source-sheet.png');
 if(process.argv[2]) fs.copyFileSync(process.argv[2],source);
 const grid=await sharp(source).resize(2048,1024,{fit:'fill',kernel:'nearest'}).png().toBuffer();
 const cw=256,ch=512;
 const rows=[];
 for(let row=0;row<2;row++){
  const frames=[];
  for(let col=0;col<8;col++){
   // Hold the same open-eye idle drawing to avoid generative silhouette shimmer.
   const sourceCol=row===0?(col===6?6:0):col;
   const {data,info}=await sharp(grid).extract({left:sourceCol*cw,top:row*ch,width:cw,height:ch}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
   let x0=cw,y0=ch,x1=0,y1=0,hx0=cw,hx1=0;
   for(let y=0;y<ch;y++)for(let x=0;x<cw;x++)if(data[(y*cw+x)*4+3]>127){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);if(y<ch*.38){hx0=Math.min(hx0,x);hx1=Math.max(hx1,x);}}
   const scale=56/(ch*.88),w=Math.round((x1-x0+1)*scale),h=Math.round((y1-y0+1)*scale);
   const headCenter=(hx0+hx1)/2;
   const left=24-Math.round((headCenter-x0)*scale),top=61-h;
   if(left<0||left+w>48||top<0)throw Error('Frame does not fit');
   const crop=await sharp(data,{raw:info}).extract({left:x0,top:y0,width:x1-x0+1,height:y1-y0+1}).resize(w,h,{kernel:'nearest'}).png().toBuffer();
   const frame=await sharp({create:{width:48,height:64,channels:4,background:'#00000000'}}).composite([{input:crop,left,top}]).png().toBuffer();
   frames.push(frame);
  }
  rows.push(frames);
 }
 const all=[],animations={};
 for(const direction of ['right','left'])for(let r=0;r<2;r++){
  const name=`${r?'walk':'idle'}-${direction}`;
  const frames=await Promise.all(rows[r].map(f=>direction==='left'?sharp(f).flop().png().toBuffer():f));
  const durations=r?Array(8).fill(100):[600,250,250,250,250,200,100,450];
  animations[name]={row:all.length/8,frames:8,durationsMs:durations};
  for(let i=0;i<8;i++)await sharp(frames[i]).toFile(path.join(dir,`${name}-${i+1}.png`));
  const raw=await Promise.all(frames.map(f=>sharp(f).resize(192,256,{kernel:'nearest'}).flatten({background:'#172131'}).removeAlpha().raw().toBuffer()));
  await sharp(Buffer.concat(raw),{raw:{width:192,height:2048,channels:3,pageHeight:256}}).gif({loop:0,delay:durations,dither:0}).toFile(path.join(dir,`${name}.gif`));
  all.push(...frames);
 }
 await sharp({create:{width:384,height:256,channels:4,background:'#00000000'}}).composite(all.map((input,i)=>({input,left:i%8*48,top:Math.floor(i/8)*64}))).png().toFile(path.join(dir,'sprite-sheet.png'));
 await sharp(path.join(dir,'sprite-sheet.png')).resize(1536,1024,{kernel:'nearest'}).flatten({background:'#172131'}).toFile(path.join(dir,'contact-sheet.png'));
 fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify({character:'garrett',status:'polished-preview',movement:'side-scrolling',frameWidth:48,frameHeight:64,columns:8,rows:4,anchor:[24,61],animations,leftDirection:'Horizontally mirrored; asymmetric clothing details mirror too.',walkCycleMs:800,integration:'Not yet connected to map movement.'},null,2)+'\n');
 for(const name of Object.keys(animations)){
  const m=await sharp(path.join(dir,name+'.gif'),{animated:true}).metadata();
  const expected=animations[name].durationsMs.reduce((a,b)=>a+b,0);
  if((name.startsWith('walk')&&m.pages!==8)||m.pageHeight!==256||m.delay.reduce((a,b)=>a+b,0)!==expected)throw Error('Invalid GIF '+name);
  console.log(name, m.pages+' frames',m.delay);
 }
 console.log('Validated four directional animations and sprite-sheet packaging.');
}
main().catch(e=>{console.error(e);process.exitCode=1});
