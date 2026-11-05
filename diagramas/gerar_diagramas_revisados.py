"""Diagramas originais GuardKids: SVG, PDF vetorial e Draw.io da mesma especificação.

Usa organização por planos e camadas inspirada nas referências fornecidas,
mantendo exclusivamente os componentes e evidências do GuardKids GK-P2.1-dev.
"""
from pathlib import Path
from dataclasses import dataclass, field
from html import escape
import json
import math
import zipfile
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "diagramas"
INK = "#20364a"
MUTED = "#536574"
BLUE = ("#eef4fb", "#426b95")
TEAL = ("#edf6f2", "#367260")
AMBER = ("#fff6e8", "#9c702e")
RED = ("#fbeeee", "#a14b4b")
GRAY = ("#f4f5f6", "#73808c")
PURPLE = ("#f3eff8", "#78628f")


@dataclass
class Figure:
    slug: str
    title: str
    subtitle: str
    h: int = 800
    nodes: list = field(default_factory=list)
    groups: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def node(self, key, x, y, w, h, title, body=(), color=BLUE, shape="box"):
        self.nodes.append(dict(id=key, x=x, y=y, w=w, h=h, title=title,
                               body=list(body), color=color, shape=shape))
        return key

    def group(self, x, y, w, h, title, color=GRAY):
        self.groups.append(dict(x=x,y=y,w=w,h=h,title=title,color=color))

    def path(self, points, label="", at=None, dashed=False, color=INK):
        self.edges.append(dict(points=points,label=label,at=at,dashed=dashed,color=color))

    def link(self, a, b, label="", dashed=False):
        src=next(n for n in self.nodes if n["id"]==a)
        dst=next(n for n in self.nodes if n["id"]==b)
        sx,sy=src['x']+src['w']/2,src['y']+src['h']/2
        tx,ty=dst['x']+dst['w']/2,dst['y']+dst['h']/2
        if abs(tx-sx)>abs(ty-sy):
            direction=1 if tx>sx else -1
            p=[(sx+direction*src['w']/2,sy),(tx-direction*dst['w']/2,ty)]
        else:
            direction=1 if ty>sy else -1
            p=[(sx,sy+direction*src['h']/2),(tx,ty-direction*dst['h']/2)]
        self.path(p,label,dashed=dashed)

    def note(self,y,text):
        self.notes.append((y,text))


