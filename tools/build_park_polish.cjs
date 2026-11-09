// Assemble imagegen scenery sprites with the game's code-native path geometry.
const fs=require('node:fs'),path=require('node:path');
const sharp=require(path.join(process.env.USERPROFILE,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'));
const root=path.resolve(__dirname,'..'),out=path.join(root,'assets/world/park');
const W=2048,H=320;
let seed=891;function random(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;}
const rect=(x,y,w,h,c)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"/>`;
const svg=s=>Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" shape-rendering="crispEdges">${s}</svg>`);
const blank=()=>sharp({create:{width:W,height:H,channels:4,background:'#00000000'}});
async function main(){
 const grid=await sharp(path.join(out,'source/props-atlas.png')).resize(2048,1024,{fit:'fill',kernel:'nearest'}).png().toBuffer();
 const parts={};
 for(const [i,name] of ['oak','maple','willow','gazebo','bench','lamp','hedge','flowers'].entries()){
  const {data,info}=await sharp(grid).extract({left:i%4*512,top:Math.floor(i/4)*512,width:512,height:512}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let x0=512,y0=512,x1=0,y1=0;
  for(let y=0;y<512;y++)for(let x=0;x<512;x++)if(data[(y*512+x)*4+3]>127){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}
  parts[name]=await sharp(data,{raw:info}).extract({left:x0,top:y0,width:x1-x0+1,height:y1-y0+1}).png().toBuffer();
 }
 async function prop(name,x,bottom,height){const input=await sharp(parts[name]).resize({height,kernel:'nearest'}).png().toBuffer();const m=await sharp(input).metadata();return {input,left:Math.round(x-m.width/2),top:bottom-height};}
 async function save(name,items,base){await (base?sharp(base):blank()).composite(items).png().toFile(path.join(out,name+'.png'));}
 for(const [name,width,height,top] of [['distant-hills',1024,248,0],['woodland',1024,290,-22]]){
  let tile=await sharp(path.join(out,'source/woodland.png')).resize(width,height,{kernel:'nearest'}).png().toBuffer();
  if(top<0)tile=await sharp(tile).extract({left:0,top:-top,width,height:height+top}).png().toBuffer();
  await save(name,[{input:tile,left:0,top:0},{input:tile,left:1024,top:0}]);
 }
 let garden=rect(0,225,W,95,'#263f38');
 for(let i=0;i<2000;i++){let x=Math.floor(random()*W),y=225+Math.floor(random()*42);garden+=rect(x,y,2+Math.floor(random()*3),1,random()<.5?'#3c5540':'#304b3b');}
 garden+='<ellipse cx="790" cy="245" rx="205" ry="26" fill="#253e45"/><ellipse cx="790" cy="242" rx="195" ry="21" fill="#345568"/>';
 for(let i=0;i<125;i++){let x=605+random()*370,y=228+random()*27;if(((x-790)/185)**2+((y-242)/16)**2<1)garden+=rect(Math.floor(x),Math.floor(y),3+Math.floor(random()*13),1,random()<.5?'#62888c':'#486f7b');}
 for(let i=0;i<65;i++){const a=i*Math.PI*2/65,x=Math.round(790+202*Math.cos(a)),y=Math.round(245+24*Math.sin(a));garden+=rect(x,y,5,3,i%2?'#6f7667':'#505e56');}
 const gardenItems=[];for(const x of [60,220,390,520,1080,1320,1530,1770,1940])gardenItems.push(await prop('hedge',x,263,26));
 for(const x of [120,350,1120,1380,1650,1900])gardenItems.push(await prop('flowers',x,265,20));
 await save('pond-and-shrubs',gardenItems,svg(garden));
 const trees=[];
 for(const [name,x,h] of [['oak',210,190],['maple',540,165],['willow',1010,183],['oak',1250,205],['maple',1510,174],['willow',1840,184]])trees.push(await prop(name,x,252,h));
 trees.splice(2,0,await prop('gazebo',670,251,95));
 await save('near-trees',trees);
 let ground=rect(0,256,W,12,'#38523c')+rect(0,268,W,30,'#433f43')+rect(0,298,W,22,'#233b32');
 const colors=['#665b57','#77665d','#6b625f','#7a6b60','#625a58'];
 for(let row=0;row<4;row++)for(let x=-18+(row%2)*13;x<W;x+=26){const y=269+row*7;ground+=rect(x+1,y,24,6,colors[Math.floor(random()*colors.length)])+rect(x+2,y,22,1,'#94806c');if(random()<.3)ground+=rect(x+7,y+4,4,1,'#464846');}
 for(let x=0;x<W;x+=13){ground+=rect(x,264,12,4,'#6c7461')+rect(x,264,11,1,'#929578');ground+=rect(x,299,12,3,'#51614c');}
 for(let i=0;i<220;i++){const x=Math.floor(random()*W),y=267+Math.floor(random()*32);ground+=rect(x,y,2,1,random()<.5?'#a27d4b':'#865b46');}
 const pathItems=[];
 for(const x of [90,380,700,1030,1390,1720])pathItems.push(await prop('lamp',x,267,78));
 for(const x of [410,1180])pathItems.push(await prop('bench',x,267,30));
 for(const x of [55,1490])ground+=rect(x,225,3,41,'#6d5545')+rect(x-12,218,40,17,'#304943')+rect(x-8,222,31,1,'#889b75')+rect(x-8,230,21,1,'#889b75');
 await save('playable-path',pathItems,svg(ground));
 let grass='';for(let x=0;x<W;x+=3){const y=307+Math.floor(random()*11);grass+=rect(x,y,1,320-y,random()<.5?'#476449':'#314d38');}
 const flowers=[];for(const x of [70,300,585,960,1300,1630,1940])flowers.push(await prop('flowers',x,320,16));
 await save('foreground-grass',flowers,svg(grass));
 const manifest=JSON.parse(fs.readFileSync(path.join(out,'layers.json'),'utf8'));
 for(const layer of manifest){const m=await sharp(path.join(out,layer.file)).metadata();if(m.width!==layer.size[0]||m.height!==layer.size[1])throw Error('Layer dimensions changed');}
 console.log('Built six detailed scenery planes; fixed sky, dimensions, depth order and collision baseline preserved.');
}
main().catch(e=>{console.error(e);process.exitCode=1});
