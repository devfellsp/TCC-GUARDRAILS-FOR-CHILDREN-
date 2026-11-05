"""Diagramas nativos no estilo aprovado pelo autor: preto e branco, Arial, sem cartões.

Mantém o primeiro desenho do autor e produz os outros seis em páginas independentes.
"""
from pathlib import Path
from copy import deepcopy
import xml.etree.ElementTree as ET
import zipfile
import math
import re
from html import unescape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'diagramas/estilo_usuario'
BASE_STYLE='rounded=0;whiteSpace=wrap;html=1;fontFamily=Arial;fontSize=14;strokeColor=#000000;fillColor=#FFFFFF;shadow=0;strokeWidth=1;'


class Diagram:
    def __init__(self,slug,name,landscape=False):
        self.slug,self.name=slug,name
        self.w,self.h=(1169,827) if landscape else (827,1169)
        self.nodes={};self.edges=[]
    def box(self,key,x,y,w,h,label,shape='box',bold=False,font=14):
        self.nodes[key]=dict(x=x,y=y,w=w,h=h,label=label,shape=shape,bold=bold,font=font)
        return key
    def group(self,key,x,y,w,h,label):
        return self.box(key,x,y,w,h,label,'group',True,11)
    def link(self,a,b,points=None,label='',at=None,start='bottom',end='top',dashed=False):
        def port(n,side):
            x,y,w,h=n['x'],n['y'],n['w'],n['h']
            return {'top':(x+w/2,y),'bottom':(x+w/2,y+h),'left':(x,y+h/2),'right':(x+w,y+h/2)}[side]
        path=[port(self.nodes[a],start),*(points or []),port(self.nodes[b],end)]
        self.edges.append(dict(a=a,b=b,path=path,label=label,at=at,start=start,end=end,dashed=dashed))