def specs():
    fs=[]
    f=Figure("01_dilema_calibracao_guardrails","Proteção contextual e atendimento educativo",
             "O problema de pesquisa: a mesma palavra pode aparecer em intenções diferentes.",650)
    for x,key,title,body,color in [
        (40,'open','1  Permissividade', ['Resposta fluente não basta.','Um pedido prejudicial pode','receber instruções de dano.','Risco: liberação inadequada.'],RED),
        (360,'closed','2  Restrição excessiva',['Palavra sensível não basta.','Uma dúvida escolar pode','ser recusada sem necessidade.','Risco: bloqueio indevido.'],AMBER),
        (680,'context','3  Leitura contextual',['Examinar intenção e contexto.','Distinguir educação e risco.','Oferecer cuidado na ajuda.','Conferir apoio nas fontes.'],TEAL)]:
        f.node(key,x,150,280,230,title,body,color)
    f.node('question',110,445,780,95,'Avaliar dimensões separadas',
           ['Segurança  |  Tratamento  |  Correção  |  Sustentação  |  Clareza'],BLUE)
    for x in [180,500,820]:f.path([(x,380),(x,415),(500,415),(500,445)])
    f.note(595,'Quadro conceitual. As três situações não são condições experimentais da POC atual.')
    fs.append(f)

    f=Figure('02_fluxo_classificacao_indicativa','Da referência de risco à decisão contextual',
             'Descritores orientam a análise; a decisão depende também da intenção e do apoio documental.',730)
    f.group(30,120,285,470,'A  REFERÊNCIAS',GRAY)
    f.group(355,120,285,470,'B  CONTEXTO',BLUE)
    f.group(680,120,290,470,'C  TRATAMENTO',TEAL)
    f.node('refs',50,195,245,270,'Categorias de cuidado',
           ['Perigo e autolesão','Sexual e ofensas','Substâncias e privacidade','Injeção de instruções','Guia ClassInd e literatura'],GRAY)
    f.node('context',375,195,245,270,'Leitura da solicitação',
           ['O que a pessoa pretende?','Pede dano ou pede ajuda?','É uma dúvida educativa?','Qual é o chat escolhido?','O acervo pode responder?'],BLUE)
    f.node('care',700,180,250,95,'Intervir',['Bloqueio ou cuidado fixo'],RED)
    f.node('edu',700,310,250,95,'Prosseguir',['Gerar e verificar a resposta'],TEAL)
    f.node('lack',700,440,250,95,'Comunicar limite',['Falta de apoio no acervo'],AMBER)
    f.link('refs','context')
    f.path([(620,330),(657,330),(657,227),(700,227)])
    f.path([(657,330),(657,357),(700,357)])
    f.path([(657,357),(657,487),(700,487)])
    f.note(640,'A referência classificatória não representa uma classificação oficial do chatbot.')
    f.note(674,'Perfil operacional: nove anos fictícios. A adequação à faixa de 7-11 anos não foi demonstrada.')
    fs.append(f)

    f=Figure('03_arquitetura_conceitual_integrada','Arquitetura do GuardKids por camadas',
             'Regra comum nos quatro chats; apenas o estilo da explicação varia entre condições.',820)
    f.node('request',50,105,900,72,'Contexto da tentativa',
           ['Pergunta + chat  |  Perfil fictício de 9 anos  |  Regra comum  |  Direto ou Passo a passo'],GRAY)
    f.group(35,190,930,230,'A  ENTRADA, BUSCA E GERAÇÃO',GRAY)
    f.group(35,435,930,230,'B  VERIFICAÇÃO E ENTREGA',GRAY)
    cards=[
        ('input',50,235,'1  Proteção de entrada',['Detector parcial de dados','Classificação de intenção','Intervenção tem precedência'],BLUE),
        ('retrieve',370,235,'2  Recuperação no chat',['Índice validado: 8 trechos','Embeddings com BGE-M3','Até 3 trechos; limiar 0,45'],BLUE),
        ('generate',690,235,'3  Geração com fontes',['Qwen3:8b + estilo escolhido','Resposta estruturada','Limite de 120 palavras'],TEAL),
        ('ground',690,470,'4  Apoio documental',['Conferir IDs e extensão','Detector parcial de dados','Verificação de sustentação'],PURPLE),
        ('output',370,470,'5  Proteção de saída',['Classificar o texto gerado','Aplicar a regra comum','Reter rascunho reprovado'],BLUE),
        ('record',50,470,'6  Registro da tentativa',['Persistência antes da saída','Comum: texto minimizado','Fictício: registro integral'],GRAY)]
    for key,x,y,t,b,c in cards:f.node(key,x,y+10 if y==235 else y+20,260,160,t,b,c)
    f.path([(180,177),(180,245)])
    for a,b in [('input','retrieve'),('retrieve','generate'),('generate','ground'),('ground','output'),('output','record')]:f.link(a,b)
    f.node('answer',50,690,900,66,'Mensagem exibida',['Explicação com fontes, cuidado, recusa ou aviso de apoio insuficiente'],TEAL)
    f.path([(180,650),(180,690)])
    f.note(790,'Caminho completo: até quatro chamadas ao mesmo Qwen3. Intervenções podem encerrar antes.')
    fs.append(f)

    f=Figure('04_protocolo_experimental_metodologia','Desenho de pesquisa e separação das evidências',
             'Os denominadores pertencem a etapas distintas e não devem ser somados.',800)
    columns=[
        (30,'A  HISTÓRICO',GRAY,[('h1','Piloto de outubro',['22 execuções preservadas','Condições anteriores']),('h2','Dois lotes de Ciências',['108 execuções no total','27 perguntas reutilizadas']),('h3','Uso das evidências',['Descrever falhas e versões','Sem integrar o lote atual'])]),
        (355,'B  DESENVOLVIMENTO',BLUE,[('d1','Regra comum + estilos',['16 perguntas conhecidas','32 tentativas executadas']),('d2','Inspeção assistida por IA',['5 de 8 explicações com','ressalvas de sustentação']),('d3','Limite da interpretação',['Campos humanos vazios','Sem eficácia demonstrada'])]),
        (680,'C  AVALIAÇÃO FINAL',TEAL,[('f1','Reserva operacional',['32 perguntas / 16 famílias','64 tentativas planejadas']),('f2','Antes da execução',['Ratificação humana','Congelamento da versão']),('f3','Depois da execução',['Revisão por dimensão','Comparação pareada'])])]
    for x,title,color,nodes in columns:
        f.group(x,120,290,520,title,color)
        for i,(key,t,b) in enumerate(nodes):f.node(key,x+15,190+145*i,260,100,t,b,color)
        f.link(nodes[0][0],nodes[1][0]);f.link(nodes[1][0],nodes[2][0])
    f.node('fixed',50,680,900,66,'O que a comparação atual modifica?',
           ['Somente a instrução de linguagem. Perfil, regra, fontes e modelo permanecem iguais.'],PURPLE)
    f.note(782,'A avaliação final não foi executada. A reserva é conhecida pelos autores e não é independente.')
    fs.append(f)

    f=Figure('05_pipeline_5_etapas_guardkids','Fluxo de uma pergunta e saídas alternativas',
             'Cinco etapas de processamento, com encerramentos distintos e registro obrigatório.',770)
    labels=[('in','1  Entrada',['Dados pessoais','Intenção e risco'],BLUE),('rag','2  Recuperação',['Filtrar o chat','Buscar trechos'],BLUE),
            ('gen','3  Geração',['Fontes + estilo','JSON e limite'],TEAL),('ground','4  Sustentação',['Conferir fontes','e afirmações'],PURPLE),('out','5  Saída',['Segurança do','texto gerado'],BLUE)]
    for i,(key,t,b,c) in enumerate(labels):f.node(key,30+190*i,165,178,160,t,b,c)
    for a,b in zip(labels,labels[1:]):f.link(a[0],b[0])
    f.node('care',40,455,280,100,'Proteção aplicada',['Bloqueio ou orientação fixa'],RED)
    f.node('lack',360,455,280,100,'Apoio insuficiente',['Comunicar o limite do acervo'],AMBER)
    f.node('error',680,455,280,100,'Falha técnica',['Erro em qualquer etapa','Preservar a tentativa perdida'],GRAY)
    f.path([(119,325),(119,455)],'risco',at=(150,393),color=RED[1])
    f.path([(309,325),(309,380),(500,380),(500,455)],'sem apoio',at=(506,400),color=AMBER[1])
    f.path([(689,325),(689,380),(590,380),(590,455)],color=AMBER[1])
    f.path([(879,325),(879,375),(980,375),(980,595),(920,595),(920,625)],'aprovada',at=(890,603),color=TEAL[1])
    f.node('persist',40,625,920,70,'Persistir antes de exibir qualquer mensagem',
           ['Falha de gravação retém a resposta. Rascunhos rejeitados não são enviados à interface.'],GRAY)
    for x in [180,500,820]:f.path([(x,555),(x,625)])
    f.note(738,'O caminho aprovado libera a explicação com fontes após a etapa 5 e a persistência.')
    fs.append(f)

    f=Figure('06_curadoria_e_indexacao_rag','Acervo rastreável e recuperação por chat',
             'Preparação do índice separada do processamento de uma pergunta.',850)
    f.group(30,120,435,620,'A  PREPARAÇÃO DO ACERVO',GRAY)
    f.group(535,120,435,620,'B  CONSULTA EM EXECUÇÃO',BLUE)
    left=[('source','Fontes e manifesto',['5 recortes de Ciências','3 sínteses experimentais']),('chunk','Seleção e segmentação',['Âncoras e exclusões nos PDFs','Blocos de até 850 caracteres']),('embed','Embeddings dos trechos',['BGE-M3; vetores normalizados','Metadados e hashes']),('publish','Publicação do índice',['Vetores + trechos completos','Troca do ponteiro de versão'])]
    right=[('validate','Validar a versão do índice',['Fontes, texto, hashes e modelo','Dimensões e normalização']),('filter','Filtrar o chat escolhido',['Pergunta e acervo do chat','Embedding da pergunta']),('rank','Ordenar por similaridade',['Até 3 trechos acima de 0,45','Similaridade não prova apoio']),('context','Contexto para o gerador',['Trechos e IDs das fontes','Sem trechos: informar limite'])]
    for x,series,col in [(55,left,GRAY),(560,right,BLUE)]:
        for i,(key,t,b) in enumerate(series):f.node(key,x,180+135*i,385,92,t,b,col)
        for a,b in zip(series,series[1:]):f.link(a[0],b[0])
    f.path([(440,631),(500,631),(500,226),(560,226)],dashed=True)
    f.note(790,'As sínteses receberam conferência documental assistida por IA; a revisão humana está pendente.')
    f.note(824,'Não há busca híbrida, re-ranking ou memória de sessão implementados nesta versão.')
    fs.append(f)

    f=Figure('07_regra_protecao_comum','Regra de proteção comum: precedência e decisões',
             'A mesma regra vale para Ciências, História, Geografia e Geral.',980)
    f.node('q',390,110,270,65,'Pergunta validada',[],GRAY)
    f.node('criterion',45,100,265,110,'Critério de cuidado',['Autolesão ou privacidade;','perigo, sexual, ofensas ou','substâncias, se pedir ajuda'],GRAY)
    f.node('risk',400,230,250,110,'Exige', ['proteção?'],BLUE,'diamond')
    f.node('caretest',45,230,265,110,'Cuidado fixo', ['aplicável?'],BLUE,'diamond')
    f.node('care',45,420,265,80,'Orientar cuidado',['Mensagem fixa por categoria'],TEAL)
    f.node('block',45,590,265,80,'Bloquear pedido',['Recusa do pedido nocivo'],RED)
    f.node('retrieve',400,410,250,110,'Há trechos', ['no chat?'],BLUE,'diamond')
    f.node('lack',745,425,215,80,'Informar limite',['Apoio insuficiente'],AMBER)
    f.node('generate',400,580,250,90,'Gerar e conferir',['Fontes, estilo e segurança'],PURPLE)
    f.node('approve',400,730,250,100,'Resposta', ['aprovada?'],BLUE,'diamond')
    f.node('reject',735,685,235,180,'Se houver reprovação',
           ['Sem apoio: informar limite','Risco: aplicar proteção','Erro: registrar perda','Reter o rascunho'],AMBER)
    f.node('final',400,885,250,65,'Registrar e exibir',['Resposta com fontes'],TEAL)
    f.node('fixed',45,885,265,65,'Registrar e exibir',['Mensagem fixa'],GRAY)
    f.node('other',735,885,235,65,'Registrar e exibir',['Mensagem da rota'],GRAY)
    f.link('q','risk');f.link('risk','caretest','sim');f.link('risk','retrieve','não')
    f.path([(177,340),(177,420)],'sim',at=(207,388))
    f.path([(45,285),(20,285),(20,630),(45,630)],'não',at=(40,560))
    f.path([(177,500),(177,550),(335,550),(335,850),(177,850),(177,885)])
    f.path([(177,670),(177,885)])
    f.link('retrieve','lack','não');f.link('retrieve','generate','sim');f.link('generate','approve')
    f.link('approve','reject','não');f.link('approve','final','sim')
    f.link('reject','other')
    f.path([(960,465),(985,465),(985,917),(970,917)])
    f.note(970,'Predação educativa não gráfica pode prosseguir; risco, falta de apoio e falha técnica são distintos.')
    fs.append(f)
    return fs


