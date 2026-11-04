"""Inspecao de fonte e PDF fornecidos como referencia; nao executa arquivos do ZIP."""
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.cache/validacao_unitins'
SOURCE = Path('C:/Users/Filipe/Downloads/Model_TCC_Latex_preenchido(1).zip')

def pdf_info(path):
    reader = PdfReader(path)
    pages = [p.extract_text() or '' for p in reader.pages]
    text_path = WORK / (path.stem + '_texto.txt')
    text_path.write_text('\n\n'.join(f'PAGINA FISICA {i+1}\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
    fonts=set()
    for p in reader.pages:
        resources=p.get('/Resources')
        if resources:
            collection=resources.get_object().get('/Font')
            if collection:
                for f in collection.get_object().values():
                    fonts.add(str(f.get_object().get('/BaseFont')))
    outline=[]
    def walk(items,level=0):
        for item in items:
            if isinstance(item,list): walk(item,level+1)
            else:
                try: page=reader.get_destination_page_number(item)+1
                except (ValueError,TypeError,KeyError): page=None
                outline.append({'level':level,'title':item.get('/Title'),'physical_page':page})
    walk(reader.outline)
    return {'path':str(path),'pages':len(pages),'text_chars':sum(map(len,pages)),
            'fonts':sorted(fonts),'outline':outline,'text_file':str(text_path),
            'metadata':{str(k):str(v) for k,v in (reader.metadata or {}).items()}}

def main():
    dest=(WORK/'referencia').resolve();dest.mkdir(parents=True,exist_ok=True)
    manifest={};total=0
    with zipfile.ZipFile(SOURCE) as archive:
        for info in archive.infolist():
            parts=PurePosixPath(info.filename).parts
            if info.is_dir() or any(p.startswith('.') for p in parts):continue
            if PurePosixPath(info.filename).suffix.lower() not in {'.tex','.sty','.bib','.pdf','.png','.jpg','.jpeg'}:continue
            target=(dest/Path(*parts[1:])).resolve()
            total+=info.file_size
            if not target.is_relative_to(dest) or info.file_size>20_000_000 or total>50_000_000:raise ValueError('Entrada de ZIP invalida')
            target.parent.mkdir(parents=True,exist_ok=True)
            data=archive.read(info);target.write_bytes(data)
            manifest[str(target.relative_to(dest)).replace('\\','/')]=hashlib.sha256(data).hexdigest()
    value={'source_zip':str(SOURCE),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'extracted':manifest,
           'reference':pdf_info(dest/'tcc.pdf'), 'guardkids':pdf_info(ROOT/'output/pdf/TCC_GuardKids_TCCI_revisado.pdf')}
    for path in (dest/'anexos').glob('*.pdf'):value[path.stem]=pdf_info(path)
    source_stats={}
    for path in [*sorted(dest.glob('c_*.tex')),*sorted((ROOT/'texto').glob('0*.tex'))]:
        raw=path.read_text(encoding='utf-8-sig',errors='replace')
        text=re.sub(r'(?<!\\)%[^\n]*','',raw)
        text=re.sub(r'\\begin\{comment\}.*?\\end\{comment\}','',text,flags=re.S)
        source_stats[str(path)]= {'chapters':re.findall(r'\\chapter\*?\{([^}]+)',text),
            'sections':re.findall(r'\\(?:sub)*section\*?\{([^}]+)',text),
            'citations':len(re.findall(r'\\cite\w*\s*[\[{]',text)),
            'figures':len(re.findall(r'\\begin\{figure',text)),
            'tables':len(re.findall(r'\\begin\{(?:table|longtable)',text)),
            'chars_without_comments':len(text)}
    value['source_stats']=source_stats
    (WORK/'comparacao_dados.json').write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'reference_pages':value['reference']['pages'],'guardkids_pages':value['guardkids']['pages'],
                     'selected_files':len(manifest),'reference_outline':value['reference']['outline'][:18]},ensure_ascii=True,indent=2))

if __name__=='__main__':main()
