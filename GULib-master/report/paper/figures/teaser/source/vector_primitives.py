"""Refine the preferred F01 B layout; SVG and draw.io share one geometry.

This is a style trial, not the adopted v5 or the AAGU-084 refinement.
Run this file, then render.mjs. A/C remain historical layout comparisons.
All node positions are illustrative.
"""
from pathlib import Path
from html import escape
import json
import math
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent.parent
assert OUT.name == 'teaser', 'Generator must remain in this revision/source'
W, H = 1280, 280
INK = '#242424'
MUTED = '#626262'
LINE = '#b8b8b8'
ACCENT = '#9f4438'
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
root = ET.Element(f'{{{SVG}}}svg', viewBox=f'0 0 {W} {H}', role='img',
                  attrib={'aria-labelledby': 'title description'})
ET.SubElement(root, f'{{{SVG}}}title', id='title').text = 'Deletion-request selection and paired graph-unlearning evaluation'
ET.SubElement(root, f'{{{SVG}}}desc', id='description').text = (
    'A red-team selector uses permitted information and budget k to choose existing '
    'eligible nodes S. The same request is evaluated with graph unlearning and full '
    'retraining. Starting-point references and budget-matched random requests support '
    'diagnosis. Node positions are illustrative, not an experimental result.')
defs = ET.SubElement(root, f'{{{SVG}}}defs')
ET.SubElement(defs, f'{{{SVG}}}style').text = (
    'text{font-family:Arial,Helvetica,sans-serif;fill:#000000}'
    '.math{font-family:"Times New Roman",serif;font-style:italic}'
    'path,line,rect,circle{stroke-linecap:round;stroke-linejoin:round}'
)
layers = {name: ET.SubElement(root, f'{{{SVG}}}g', id=name)
          for name in ['background', 'connectors', 'shapes', 'labels']}

doc = ET.Element('mxfile', host='app.diagrams.net', version='24.7.17')
diagram = ET.SubElement(doc, 'diagram', id='f01-selector-trial', name='Selector pipeline trial')
model = ET.SubElement(diagram, 'mxGraphModel', grid='1', gridSize='5', page='1',
                      pageWidth=str(W), pageHeight=str(H), background='#FFFFFF')
mxroot = ET.SubElement(model, 'root')
ET.SubElement(mxroot, 'mxCell', id='0')
ET.SubElement(mxroot, 'mxCell', id='1', parent='0')
counter = 1

def cell(value, style, x, y, w, h):
    global counter
    counter += 1
    item = ET.SubElement(mxroot, 'mxCell', id=str(counter), value=value,
                         style=style, vertex='1', parent='1')
    ET.SubElement(item, 'mxGeometry', x=str(x), y=str(y), width=str(w),
                  height=str(h), attrib={'as': 'geometry'})

def rect(x, y, w, h, fill='#FFFFFF', stroke=LINE, radius=0, width=1.3, layer='shapes'):
    ET.SubElement(layers[layer], f'{{{SVG}}}rect', x=str(x), y=str(y),
                  width=str(w), height=str(h), rx=str(radius), fill=fill,
                  stroke=stroke, attrib={'stroke-width': str(width)})
    cell('', f'rounded={int(radius>0)};arcSize=6;fillColor={fill};strokeColor={stroke};strokeWidth={width};', x,y,w,h)

def circle(x, y, r, fill, stroke, width=1.5, key=None):
    attrib = {'cx':str(x), 'cy':str(y), 'r':str(r), 'fill':fill,
              'stroke':stroke, 'stroke-width':str(width)}
    if key:
        attrib['data-node'] = key
    ET.SubElement(layers['shapes'], f'{{{SVG}}}circle', attrib)
    cell('', f'ellipse;fillColor={fill};strokeColor={stroke};strokeWidth={width};', x-r,y-r,2*r,2*r)

arrow_records=[]

