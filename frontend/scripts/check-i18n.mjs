import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve('src');
const dicts=['en','hi','or'].map(l=>JSON.parse(fs.readFileSync(path.join(root,'i18n',l+'.json'),'utf8')));
const keys=Object.keys(dicts[0]).sort();
for(const [index,dict] of dicts.entries()){
 if(JSON.stringify(Object.keys(dict).sort())!==JSON.stringify(keys))throw Error('Dictionary key mismatch: '+index);
 for(const [key,value] of Object.entries(dict))if(!value?.trim())throw Error('Empty translation '+key);
}
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
const missing=new Set();
for(const file of walk(root).filter(f=>f.endsWith('.jsx'))){
 const source=fs.readFileSync(file,'utf8');
 for(const match of source.matchAll(/(?:\bt\(\s*|(?:label|message|placeholder)=)(['"])(.*?)\1/g)){
  if(!(match[2] in dicts[0]))missing.add(match[2]);
 }
}
if(missing.size)throw Error('Missing translations: '+[...missing].join(', '));
console.log(keys.length+' keys present in English, Hindi and Odia; literal UI keys checked.');