def diagrams():
    ds=[]
    d=Diagram('02_Analise_contextual','02 Análise contextual')
    d.box('q',303,40,220,55,'Pergunta')
    d.box('intent',303,145,220,65,'Analisar intenção\ne contexto')
    d.box('route',303,260,220,140,'Qual tratamento?','diamond')
    d.box('block',35,490,210,65,'Bloquear pedido')
    d.box('retrieve',303,490,220,65,'Consultar o acervo\ndo chat')
    d.box('care',585,490,210,65,'Oferecer orientação\nfixa de cuidado')
    d.box('support',303,650,220,140,'Há apoio para\nresponder?','diamond')
    d.box('proceed',35,940,250,75,'Prosseguir para geração\ne verificação da resposta')
    d.box('lack',565,940,230,75,'Informar insuficiência\nde apoio')
    d.link('q','intent');d.link('intent','route')
    d.link('route','block',[(140,330)],'Pedido prejudicial',(180,305),'left')
    d.link('route','care',[(690,330)],'Ajuda ou cuidado',(650,305),'right')
    d.link('route','retrieve',label='Educativa',at=(475,449))
    d.link('retrieve','support')
    d.link('support','proceed',[(160,720)],'Sim',(205,704),'left')
    d.link('support','lack',[(680,720)],'Não',(640,704),'right')
    ds.append(d)

    d=Diagram('03_Arquitetura_GuardKids','03 Arquitetura do GuardKids')
    d.group('g1',250,125,340,130,'Entrada')
    d.group('g2',250,280,340,280,'Processamento com fontes')
    d.group('g3',250,585,340,280,'Verificação e entrega')
    d.box('q',290,40,250,50,'Pergunta + chat escolhido')
    d.box('input',290,165,250,65,'Proteção de entrada')
    d.box('retrieve',290,330,250,65,'Recuperação no acervo\ndo chat')
    d.box('gen',290,465,250,65,'Geração com fontes\ne estilo escolhido')
    d.box('index',30,330,180,65,'Índice vetorial','cylinder')
    d.box('style',30,465,180,65,'Direto /\nPasso a passo')
    d.box('ground',290,625,250,65,'Verificação de sustentação')
    d.box('output',290,775,250,65,'Proteção de saída')
    d.box('care',615,165,175,65,'Bloqueio ou orientação\nde cuidado')
    d.box('lack',615,625,175,65,'Informar insuficiência\nde apoio')
    d.box('record',290,940,250,60,'Persistência do registro')
    d.box('answer',290,1060,250,55,'Mensagem ao usuário')
    for a,b in [('q','input'),('input','retrieve'),('retrieve','gen'),('gen','ground'),('ground','output'),('output','record'),('record','answer')]:d.link(a,b)
    d.link('index','retrieve',start='right',end='left')
    d.link('style','gen',start='right',end='left')
    d.link('input','care',start='right',end='left')
    d.link('output','care',[(600,807.5),(600,270),(702.5,270)],start='right',end='bottom')
    d.link('ground','lack',start='right',end='left')
    d.link('retrieve','lack',[(607,362.5),(607,657.5)],start='right',end='left')
    d.link('gen','lack',[(565,497.5),(565,710),(702.5,710)],start='right',end='bottom')
    d.link('care','record',[(805,197.5),(805,970)],start='right',end='right')
    d.link('lack','record',[(805,657.5),(805,970)],start='right',end='right')
    ds.append(d)

    d=Diagram('04_Desenho_da_pesquisa','04 Desenho da pesquisa',True)
    for key,x,title in [('hist',45,'Histórico'),('dev',425,'Desenvolvimento atual'),('final',805,'Avaliação final')]:d.box(key,x,45,300,40,title,bold=True)
    d.box('pilot',85,135,220,85,'Piloto\n22 execuções')
    d.box('science',85,275,220,110,'Dois lotes de Ciências\n108 execuções\n27 perguntas reutilizadas')
    d.box('cases',465,135,220,135,'16 perguntas\n2 estilos\n32 tentativas executadas')
    d.box('review',465,345,220,80,'Inspeção preliminar\ndas respostas')
    d.box('reserve',845,135,220,135,'32 perguntas\n16 famílias\n2 estilos\n64 tentativas planejadas')
    d.box('human',845,345,220,80,'Ratificação humana\ne congelamento')
    d.box('after',845,500,220,80,'Execução e revisão\nPlanejadas')
    d.link('cases','review');d.link('reserve','human',dashed=True);d.link('human','after',dashed=True)
    d.box('note',180,680,810,50,'Conjuntos distintos. Os denominadores não devem ser somados.',font=13)
    ds.append(d)

    d=Diagram('05_Processamento_da_pergunta','05 Processamento de uma pergunta')
    for key,y,text in [('input',60,'Proteção de entrada'),('retrieve',180,'Recuperação'),('gen',300,'Geração'),('ground',420,'Verificação de sustentação'),('output',540,'Proteção de saída')]:d.box(key,285,y,250,60,text)
    d.box('care',20,360,200,60,'Bloqueio ou orientação\nde cuidado')
    d.box('lack',600,360,185,60,'Informar insuficiência\nde apoio')
    d.box('error',20,560,200,70,'Falha em qualquer etapa:\ntentativa não concluída')
    d.box('answer',285,680,250,60,'Resposta com fontes')
    d.box('record',285,820,250,55,'Tentar persistir o registro')
    d.box('saved',285,930,250,120,'Registro\ngravado?','diamond')
    d.box('display',285,1090,250,50,'Exibir mensagem')
    d.box('retain',600,1025,185,70,'Reter resposta e\nretornar erro de\npersistência')
    for a,b in [('input','retrieve'),('retrieve','gen'),('gen','ground'),('ground','output'),('output','answer'),('answer','record'),('record','saved')]:d.link(a,b)
    d.link('saved','display',label='Sim',at=(450,1077))
    d.link('saved','retain',[(570,990),(570,1060)],'Não',(570,974),'right','left')
    d.link('input','care',[(120,90)],'Risco',(176,180),'left')
    d.link('output','care',[(240,570),(240,390)],start='left',end='right')
    d.link('retrieve','lack',[(590,210),(590,390)],'Sem apoio',(656,266),'right','left')
    d.link('ground','lack',[(570,450),(570,390)],start='right',end='left')
    d.link('gen','lack',[(550,330),(550,390)],start='right',end='left')
    d.link('care','record',[(120,450),(10,450),(10,847.5)],start='bottom',end='left')
    d.link('error','record',[(10,595),(10,847.5)],start='left',end='left')
    d.link('lack','record',[(805,390),(805,847.5)],start='right',end='right')
    ds.append(d)

    d=Diagram('06_Preparacao_e_consulta','06 Preparação e consulta do acervo',True)
    d.group('prep',45,45,465,655,'Preparação do acervo')
    d.group('query',660,45,465,655,'Consulta')
    for key,y,h,text in [('sources',110,65,'Fontes + manifesto'),('extract',225,60,'Extração e seleção'),('chunk',330,50,'Segmentação'),('embed',425,60,'Embeddings BGE-M3'),('index',545,90,'Índice vetorial\nTrechos, metadados e hashes')]:d.box(key,135,y,290,h,text,'cylinder' if key=='index' else 'box')
    for a,b in [('sources','extract'),('extract','chunk'),('chunk','embed'),('embed','index')]:d.link(a,b)
    for key,y,h,text in [('q',110,60,'Pergunta + chat escolhido'),('valid',215,60,'Validar o índice'),('qembed',320,60,'Embedding da pergunta'),('select',430,100,'Comparar vetores e filtrar o chat\nAté 3 trechos\nSimilaridade mínima: 0,45'),('context',590,60,'Contexto ao gerador')]:d.box(key,735,y,290,h,text)
    for a,b in [('q','valid'),('valid','qembed'),('qembed','select'),('select','context')]:d.link(a,b)
    d.link('index','valid',[(585,590),(585,245)],start='right',end='left',dashed=True)
    d.box('note',145,735,880,45,'Acervo: 5 recortes de Ciências e 3 sínteses experimentais. Sem trechos: informar insuficiência.',font=13)
    ds.append(d)

    d=Diagram('07_Regra_de_protecao','07 Regra de proteção comum')
    d.box('legend',25,25,240,115,'Cuidado fixo:\nautolesão ou privacidade;\najuda em perigo, sexual,\nofensas ou substâncias.',font=12)
    d.box('message',303,30,220,45,'Mensagem recebida')
    d.box('risk',303,110,220,100,'Exige\nproteção?','diamond')
    d.box('caretest',40,300,240,140,'Aplica-se\ncuidado fixo?','diamond')
    d.box('care',40,535,240,60,'Orientação fixa')
    d.box('block',40,695,240,60,'Bloqueio')
    d.box('retrieve',303,270,220,50,'Buscar no acervo do chat')
    d.box('support',303,370,220,100,'Há trechos\npara prosseguir?','diamond')
    d.box('gen',303,530,220,55,'Gerar e verificar\na resposta')
    d.box('approved',303,650,220,100,'Resposta\naprovada?','diamond')
    d.box('answer',303,790,220,50,'Preparar resposta\ncom fontes')
    d.box('lack',615,385,190,70,'Informar insuficiência')
    d.box('draft',615,670,190,60,'Reter rascunho')
    d.box('route',615,780,190,80,'Aplicar a rota:\nproteção, insuficiência\nou falha técnica')
    d.box('record',303,900,220,50,'Tentar persistir o registro')
    d.box('saved',303,990,220,90,'Registro\ngravado?','diamond')
    d.box('display',303,1120,220,35,'Exibir mensagem')
    d.box('failure',615,1000,190,70,'Reter resposta e\nretornar erro')
    d.link('message','risk')
    d.link('risk','caretest',[(160,160)],'Sim',(220,145),'left')
    d.link('risk','retrieve',label='Não',at=(450,245))
    d.link('caretest','care',label='Sim',at=(190,495))
    d.link('caretest','block',[(20,370),(20,725)],'Não',(42,650),'left','left')
    d.link('care','record',[(160,615),(290,615),(290,925)],start='bottom',end='left')
    d.link('block','record',[(160,780),(275,780),(275,925)],start='bottom',end='left')
    d.link('retrieve','support')
    d.link('support','lack',label='Não',at=(567,402),start='right',end='left')
    d.link('support','gen',label='Sim',at=(450,509))
    d.link('gen','approved');d.link('approved','answer',label='Sim',at=(450,777))
    d.link('approved','draft',label='Não',at=(568,684),start='right',end='left')
    d.link('draft','route')
    d.link('lack','record',[(815,420),(815,925)],start='right',end='right')
    d.link('route','record',[(815,820),(815,925)],start='right',end='right')
    d.link('answer','record');d.link('record','saved')
    d.link('saved','display',label='Sim',at=(450,1107))
    d.link('saved','failure',label='Não',at=(567,1018),start='right',end='left')
    ds.append(d)
    return ds