def svg(f):
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{f.h}" viewBox="0 0 1000 {f.h}">',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#20364a"/></marker></defs>',
           '<rect width="1000" height="100%" fill="white"/>']
    def text(x,y,t,size=18,bold=False,color=INK,anchor='middle'):
        parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{color}">{escape(t)}</text>')
    text(500,38,f.title,28,True);text(500,76,f.subtitle,17,color=MUTED)
    for a in f.groups:
        parts.append(f'<rect x="{a["x"]}" y="{a["y"]}" width="{a["w"]}" height="{a["h"]}" rx="9" fill="{a["color"][0]}" stroke="{a["color"][1]}" stroke-dasharray="6 5"/>')
        text(a['x']+a['w']/2,a['y']+35,a['title'],20,True)
    for e in f.edges:
        p=' '.join(f'{x},{y}' for x,y in e['points'])
        dash=' stroke-dasharray="6 5"' if e['dashed'] else ''
        parts.append(f'<polyline points="{p}" fill="none" stroke="{e["color"]}" stroke-width="2" marker-end="url(#arrow)"{dash}/>')
    for n in f.nodes:
        x,y,w,h=n['x'],n['y'],n['w'],n['h'];fill,stroke=n['color']
        if n['shape']=='diamond':
            pts=f'{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}'
            parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
        else:parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
        title_y,body_y=node_text_y(n)
        text(x+w/2,title_y,n['title'],20,True)
        for i,t in enumerate(n['body']):text(x+w/2,body_y+25*i,t,18)
    for e in f.edges:
        if e['label']:
            x,y=label_position(e);w=pdfmetrics.stringWidth(e['label'],'GK',17)+14
            parts.append(f'<rect x="{x-w/2}" y="{y-17}" width="{w}" height="23" rx="3" fill="white"/>')
            text(x,y,e['label'],17,color=e['color'])
    for y,t in f.notes:text(500,y,t,17,color=MUTED)
    parts.append('</svg>')
    return '\n'.join(parts)


