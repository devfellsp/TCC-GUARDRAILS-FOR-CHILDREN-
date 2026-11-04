"""Variante com símbolos vetoriais nativos do Draw.io, sem alterar os fluxos."""
from pathlib import Path
from copy import deepcopy
import xml.etree.ElementTree as ET
import zipfile
import json
import math
import gerar_estilo_usuario as base
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=base.ROOT
OUT=ROOT/'diagramas/estilo_usuario_com_simbolos'
LIB=ET.parse(ROOT/'diagramas/recursos/gmdl_utilizados.xml').getroot()
STENCILS={s.get('name'):s for s in LIB}

# Ícones são filhos dos blocos: acompanham movimentos e continuam editáveis.
ICONS={
 '02':{'q':'chat2','intent':'search','block':'lock','retrieve':'search','care':'chat2','proceed':'component'},
 '03':{'q':'chat2','input':'lock','retrieve':'search','gen':'component','style':'document','ground':'check','output':'lock','record':'database','answer':'chat2'},
 '04':{'pilot':'document','science':'document','cases':'document','review':'search','reserve':'folder','human':'check','after':'document'},
 '05':{'input':'lock','retrieve':'search','gen':'component','ground':'check','output':'lock','answer':'document','record':'database','display':'chat2'},
 '06':{'sources':'document','extract':'document','chunk':'document','embed':'component','q':'chat2','valid':'check','qembed':'component','select':'search','context':'document'},
 '07':{'message':'chat2','care':'chat2','block':'lock','retrieve':'search','gen':'component','answer':'document','record':'database','display':'chat2'},
}


def icon_geometry(n,kind):
    w,h=24,24
    if kind in STENCILS:
        s=STENCILS[kind];ratio=float(s.get('h'))/float(s.get('w'));h=w*ratio
    return 11,(n['h']-h)/2,w,h