def export_xml(d):
    diagram=ET.Element('diagram',name=d.name,id=d.slug)
    model=ET.SubElement(diagram,'mxGraphModel',page='1',pageScale='1',pageWidth=str(d.w),pageHeight=str(d.h),grid='1',gridSize='10',shadow='0')
    root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    for key,n in d.nodes.items():
        style=BASE_STYLE+f'fontSize={n["font"]};fontStyle={1 if n["bold"] else 0};'
        if n['shape']=='diamond':style+='rhombus;'
        elif n['shape']=='cylinder':style+='shape=cylinder3;boundedLbl=1;size=12;'
        elif n['shape']=='group':style+='fillColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingTop=7;'
        c=ET.SubElement(root,'mxCell',id=key,parent='1',value=n['label'].replace('\n','<br>'),style=style,vertex='1')
        ET.SubElement(c,'mxGeometry',x=str(n['x']),y=str(n['y']),width=str(n['w']),height=str(n['h']),attrib={'as':'geometry'})
    ports={'top':(0.5,0),'bottom':(0.5,1),'left':(0,0.5),'right':(1,0.5)}
    for i,e in enumerate(d.edges):
        ex,ey=ports[e['start']];ix,iy=ports[e['end']]
        style=f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;strokeWidth=1;startArrow=none;endArrow=classic;exitX={ex};exitY={ey};entryX={ix};entryY={iy};'
        if e['dashed']:style+='dashed=1;'
        c=ET.SubElement(root,'mxCell',id=f'edge{i}',parent='1',source=e['a'],target=e['b'],edge='1',style=style)
        geo=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if len(e['path'])>2:
            a=ET.SubElement(geo,'Array',attrib={'as':'points'})
            for x,y in e['path'][1:-1]:ET.SubElement(a,'mxPoint',x=str(x),y=str(y))
        if e['label']:
            x,y=label_pos(e)
            c=ET.SubElement(root,'mxCell',id=f'label{i}',parent='1',value=e['label'],vertex='1',style='text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=12;fillColor=#FFFFFF;strokeColor=none;')
            ET.SubElement(c,'mxGeometry',x=str(x-70),y=str(y-13),width='140',height='25',attrib={'as':'geometry'})
    return diagram