def node_text_y(n):
    if n['shape']=='diamond':
        return n['y']+n['h']/2-5,n['y']+n['h']/2+22
    total=24+len(n['body'])*25+(6 if n['body'] else 0)
    top=n['y']+(n['h']-total)/2
    return top+20,top+50


def label_position(e):
    if e['at']:return e['at']
    p,q=e['points'][0],e['points'][-1]
    return ((p[0]+q[0])/2+16,(p[1]+q[1])/2-8)


def paint(c,f):
    def line_text(x,y,t,size=18,bold=False,color=INK):
        c.setFillColor(color);c.setFont('GK-Bold' if bold else 'GK',size);c.drawCentredString(x,f.h-y,t)
    c.setFillColor('white');c.rect(0,0,1000,f.h,fill=1,stroke=0)
    line_text(500,38,f.title,28,True);line_text(500,76,f.subtitle,17,color=MUTED)
    for a in f.groups:
        c.setFillColor(a['color'][0]);c.setStrokeColor(a['color'][1]);c.setDash(6,5);c.setLineWidth(1)
        c.roundRect(a['x'],f.h-a['y']-a['h'],a['w'],a['h'],9,fill=1,stroke=1);c.setDash()
        line_text(a['x']+a['w']/2,a['y']+35,a['title'],20,True)
    for e in f.edges:
        c.setStrokeColor(e['color']);c.setFillColor(e['color']);c.setLineWidth(2)
        c.setDash(6,5) if e['dashed'] else c.setDash()
        p=c.beginPath();p.moveTo(e['points'][0][0],f.h-e['points'][0][1])
        for x,y in e['points'][1:]:p.lineTo(x,f.h-y)
        c.drawPath(p);c.setDash()
        (ax,ay),(bx,by)=e['points'][-2:];angle=math.atan2(by-ay,bx-ax)
        tip=c.beginPath();tip.moveTo(bx,f.h-by)
        for side in [-1,1]:
            x=bx-10*math.cos(angle)+side*4*math.sin(angle);y=by-10*math.sin(angle)-side*4*math.cos(angle)
            tip.lineTo(x,f.h-y)
        tip.close();c.drawPath(tip,fill=1,stroke=0)
    for n in f.nodes:
        x,y,w,h=n['x'],n['y'],n['w'],n['h'];c.setFillColor(n['color'][0]);c.setStrokeColor(n['color'][1]);c.setLineWidth(1.8)
        if n['shape']=='diamond':
            p=c.beginPath();p.moveTo(x+w/2,f.h-y)
            for px,py in [(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)]:p.lineTo(px,f.h-py)
            p.close();c.drawPath(p,fill=1,stroke=1)
        else:c.roundRect(x,f.h-y-h,w,h,7,fill=1,stroke=1)
        ty,by=node_text_y(n);line_text(x+w/2,ty,n['title'],20,True)
        for i,t in enumerate(n['body']):line_text(x+w/2,by+25*i,t,18)
    for e in f.edges:
        if e['label']:
            x,y=label_position(e);w=pdfmetrics.stringWidth(e['label'],'GK',17)+14
            c.setFillColor('white');c.roundRect(x-w/2,f.h-y-6,w,23,3,fill=1,stroke=0)
            line_text(x,y,e['label'],17,color=e['color'])
    for y,t in f.notes:line_text(500,y,t,17,color=MUTED)


