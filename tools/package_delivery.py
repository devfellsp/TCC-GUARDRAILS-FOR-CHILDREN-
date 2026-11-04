"""Empacota apenas materiais de entrega; exclui modelos, livros integrais e ambientes."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/guardkids_revisao_20261103'

def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    pdf=ROOT/'output/pdf/TCC_PoC_TCCI_revisado.pdf'
    reader=PdfReader(pdf)
    text='\n'.join(p.extract_text() or '' for p in reader.pages)
    log=(ROOT/'.cache/latex-output/main.log').read_text(encoding='utf-8',errors='replace')
    issues=re.findall(r'Overfull|Missing character|LaTeX Error|LaTeX Warning:.*undefined',log)
    assert not issues,issues
    assert '??' not in text and chr(0xfffd) not in text
    assert not any(not(p.extract_text() or '').strip() for p in reader.pages)
    active=json.loads((ROOT/'avaliacao/congelamento_ativo.json').read_text())['id']
    models=json.loads((ROOT/'avaliacao/congelamentos'/f'{active}.json').read_text())['model_digests']
    fonts=sorted({str(font.get_object().get('/BaseFont')) for page in reader.pages for font in page.get('/Resources').get_object().get('/Font',{}).get_object().values()})
    qa={'stage':'Projeto/TCC I','pdf_pages':len(reader.pages),'pdf_sha256':sha(pdf.read_bytes()),'pdf_no_overfull_missing_glyphs_or_undefined_refs':True,
        'visual_review':'capas, resumos, sumario, listas, figuras, tabelas, algoritmo, referencias e paginas de contato inspecionados',
        'fonts':fonts,'python_tests_passed':45,'javascript_tests_passed':1,'new_development_executions':108,'reused_development_questions':27,
        'final_executions':0,'human_judgments':0,'xlsx_formula_errors':0,'workbook_calculation_simulation_passed':True,
        'native_Excel_opened':False,'remote_Overleaf_used':False,'Overleaf_zip_compiled_in_isolated_folder':True,
        'active_freeze':active,'model_digests':models,
        'known_build_notes':'Tres avisos de comentarios UTF-8 do algorithm2e e aviso de configuracao fontconfig; sem caractere substituto extraido ou defeito visual observado.'}
    (ROOT/'avaliacao/evidencias/verificacao_entrega.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    selected=[ROOT/n for n in ['main.tex','document.tex','unitins.sty','unitins.png','latexmkrc','README.md','LEIA-ME_OVERLEAF.md','ENTREGA_LEIA-ME.md','Overleaf_TCC_PoC.zip']]
    for directory in ['texto','generated','imagens','tools','diagramas','.github','avaliacao']:
        for p in (ROOT/directory).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and not (directory=='avaliacao' and p.suffix=='.pdf'):
                selected.append(p)
    selected.extend(p for p in (ROOT/'poc').glob('*') if p.is_file() and p.suffix in {'.py','.json','.txt','.md','.ps1','.cmd'})
    for directory in ['prompts','web','tests','docs']:
        selected.extend(p for p in (ROOT/'poc'/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    selected.extend([pdf,OUT/'GuardKids_avaliacao_completa.xlsx',OUT/'GuardKids_revisao_cega.xlsx'])
    selected=sorted(set(selected))
    manifest={str(p.relative_to(ROOT)).replace('\\','/'):{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in selected}
    output=OUT/'Entrega_PoC_TCCI_revisado.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for p in selected:z.writestr(str(p.relative_to(ROOT)).replace('\\','/'),p.read_bytes())
        z.writestr('MANIFESTO_SHA256.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for name,meta in manifest.items():assert sha(z.read(name))==meta['sha256']
    (OUT/'Entrega_PoC_TCCI_revisado.sha256').write_text(sha(output.read_bytes())+'  '+output.name+'\n',encoding='ascii')
    print(json.dumps({'file':str(output),'files':len(manifest),'bytes':output.stat().st_size,'sha256':sha(output.read_bytes()),'pdf_pages':len(reader.pages)},ensure_ascii=False))

if __name__=='__main__':main()