def label_pos(e):
    if e['at']:return e['at']
    a,b=e['path'][0],e['path'][-1]
    return ((a[0]+b[0])/2+30,(a[1]+b[1])/2)


def lines(label,width,font,size):
    result=[]
    for paragraph in label.split('\n'):
        line=''
        for word in paragraph.split():
            new=(line+' '+word).strip()
            if line and pdfmetrics.stringWidth(new,font,size)>width:result.append(line);line=word
            else:line=new
        result.append(line)
    return result


def render(c,d):
    scale=.72
    c.setPageSize((d.w*scale,d.h*scale));c.saveState();c.scale(scale,scale)
    c.setStrokeColorRGB(0,0,0);c.setFillColorRGB(1,1,1);c.setLineWidth(1)
    def text(n):
        font='U-Bold' if n['bold'] else 'U';size=n['font']
        ls=lines(n['label'],n['w']-16 if n['shape']!='diamond' else n['w']*.76,font,size)
        lh=size*1.3
        if len(ls)*lh>n['h']-8:raise ValueError('Texto não cabe: '+n['label'])
        c.setFont(font,size);c.setFillColorRGB(0,0,0)
        if n['shape']=='group':
            c.drawString(n['x']+8,d.h-n['y']-19,n['label']);return
        y=n['y']+(n['h']-len(ls)*lh)/2+size
        for i,t in enumerate(ls):c.drawCentredString(n['x']+n['w']/2,d.h-y-i*lh,t)
    for n in d.nodes.values():
        if n['shape']=='group':c.rect(n['x'],d.h-n['y']-n['h'],n['w'],n['h'],fill=0,stroke=1);text(n)
    for e in d.edges:
        c.setDash(5,4) if e['dashed'] else c.setDash()
        p=c.beginPath();p.moveTo(e['path'][0][0],d.h-e['path'][0][1])
        for x,y in e['path'][1:]:p.lineTo(x,d.h-y)
        c.drawPath(p);c.setDash()
        a,b=e['path'][-2:];angle=math.atan2(b[1]-a[1],b[0]-a[0]);p=c.beginPath();p.moveTo(b[0],d.h-b[1])
        for side in [-1,1]:p.lineTo(b[0]-9*math.cos(angle)+side*3.5*math.sin(angle),d.h-(b[1]-9*math.sin(angle)-side*3.5*math.cos(angle)))
        p.close();c.setFillColorRGB(0,0,0);c.drawPath(p,fill=1,stroke=0)
    for n in d.nodes.values():
        if n['shape']=='group':continue
        x,y,w,h=n['x'],n['y'],n['w'],n['h'];c.setFillColorRGB(1,1,1)
        c.setDash(5,4) if n.get('dashed') else c.setDash()
        if n['shape']=='diamond':
            p=c.beginPath();p.moveTo(x+w/2,d.h-y)
            for px,py in [(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)]:p.lineTo(px,d.h-py)
            p.close();c.drawPath(p,fill=1,stroke=1)
        elif n['shape']=='cylinder':
            c.rect(x,d.h-y-h+8,w,h-16,fill=1,stroke=0)
            c.line(x,d.h-y-8,x,d.h-y-h+8);c.line(x+w,d.h-y-8,x+w,d.h-y-h+8)
            c.ellipse(x,d.h-y-16,x+w,d.h-y,fill=1,stroke=1)
            p=c.beginPath();p.moveTo(x,d.h-y-h+8);p.curveTo(x,d.h-y-h-3,x+w,d.h-y-h-3,x+w,d.h-y-h+8);c.drawPath(p)
        else:c.rect(x,d.h-y-h,w,h,fill=1,stroke=1)
        c.setDash();text(n)
    for e in d.edges:
        if e['label']:
            x,y=label_pos(e);size=12;w=pdfmetrics.stringWidth(e['label'],'U',size)
            c.setFillColorRGB(1,1,1);c.rect(x-w/2-4,d.h-y-4,w+8,18,fill=1,stroke=0)
            c.setFillColorRGB(0,0,0);c.setFont('U',size);c.drawCentredString(x,d.h-y,e['label'])
    c.restoreState()