def endpoint_node(f,point):
    px,py=point
    for n in f.nodes:
        x,y,w,h=n['x'],n['y'],n['w'],n['h']
        if n['shape']=='diamond':
            on=abs(abs(px-(x+w/2))/(w/2)+abs(py-(y+h/2))/(h/2)-1)<0.001
        else:
            on=((abs(px-x)<0.01 or abs(px-x-w)<0.01) and y<=py<=y+h) or ((abs(py-y)<0.01 or abs(py-y-h)<0.01) and x<=px<=x+w)
        if on:return n
    return None


def drawio(f,index):
    out=[f'<diagram id="gk-{index}" name="{escape(f.title)}"><mxGraphModel page="1" pageWidth="1000" pageHeight="{f.h}" grid="1"><root><mxCell id="0"/><mxCell id="1" parent="0"/>']
    def cell(key,x,y,w,h,value,style,parent='1'):
        out.append(f'<mxCell id="{key}" value="{escape(value,quote=True)}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    cell('title',20,8,960,40,f.title,'text;html=1;align=center;fontSize=28;fontStyle=1;fontColor='+INK+';')
    cell('subtitle',20,48,960,42,f.subtitle,'text;html=1;align=center;fontSize=17;fontColor='+MUTED+';')
    for i,g in enumerate(f.groups):
        cell(f'group{i}',g['x'],g['y'],g['w'],g['h'],g['title'],f'container=1;collapsible=0;rounded=1;dashed=1;fillColor={g["color"][0]};strokeColor={g["color"][1]};verticalAlign=top;spacingTop=12;fontSize=20;fontStyle=1;')
    for i,e in enumerate(f.edges):
        # Pontos explícitos preservam a mesma rota do SVG e do PDF; conectores editáveis.
        pts=e['points'];attached='';ports=''
        for name,point in [('source',pts[0]),('target',pts[-1])]:
            n=endpoint_node(f,point)
            if n:
                attached+=f' {name}="{n["id"]}"'
                port='exit' if name=='source' else 'entry'
                ports+=f'{port}X={(point[0]-n["x"])/n["w"]};{port}Y={(point[1]-n["y"])/n["h"]};{port}Perimeter=0;'
        out.append(f'<mxCell id="edge{i}" style="endArrow=block;endFill=1;strokeWidth=2;strokeColor={e["color"]};dashed={int(e["dashed"])};{ports}" edge="1" parent="1"{attached}><mxGeometry relative="1" as="geometry">')
        out.append(f'<mxPoint x="{pts[0][0]}" y="{pts[0][1]}" as="sourcePoint"/><mxPoint x="{pts[-1][0]}" y="{pts[-1][1]}" as="targetPoint"/>')
        if len(pts)>2:out.append('<Array as="points">'+''.join(f'<mxPoint x="{x}" y="{y}"/>' for x,y in pts[1:-1])+'</Array>')
        out.append('</mxGeometry></mxCell>')
    for n in f.nodes:
        value='<b>'+escape(n['title'])+'</b>' + ('<br><br>'+'<br>'.join(escape(t) for t in n['body']) if n['body'] else '')
        shape='rhombus;' if n['shape']=='diamond' else 'rounded=1;arcSize=8;'
        parent='1';nx,ny=n['x'],n['y']
        for i,g in enumerate(f.groups):
            if g['x']<=nx and g['y']<=ny and nx+n['w']<=g['x']+g['w'] and ny+n['h']<=g['y']+g['h']:
                parent=f'group{i}';nx-=g['x'];ny-=g['y'];break
        cell(n['id'],nx,ny,n['w'],n['h'],value,shape+f'html=1;whiteSpace=wrap;align=center;fontFamily=Arial;fontSize=18;fontColor={INK};fillColor={n["color"][0]};strokeColor={n["color"][1]};strokeWidth=1.8;',parent)
    for i,e in enumerate(f.edges):
        if e['label']:
            x,y=label_position(e);cell(f'label{i}',x-45,y-19,90,30,e['label'],'text;html=1;align=center;fontSize=17;fillColor=#ffffff;')
    for i,(y,t) in enumerate(f.notes):cell(f'note{i}',20,y-20,960,30,t,'text;html=1;align=center;fontSize=17;fontColor='+MUTED+';')
    out.append('</root></mxGraphModel></diagram>');return '\n'.join(out)


def validate(f):
    if pdfmetrics.stringWidth(f.title,'GK-Bold',28)>960:
        raise ValueError('Título excede a página')
    for n in f.nodes:
        for t,font,size in [(n['title'],'GK-Bold',20),*[(t,'GK',18) for t in n['body']]]:
            if pdfmetrics.stringWidth(t,font,size)>n['w']-18:
                raise ValueError(f'{f.slug}: texto excede caixa: {t}')
        if n['x']<0 or n['y']<0 or n['x']+n['w']>1000 or n['y']+n['h']>f.h:
            raise ValueError('Caixa fora da página')
        if n['body'] and node_text_y(n)[1]+25*(len(n['body'])-1)>n['y']+n['h']-4:
            raise ValueError('Texto excede altura da caixa')


def main():
    regular=Path('C:/Windows/Fonts/arial.ttf');bold=Path('C:/Windows/Fonts/arialbd.ttf')
    pdfmetrics.registerFont(TTFont('GK',str(regular)))
    pdfmetrics.registerFont(TTFont('GK-Bold',str(bold)))
    for folder in ['svg','drawio','pdf']: (BASE/folder).mkdir(exist_ok=True)
    figures=specs();xml=['<mxfile host="app.diagrams.net" version="24.7.17">']
    for i,f in enumerate(figures,1):
        validate(f)
        (BASE/'svg'/f'{f.slug}.svg').write_text(svg(f),encoding='utf-8')
        fragment=drawio(f,i);xml.append(fragment)
        (BASE/'drawio'/f'{f.slug}.drawio').write_text('<mxfile host="app.diagrams.net">'+fragment+'</mxfile>',encoding='utf-8')
        c=canvas.Canvas(str(BASE/'pdf'/f'{f.slug}.pdf'),pagesize=(1000,f.h));c.setTitle(f.title);paint(c,f);c.save()
    xml.append('</mxfile>');(BASE/'Todos_os_Diagramas_TCC_GuardKids.drawio').write_text('\n'.join(xml),encoding='utf-8')
    book=ROOT/'output/pdf/Diagramas_GuardKids_revisados.pdf';book.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(book),pagesize=(1000,800));c.setTitle('GuardKids - Diagramas revisados')
    for f in figures:c.setPageSize((1000,f.h));paint(c,f);c.showPage()
    c.save()
    (BASE/'indice_diagramas.json').write_text(json.dumps([dict(number=i+1,slug=f.slug,title=f.title,width=1000,height=f.h) for i,f in enumerate(figures)],ensure_ascii=False,indent=2),encoding='utf-8')
    with zipfile.ZipFile(BASE/'Diagramas_GuardKids_editaveis.zip','w',zipfile.ZIP_DEFLATED) as z:
        for folder in ['drawio','svg','pdf']:
            for f in figures:z.write(BASE/folder/f'{f.slug}.{folder if folder != "drawio" else "drawio"}',f'{folder}/{f.slug}.{folder if folder != "drawio" else "drawio"}')
        z.write(BASE/'Todos_os_Diagramas_TCC_GuardKids.drawio','Todos_os_Diagramas_TCC_GuardKids.drawio')
    print('7 diagramas em SVG, Draw.io e PDF; caderno e pacote editável gerados.')


if __name__=='__main__':main()