def cell(root,key,parent,style,x,y,w,h):
    e=ET.SubElement(root,'mxCell',id=key,parent=parent,vertex='1',value='',style=style+';html=1;strokeColor=#000000;fillColor=#FFFFFF;strokeWidth=1;aspect=fixed;')
    ET.SubElement(e,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    return e


def add_symbols(d):
    for key,kind in ICONS.get(d.slug[:2],{}).items():
        d.nodes[key]['icon']=kind
        # A área útil desconta o símbolo; rótulos extensos usam 13 pt.
        if d.nodes[key]['w']<=220:d.nodes[key]['font']=13


def export(d):
    el=base.export_xml(d);root=el.find('mxGraphModel/root')
    for key,n in d.nodes.items():
        kind=n.get('icon')
        if not kind:continue
        box=root.find(f"mxCell[@id='{key}']")
        box.set('style',box.get('style')+'spacingLeft=44;spacingRight=8;')
        x,y,w,h=icon_geometry(n,kind)
        if kind=='lock':
            cell(root,key+'_shackle',key,'ellipse',x+5,y+1,14,18)
            cell(root,key+'_lock',key,'rounded=1;arcSize=10',x+1,y+10,22,14)
            cell(root,key+'_keyhole',key,'ellipse;fillColor=#000000',x+11,y+15,2,4).set('style','ellipse;fillColor=#000000;strokeColor=#000000;')
        else:
            style={'document':'shape=document;size=0.2','database':'shape=cylinder3;size=4;boundedLbl=1','component':'shape=component;jettyWidth=5;jettyHeight=4'}.get(kind,'shape=mxgraph.gmdl.'+kind)
            cell(root,key+'_symbol',key,style,x,y,w,h)
    return el


def arc(p,x0,y0,a):
    """SVG elliptical arc to cubic Béziers, in the stencil's own coordinates."""
    x1,y1=float(a['x']),float(a['y']);rx,ry=abs(float(a['rx'])),abs(float(a['ry']))
    if not rx or not ry or (x0==x1 and y0==y1):p.lineTo(x1,y1);return
    phi=math.radians(float(a.get('x-axis-rotation',0)));cp,sp=math.cos(phi),math.sin(phi)
    xp=cp*(x0-x1)/2+sp*(y0-y1)/2;yp=-sp*(x0-x1)/2+cp*(y0-y1)/2
    lam=xp*xp/(rx*rx)+yp*yp/(ry*ry)
    if lam>1:rx*=math.sqrt(lam);ry*=math.sqrt(lam)
    large=int(a.get('large-arc-flag',0));sweep=int(a.get('sweep-flag',0))
    v=max(0,(rx*rx*ry*ry-rx*rx*yp*yp-ry*ry*xp*xp)/(rx*rx*yp*yp+ry*ry*xp*xp))
    fac=(-1 if large==sweep else 1)*math.sqrt(v)
    cxp=fac*rx*yp/ry;cyp=-fac*ry*xp/rx
    cx=cp*cxp-sp*cyp+(x0+x1)/2;cy=sp*cxp+cp*cyp+(y0+y1)/2
    u=((xp-cxp)/rx,(yp-cyp)/ry);v=((-xp-cxp)/rx,(-yp-cyp)/ry)
    t0=math.atan2(u[1],u[0]);dt=math.atan2(u[0]*v[1]-u[1]*v[0],u[0]*v[0]+u[1]*v[1])
    if not sweep and dt>0:dt-=2*math.pi
    if sweep and dt<0:dt+=2*math.pi
    count=max(1,math.ceil(abs(dt)/(math.pi/2)));step=dt/count
    def point(t):return (cx+rx*cp*math.cos(t)-ry*sp*math.sin(t),cy+rx*sp*math.cos(t)+ry*cp*math.sin(t))
    def tangent(t):return (-rx*cp*math.sin(t)-ry*sp*math.cos(t),-rx*sp*math.sin(t)+ry*cp*math.cos(t))
    for i in range(count):
        t=t0+i*step;z=t+step;k=4/3*math.tan(step/4);a0,b0=point(t),point(z);da,db=tangent(t),tangent(z)
        p.curveTo(a0[0]+k*da[0],a0[1]+k*da[1],b0[0]-k*db[0],b0[1]-k*db[1],*b0)


def stencil(c,kind,w,h):
    s=STENCILS[kind];sx=w/float(s.get('w'));sy=h/float(s.get('h'))
    c.saveState();c.scale(sx,sy);c.setLineWidth(1/max(sx,sy))
    p=None;fill=True;stroke=True;stack=[]
    for e in s.find('foreground'):
        tag=e.tag;a=e.attrib
        if tag=='save':stack.append((fill,stroke));c.saveState()
        elif tag=='restore':fill,stroke=stack.pop();c.restoreState()
        elif tag=='fillcolor':fill=a['color']!='none'
        elif tag=='strokecolor':stroke=a['color']!='none'
        elif tag=='path':
            p=c.beginPath();last=(0,0)
            for q in e:
                if q.tag=='move':last=(float(q.get('x')),float(q.get('y')));p.moveTo(*last)
                elif q.tag=='line':last=(float(q.get('x')),float(q.get('y')));p.lineTo(*last)
                elif q.tag=='arc':arc(p,*last,q.attrib);last=(float(q.get('x')),float(q.get('y')))
                elif q.tag=='close':p.close()
                else:raise ValueError(q.tag)
        elif tag in ['rect','roundrect','ellipse']:
            p=c.beginPath();x,y,ww,hh=[float(a.get(k,0)) for k in ['x','y','w','h']]
            if tag=='ellipse':p.ellipse(x,y,x+ww,y+hh)
            elif tag=='rect':p.rect(x,y,ww,hh)
            else:raise ValueError(tag)
        elif tag in ['stroke','fill','fillstroke'] and p is not None:
            c.drawPath(p,stroke=int(stroke and tag in ['stroke','fillstroke']),fill=int(fill and tag in ['fill','fillstroke']))
        else:raise ValueError(tag)
    c.restoreState()


def symbol(c,kind,x,y,w,h,page_h):
    c.saveState();c.translate(x,page_h-y);c.scale(1,-1);c.setStrokeColorRGB(0,0,0);c.setFillColorRGB(1,1,1);c.setLineWidth(1)
    if kind in STENCILS:stencil(c,kind,w,h)
    elif kind=='lock':
        c.ellipse(5,1,19,19,fill=1);c.roundRect(1,10,22,14,1,fill=1)
        c.setFillColorRGB(0,0,0);c.ellipse(11,15,13,19,fill=1,stroke=0)
    elif kind=='component':
        c.rect(4,0,20,24,fill=1);c.rect(0,5,8,4,fill=1);c.rect(0,15,8,4,fill=1)
    elif kind=='database':
        c.rect(0,4,w,h-8,fill=1,stroke=0);c.line(0,4,0,h-4);c.line(w,4,w,h-4)
        p=c.beginPath();p.moveTo(0,h-4);p.curveTo(0,h+1,w,h+1,w,h-4);c.drawPath(p)
        c.ellipse(0,0,w,8,fill=1)
    elif kind=='document':
        p=c.beginPath();p.moveTo(0,0);p.lineTo(w,0);p.lineTo(w,h*.8);p.curveTo(w*.6,h*.6,w*.4,h,0,h*.8);p.close();c.drawPath(p,fill=1)
    c.restoreState()


def render(c,d):
    # Reutiliza contornos e conexões já aprovados, pintando só rótulos com símbolos.
    plain=deepcopy(d)
    for n in plain.nodes.values():
        if n.get('icon'):n['label']=''
    base.render(c,plain)
    c.saveState();c.scale(.72,.72)
    for n in d.nodes.values():
        kind=n.get('icon')
        if not kind:continue
        x,y,w,h=icon_geometry(n,kind);symbol(c,kind,n['x']+x,n['y']+y,w,h,d.h)
        font='U-Bold' if n['bold'] else 'U';size=n['font'];width=n['w']-52
        ls=base.lines(n['label'],width,font,size);lh=size*1.3
        if len(ls)*lh>n['h']-8:raise ValueError('Texto não cabe: '+n['label'])
        ty=n['y']+(n['h']-len(ls)*lh)/2+size
        c.setFillColorRGB(0,0,0);c.setFont(font,size)
        for i,line in enumerate(ls):c.drawCentredString(n['x']+44+width/2,d.h-ty-i*lh,line)
    c.restoreState()


def main():
    pdfmetrics.registerFont(TTFont('U','C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('U-Bold','C:/Windows/Fonts/arialbd.ttf'))
    OUT.mkdir(exist_ok=True)
    first,first_xml=base.import_first();ds=[first,*base.diagrams()]
    # Afasta o rótulo da borda da nota explicativa.
    for e in ds[-1].edges:
        if e['a']=='risk' and e['b']=='caretest':e['at']=(245,180)
    combined=ET.Element('mxfile',host='app.diagrams.net')
    book=ROOT/'output/pdf/Diagramas_GuardKids_com_simbolos.pdf'
    c=canvas.Canvas(str(book));c.setTitle('GuardKids - Diagramas com símbolos nativos')
    counts={}
    for d in ds:
        add_symbols(d);xml=first_xml if d is first else export(d);combined.append(deepcopy(xml))
        single=ET.Element('mxfile',host='app.diagrams.net');single.append(deepcopy(xml))
        ET.ElementTree(single).write(OUT/(d.slug+'.drawio'),encoding='utf-8',xml_declaration=True)
        render(c,d);c.showPage()
        p=canvas.Canvas(str(OUT/(d.slug+'.pdf')));p.setTitle(d.name);render(p,d);p.save()
        counts[d.slug]=sum(bool(n.get('icon')) for n in d.nodes.values())
    c.save();ET.ElementTree(combined).write(OUT/'GuardKids_7_diagramas_com_simbolos.drawio',encoding='utf-8',xml_declaration=True)
    (OUT/'LEIA-ME.txt').write_text('Abra GuardKids_7_diagramas_com_simbolos.drawio no Draw.io. São sete abas.\nO primeiro desenho do autor foi preservado. Os outros seis receberam símbolos vetoriais editáveis.\nBalão: mensagem; lupa: busca; documento: fontes; componente: processamento/geração; cadeado: proteção; cilindro: registro/índice; visto: verificação; pasta: conjunto reservado.\nLupa, balão, visto e pasta pertencem à biblioteca GMDL nativa do Draw.io. Os demais usam formas básicas, documento, componente e cilindro. O cadeado é composto de formas básicas editáveis.\nOs ícones estão vinculados aos blocos e acompanham seu movimento.\nAs versões anteriores e o manuscrito foram mantidos.\nReferência da biblioteca: https://app.diagrams.net/stencils/gmdl.xml\n',encoding='utf-8')
    with zipfile.ZipFile(OUT/'GuardKids_diagramas_com_simbolos.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in OUT.iterdir():
            if p.suffix!='.zip':z.write(p,p.name)
    report={'abas':7,'simbolos_por_diagrama':counts,'total_simbolos':sum(counts.values()),'originais_preservados':True,'biblioteca':'https://app.diagrams.net/stencils/gmdl.xml'}
    (ROOT/'avaliacao/evidencias/verificacao_diagramas_com_simbolos_2026-11-04.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