def line(points, color=INK, width=1.8, arrow=False, dashed=False, layer='connectors'):
    """Native shaft plus editable head. The head tip owns the original endpoint."""
    global counter
    shaft=list(points)
    head=None
    if arrow:
        x,y=points[-1]; px,py=points[-2]
        length=math.hypot(x-px,y-py)
        assert length>0
        ux,uy=(x-px)/length,(y-py)/length
        head_length=min(8.0,length*.75)
        half_width=head_length*.4
        bx,by=x-head_length*ux,y-head_length*uy
        head=[(x,y),(bx-half_width*uy,by+half_width*ux),(bx+half_width*uy,by-half_width*ux)]
        # A small overlap sits inside the filled head; no shaft reaches its tip.
        shaft[-1]=(bx+.4*ux,by+.4*uy)
        arrow_records.append({'points':points,'tip':[x,y],'shaft_end':shaft[-1],
                              'head':head,'head_length':head_length,'color':color})
    attrib={'d':'M'+' L'.join(f'{x} {y}' for x,y in shaft),'fill':'none',
            'stroke':color,'stroke-width':str(width)}
    if dashed: attrib['stroke-dasharray']='5 5'
    if arrow:
        attrib['data-arrow-shaft']='true'
        attrib['data-arrow-tip']=' '.join(str(v) for v in points[-1])
        attrib['style']='stroke-linecap:butt'
    ET.SubElement(layers[layer],f'{{{SVG}}}path',attrib)
    if arrow and dashed:
        # End the dashed route with a solid join, independent of dash phase.
        join_length=min(3.0,math.hypot(shaft[-1][0]-points[-2][0],shaft[-1][1]-points[-2][1]))
        jx,jy=shaft[-1][0]-join_length*ux,shaft[-1][1]-join_length*uy
        ET.SubElement(layers[layer],f'{{{SVG}}}path',
                      d=f'M{jx} {jy} L{shaft[-1][0]} {shaft[-1][1]}',fill='none',
                      stroke=color,attrib={'stroke-width':str(width),'style':'stroke-linecap:butt','data-arrow-terminal':'true'})
        counter+=1
        join_edge=ET.SubElement(mxroot,'mxCell',id=str(counter),edge='1',parent='1',
                      style=f'edgeStyle=none;strokeColor={color};strokeWidth={width};endArrow=none;')
        jgeom=ET.SubElement(join_edge,'mxGeometry',relative='1',attrib={'as':'geometry'})
        for name,(xx,yy) in zip(['sourcePoint','targetPoint'],[(jx,jy),shaft[-1]]):
            ET.SubElement(jgeom,'mxPoint',x=str(xx),y=str(yy),attrib={'as':name})
    counter+=1
    edge=ET.SubElement(mxroot,'mxCell',id=str(counter),edge='1',parent='1',
        style=f'edgeStyle=none;rounded=0;strokeColor={color};strokeWidth={width};endArrow=none;dashed={int(dashed)};')
    geom=ET.SubElement(edge,'mxGeometry',relative='1',attrib={'as':'geometry'})
    for name,(x,y) in zip(['sourcePoint','targetPoint'],[shaft[0],shaft[-1]]):
        ET.SubElement(geom,'mxPoint',x=str(x),y=str(y),attrib={'as':name})
    if len(shaft)>2:
        arr=ET.SubElement(geom,'Array',attrib={'as':'points'})
        for x,y in shaft[1:-1]: ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    if head:
        ET.SubElement(layers[layer],f'{{{SVG}}}polygon',points=' '.join(f'{x},{y}' for x,y in head),
                      fill=color,stroke='none',attrib={'data-arrow-head':'true','data-tip':f'{head[0][0]} {head[0][1]}'})
        angle=math.degrees(math.atan2(uy,ux))
        cx,cy=points[-1][0]-head_length*.5*ux,points[-1][1]-head_length*.5*uy
        cell('',f'shape=triangle;direction=east;rotation={angle};fillColor={color};strokeColor=none;',
             cx-head_length/2,cy-half_width,head_length,half_width*2)


def text(x, y, value, size=20, bold=False, color=INK, anchor='start', math_font=False):
    attrs={'x':str(x),'y':str(y),'font-size':str(size),'text-anchor':anchor,
           'style':f'fill:{color}', 'font-weight':'700' if bold else '400'}
    if math_font: attrs['class']='math'
    ET.SubElement(layers['labels'],f'{{{SVG}}}text',attrs).text=value
    # draw.io uses a text baseline 80% of its line height from the top.
    w = max(80, len(value)*size*.58+12)
    left = x-w/2 if anchor=='middle' else x-w if anchor=='end' else x
    cell(value, f'text;html=0;whiteSpace=wrap;align={"center" if anchor=="middle" else "right" if anchor=="end" else "left"};verticalAlign=top;spacing=0;fontFamily={"Times New Roman" if math_font else "Arial"};fontSize={size};fontStyle={int(bold)+(2 if math_font else 0)};fontColor={color};strokeColor=none;fillColor=none;',left,y-size*.88,w,size*1.35)

def rich(x, y, runs, size=23, color=INK, anchor='start'):
    attrs={'x':str(x),'y':str(y),'font-size':str(size),'text-anchor':anchor,
           'style':f'fill:{color}', 'class':'math'}
    item=ET.SubElement(layers['labels'],f'{{{SVG}}}text',attrs)
    html=[]
    for content, sub in runs:
        attrs=({'baseline-shift':'sub','font-size':str(size*.68)} if sub is True
               else {'text-decoration':'overline'} if sub=='bar' else {})
        span=ET.SubElement(item,f'{{{SVG}}}tspan',attrib=attrs)
        span.text=content
        html.append(f'<sub>{escape(content)}</sub>' if sub is True else
                    f'<span style="text-decoration:overline">{escape(content)}</span>'
                    if sub=='bar' else escape(content))
    n=sum(len(s) for s,_ in runs)
    w=max(80,n*size*.51+8)
    left=x-w/2 if anchor=='middle' else x
    cell(''.join(html),f'text;html=1;align={"center" if anchor=="middle" else "left"};verticalAlign=top;spacing=0;fontFamily=Times New Roman;fontSize={size};fontStyle=2;fontColor={color};strokeColor=none;fillColor=none;',left,y-size*.88,w,size*1.45)

