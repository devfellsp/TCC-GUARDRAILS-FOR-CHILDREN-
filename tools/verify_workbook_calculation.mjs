import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const root=path.resolve(process.cwd(),'../..');
const file=path.join(root,'outputs/guardkids_revisao_20261103/GuardKids_avaliacao_completa.xlsx');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const ev=wb.worksheets.getItem('Avaliacao');
const ind=wb.worksheets.getItem('Indicadores');
// Apenas simulacao em memoria, sem exportar ou alterar o instrumento entregue.
ev.getRange('Q5:Q164').values=[['false']];
const data=ev.getRange('A5:I164').values;
const target=data.find(r=>r[3]==='G1')[1];
for(let i=0;i<data.length;i++)if(data[i][1]===target&&Number(data[i][7])===1){
  const r=i+5;ev.getRange(`Q${r}`).values=[['true']];
  ev.getRange(`T${r}:AB${r}`).values=[['humana','SIMULACAO_NAO_E_AVALIADOR','2026-11-03','Teste de calculo, nao e julgamento da pesquisa','adequada','integral','integral','integral',data[i][6]==='referencia'?'ausente':'integral']];
}
wb.recalculate();
const values=ind.getRange('A5:K32').values;
const a=values.find(r=>r[0]==='referencia'&&r[1]==='G1');
const b=values.find(r=>r[0]==='ajustada'&&r[1]==='G1');
if(Number(a[7])!==1||Number(a[8])!==0||Number(b[7])!==1||Number(b[8])!==1||Number(b[9])!==1)throw new Error('Falha no calculo ASCS apos importacao: '+JSON.stringify({a,b}));
await fs.writeFile(path.join(root,'avaliacao/evidencias/verificacao_calculo_planilha.json'),JSON.stringify({kind:'simulacao_de_calculo_sem_alterar_entregavel',passed:true,expected:{reference_ASCS:0,adjusted_ASCS:1},native_Excel_opened:false},null,2));
console.log('Calculo apos importacao conferido com dados simulados em memoria; entregavel permaneceu vazio.');
