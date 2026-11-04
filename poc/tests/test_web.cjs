const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

test('falha depois de sucesso nao reapresenta fontes ou identificadores antigos', async () => {
  const nodes = new Map();
  const element = () => ({textContent:'', value:'', children:[], hidden:false,
    replaceChildren(){ this.children=[]; }, append(child){ this.children.push(child); }});
  const document = {
    querySelector(selector) { if (!nodes.has(selector)) nodes.set(selector, element()); return nodes.get(selector); },
    querySelectorAll(){ return []; }, createElement: element
  };
  let response = {ok:true, json:async () => ({ready:true})};
  const sent = [];
  const context = vm.createContext({document, fetch:async (url, options) => {
    if (options) sent.push(JSON.parse(options.body));
    return response;
  }, AbortController, setTimeout, clearTimeout});
  const html = fs.readFileSync(path.join(__dirname,'../web/index.html'),'utf8');
  vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1], context);
  await Promise.resolve();
  document.querySelector('#response-style').value = 'passo_a_passo';
  response = {ok:true, json:async () => ({answer:'Resposta anterior',action:'allow',seconds:1,policy:'comum',id:'ANTIGO',
    sources:[{source:'Fonte anterior',page:1,pdf_page:1}],stages:[{name:'generation',seconds:1}]})};
  await document.querySelector('#form').onsubmit({preventDefault(){}});
  assert.equal(nodes.get('#sources').children.length,1);
  assert.equal(sent[0].response_style,'passo_a_passo');
  assert.equal(sent[0].policy,'comum');
  assert.match(html, /<summary>Regra de proteção<\/summary>/);
  assert.doesNotMatch(html, /id="policy"/);
  assert.equal(nodes.get('#response-style').disabled,false);
  assert.match(nodes.get('#runid').textContent,/ANTIGO/);
  response = {ok:false,status:503};
  await document.querySelector('#form').onsubmit({preventDefault(){}});
  assert.equal(nodes.get('#sources').children.length,0);
  assert.equal(nodes.get('#stages').children.length,0);
  assert.equal(nodes.get('#meta').textContent,'');
  assert.equal(nodes.get('#runid').textContent,'');
  assert.match(nodes.get('#answer').textContent,/registrar/);
  assert.equal(nodes.get('#send').disabled,false);
});
