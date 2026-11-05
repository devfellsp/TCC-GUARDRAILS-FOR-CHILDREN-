const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

test('materias dinamicas, envio correto e troca limpa a resposta anterior', async () => {
  const nodes = new Map();
  const element = () => ({textContent:'',value:'',children:[],hidden:false,disabled:false,
    replaceChildren(){this.children=[];},append(child){this.children.push(child);},focus(){}});
  const document = {
    querySelector(s){if(!nodes.has(s))nodes.set(s,element());return nodes.get(s);},
    querySelectorAll(){return [];},createElement:element
  };
  const subjects = ['portugues','matematica','ciencias','historia','geografia','arte','educacao_fisica','ingles','tecnologia','geral'];
  const channels = Object.fromEntries(subjects.map(key=>[key,{label:key,title:key,scope:key,examples:['Um','Dois','Tres']}]));
  let askResponse={ok:true,json:async()=>({answer:'Resposta com fontes',action:'allow',seconds:1,id:'TESTE',response_style:'padrao',sources:[{source:'Fonte',page:1,pdf_page:2}],stages:[]})};
  const sent=[];
  const context=vm.createContext({document,AbortController,setTimeout,clearTimeout,fetch:async(url,opts)=>{
    if(url==='/api/channels')return {ok:true,json:async()=>channels};
    if(url==='/api/status')return {ok:true,json:async()=>({ready:true,request_timeout_ms:610000})};
    sent.push(JSON.parse(opts.body));return askResponse;
  }});
  const html=fs.readFileSync(path.join(__dirname,'../versions/GK-P2.6-dev/web/index.html'),'utf8');
  vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
  await new Promise(resolve=>setImmediate(resolve));
  assert.equal(nodes.get('#channel').children.length,10);
  assert.equal(nodes.get('#send').disabled,false);
  nodes.get('#channel').value='matematica';nodes.get('#response-style').value='padrao';
  nodes.get('#question').value='Como lemos fracoes?';
  await nodes.get('#form').onsubmit({preventDefault(){}});
  assert.equal(sent[0].channel,'matematica');
  assert.equal(nodes.get('#sources').children.length,1);
  nodes.get('#channel').value='ingles';nodes.get('#channel').onchange();
  assert.equal(nodes.get('#sources').children.length,0);
  assert.equal(nodes.get('#answer').textContent,'');
  askResponse={ok:false,status:503};
  await nodes.get('#form').onsubmit({preventDefault(){}});
  assert.match(nodes.get('#answer').textContent,/registrar/);
  assert.equal(nodes.get('#channel').disabled,false);
});