def heading(x, end, number, label):
    text(x,35,number,22,True)
    text(x+38,35,label,22,True)
    line([(x,46),(end,46)],LINE,.8)

POINTS=[(0,69),(30,22),(44,120),(81,68),(101,8),
        (113,122),(150,40),(176,103),(194,4),(215,66)]
EDGES=[(0,1),(0,2),(0,3),(1,3),(1,4),(2,3),(2,5),(3,4),
       (3,5),(3,6),(4,6),(4,8),(5,6),(5,7),(6,7),(6,8),(6,9),(7,9),(8,9)]
ELIGIBLE={0,1,2,3,5,6,7,9}
SELECTED={1,5,9}
graph_records=[]

def graph(x,y,selected=False,scale=.78):
    coords=[(x+a*scale,y+b*scale) for a,b in POINTS]
    for a,b in EDGES: line([coords[a],coords[b]],'#a2a2a2',1.5)
    for i,(xx,yy) in enumerate(coords):
        active=selected and i in SELECTED
        if active: circle(xx,yy,11.5,'#FFFFFF',ACCENT,1.6)
        fill=ACCENT if active else '#dddddd' if i in ELIGIBLE else '#FFFFFF'
        circle(xx,yy,6.9,fill,ACCENT if active else '#575757' if i in ELIGIBLE else '#a2a2a2',1.4,
               f'{"selected" if selected else "input"}-{i}')
    graph_records.append({'origin':[x,y],'coords':coords,'selected':sorted(SELECTED) if selected else []})

def network(cx, cy, scale=1, color=INK):
    pts=[(cx-12*scale,cy-10*scale),(cx-12*scale,cy+10*scale),
         (cx,cy-15*scale),(cx,cy+15*scale),(cx+13*scale,cy)]
    for a,b in [(0,2),(0,3),(1,2),(1,3),(2,4),(3,4)]: line([pts[a],pts[b]],color,1.1,layer='shapes')
    for xx,yy in pts: circle(xx,yy,2.8*scale,'#FFFFFF',color,1.3)


def save(name, title, description):
    root.find(f'{{{SVG}}}title').text = title
    root.find(f'{{{SVG}}}desc').text = description
    diagram.set('name', title)
    # XML pretty-printing injects rendered whitespace between SVG tspans.
    # Keep formula runs adjacent; indentation remains safe for mxGraph attributes.
    assert all(s.tail is None for t in root.iter(f'{{{SVG}}}text')
               for s in t.findall(f'{{{SVG}}}tspan'))
    (OUT/'arrow-records.json').write_text(json.dumps(arrow_records,indent=2),encoding='utf-8')
    ET.ElementTree(root).write(OUT/(name+'.svg'),encoding='utf-8',xml_declaration=True)
    ET.indent(doc)
    ET.ElementTree(doc).write(OUT/(name+'.drawio'),encoding='utf-8',xml_declaration=True)


def actor(cx,cy):
    # A neutral research actor, without a dialogue bubble or adversarial costume.
    circle(cx,cy-8,6.7,'#FFFFFF',INK,1.6)
    line([(cx-12,cy+13),(cx-12,cy+8),(cx-6,cy+2),
          (cx+6,cy+2),(cx+12,cy+8),(cx+12,cy+13)],INK,1.6,layer='shapes')


def eye(cx,cy):
    # An outlined eye denotes observation of an information view.
    line([(cx-10,cy),(cx-5,cy-5),(cx+5,cy-5),(cx+10,cy),
          (cx+5,cy+5),(cx-5,cy+5),(cx-10,cy)],MUTED,1.3,layer='shapes')
    circle(cx,cy,2.8,'#FFFFFF',INK,1.2)


def small_graph(cx,cy):
    pts=[(cx-23,cy+9),(cx-8,cy-13),(cx+9,cy+11),(cx+24,cy-7)]
    for a,b in [(0,1),(0,2),(1,2),(1,3),(2,3)]:
        line([pts[a],pts[b]],'#888888',1.1,layer='shapes')
    for xx,yy in pts: circle(xx,yy,3.8,'#dddddd',INK,1.1)


def data_tiles(x,y):
    # Features and training/validation labels are data objects, not prose lists.
    for row in range(3):
        for col in range(3):
            fill=['#f4f4f4','#cccccc','#969696'][(row+col)%3]
            rect(x+col*7,y+row*7,6,6,fill,'#969696',0,.5)
    for row,fill in enumerate(['#777777','#cccccc','#777777']):
        rect(x+27,y+row*7,8,6,fill,'#888888',0,.5)


def lock(cx,cy):
    # A closed lock marks unavailable model information in the topology view.
    line([(cx-5,cy),(cx-5,cy-5),(cx-2,cy-8),(cx+2,cy-8),
          (cx+5,cy-5),(cx+5,cy)],MUTED,1.3,layer='shapes')
    rect(cx-8,cy,16,13,'#FFFFFF',MUTED,0,1.3)
    circle(cx,cy+5,1.6,MUTED,MUTED,.5)