def import_first():
    source=ROOT/'diagramas/revisao_usuario/Problema_de_pesquisa_corrigido.drawio'
    element=deepcopy(ET.parse(source).getroot().find('diagram'))
    element.set('name','01 Problema de pesquisa');element.set('id','01_problema')
    model=element.find('mxGraphModel');d=Diagram('01_Problema_de_pesquisa','01 Problema de pesquisa',True)
    for el in model.find('root'):
        if el.get('vertex')!='1':continue
        g=el.find('mxGeometry');style=el.get('style','')
        key=d.box(el.get('id'),float(g.get('x',0)),float(g.get('y',0)),float(g.get('width')),float(g.get('height')),
              unescape(re.sub('<[^>]+>',' ',el.get('value',''))),bold='fontStyle=1' in style,font=12)
        d.nodes[key]['dashed']='dashed=1' in style
    for el in model.find('root'):
        if el.get('edge')=='1':d.link(el.get('source'),el.get('target'))
    return d,element


def main():
    pdfmetrics.registerFont(TTFont('U','C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('U-Bold','C:/Windows/Fonts/arialbd.ttf'))
    OUT.mkdir(exist_ok=True)
    first,first_xml=import_first();all_ds=[first,*diagrams()]
    combined=ET.Element('mxfile',host='app.diagrams.net')
    book=ROOT/'output/pdf/Diagramas_GuardKids_preto_e_branco.pdf';c=canvas.Canvas(str(book));c.setTitle('GuardKids - Diagramas em preto e branco')
    for d in all_ds:
        for n in d.nodes.values():
            assert 0<=n['x'] and 0<=n['y'] and n['x']+n['w']<=d.w and n['y']+n['h']<=d.h
        diagram=first_xml if d is first else export_xml(d)
        combined.append(deepcopy(diagram))
        single=ET.Element('mxfile',host='app.diagrams.net');single.append(deepcopy(diagram))
        ET.ElementTree(single).write(OUT/(d.slug+'.drawio'),encoding='utf-8',xml_declaration=True)
        render(c,d);c.showPage()
        p=canvas.Canvas(str(OUT/(d.slug+'.pdf')));p.setTitle(d.name);render(p,d);p.save()
    c.save();ET.ElementTree(combined).write(OUT/'GuardKids_7_diagramas.drawio',encoding='utf-8',xml_declaration=True)
    (OUT/'LEIA-ME.txt').write_text('Abra GuardKids_7_diagramas.drawio no Draw.io: há sete abas, uma por desenho.\nOs arquivos numerados permitem abrir ou imprimir cada diagrama separadamente.\nO primeiro desenho é a versão corrigida do autor; os outros seis seguem seu estilo.\nCada aba tem formato de página adequado ao desenho. Não juntar as sete abas em uma área única.\nEste pacote não substitui automaticamente as figuras do manuscrito.\n',encoding='utf-8')
    with zipfile.ZipFile(OUT/'GuardKids_diagramas_editaveis.zip','w',zipfile.ZIP_DEFLATED) as z:
        for d in all_ds:
            for ext in ['drawio','pdf']:z.write(OUT/(d.slug+'.'+ext),d.slug+'.'+ext)
        z.write(OUT/'GuardKids_7_diagramas.drawio','GuardKids_7_diagramas.drawio')
        z.write(OUT/'LEIA-ME.txt','LEIA-ME.txt')
    print('Sete abas e sete PDFs individuais, com um desenho por página. Primeiro desenho do autor preservado.')


if __name__=='__main__':main()
