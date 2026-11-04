"""Inspecao somente leitura dos artefatos e folhas de contato para QA visual."""
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
def main():
    folder=ROOT/'.cache/academico'
    pages=sorted(folder.glob('tcc-*.png'))
    for start in range(0,len(pages),12):
        canvas=Image.new('RGB',(840,960),'#dadada'); draw=ImageDraw.Draw(canvas)
        for j,p in enumerate(pages[start:start+12]):
            im=Image.open(p); im.thumbnail((200,290)); x=(j%4)*210+5; y=(j//4)*320+20
            canvas.paste(im,(x,y)); draw.text((x,y-16),str(start+j+1),fill='black')
        canvas.save(folder/f'contact_{start//12+1}.png')
    reader=PdfReader(ROOT/'.cache/latex-output/main.pdf')
    text='\n\n'.join(f'PAGINA {i+1}\n'+(p.extract_text() or '') for i,p in enumerate(reader.pages))
    (folder/'pdf_texto.txt').write_text(text,encoding='utf-8')
    print(json.dumps({'pdf_pages':len(reader.pages),'text_chars':len(text),'replacement_chars':text.count(chr(0xfffd))},ensure_ascii=True))
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    for file in (ROOT/'outputs/guardkids_revisao_20261103').glob('*.xlsx'):
        with zipfile.ZipFile(file) as z:
            bad=[]; formulas=0
            for name in z.namelist():
                if not re.fullmatch(r'xl/worksheets/sheet\d+.xml',name):continue
                sheet=ET.fromstring(z.read(name))
                formulas+=len(sheet.findall('.//s:f',ns))
                bad.extend((name,c.get('r')) for c in sheet.findall('.//s:c',ns) if c.get('t')=='e')
            assert not bad,bad
            if 'cega' in file.name:
                data='\n'.join(z.read(n).decode('utf-8') for n in z.namelist() if n.endswith('.xml'))
                assert 'name="policy"' not in data and '<t>referencia</t>' not in data and '<t>ajustada</t>' not in data
                assert 'state="hidden"' not in data and 'state="veryHidden"' not in data
            print(json.dumps({'workbook':file.name,'formula_count':formulas,'errors':bad},ensure_ascii=True))

if __name__=='__main__':main()
