// Package imagegen-authored frames; no character artwork is drawn here.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(path.join(process.env.USERPROFILE, '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'));
const dir = path.resolve('assets/sprites/chibi-preview/garrett');
async function main() {
  fs.mkdirSync(dir, {recursive:true});
  const source = path.join(dir, 'source-sheet.png');
  if (process.argv[2]) fs.copyFileSync(process.argv[2], source);
  const all = [];
  for (let row=0;row<2;row++) {
    const frames=[];
    for (let col=0;col<6;col++) {
      const frame = await sharp(source).extract({left:col*256,top:row*512,width:256,height:512})
        .resize(48,64,{fit:'contain',kernel:'nearest',background:'#00000000'}).png().toBuffer();
      await sharp(frame).toFile(path.join(dir,`${row?'walk':'idle'}-${col+1}.png`));
      frames.push(frame); all.push(frame);
    }
    const delay = row ? [120,120,120,120,120,120] : [650,250,300,250,110,500];
    const raws=await Promise.all(frames.map(f=>sharp(f).resize(192,256,{kernel:'nearest'}).flatten({background:'#172131'}).raw().toBuffer()));
    await sharp(Buffer.concat(raws),{raw:{width:192,height:256*6,channels:3,pageHeight:256}})
      .gif({loop:0,delay,dither:0}).toFile(path.join(dir,row?'walk.gif':'idle.gif'));
  }
  await sharp({create:{width:288,height:128,channels:4,background:'#00000000'}})
    .composite(all.map((input,i)=>({input,left:(i%6)*48,top:Math.floor(i/6)*64})))
    .png().toFile(path.join(dir,'sprite-sheet.png'));
  const metadata={character:'garrett',status:'style-preview-only',direction:'right',frameWidth:48,frameHeight:64,columns:6,rows:2,anchor:[24,60],animations:{idle:{row:0,durationsMs:[650,250,300,250,110,500]},walk:{row:1,durationsMs:[120,120,120,120,120,120]}},notes:'Generated pixel-art style test. Not integrated into the game. Left/back/front directions and final animation cleanup pending style approval.'};
  fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify(metadata,null,2)+'\n');
  for(const name of ['idle.gif','walk.gif','sprite-sheet.png']) {
    const m=await sharp(path.join(dir,name),{animated:true}).metadata();
    console.log(name,JSON.stringify({width:m.width,height:m.height,pages:m.pages,pageHeight:m.pageHeight,delay:m.delay,alpha:m.hasAlpha}));
    if(name.endsWith('.gif') && m.pages!==6) throw Error('Expected six animation frames');
  }
}
main().catch(e=>{console.error(e);process.exitCode=1});
