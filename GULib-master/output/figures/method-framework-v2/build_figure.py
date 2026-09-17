"""Compact framework: editable mxGraph primitives and matching vector PDF."""
from pathlib import Path
import xml.etree.ElementTree as E
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import pypdfium2 as pdfium

OUT=Path(__file__).parent
W,H=850,300
c=canvas.Canvas(str(OUT/'method-framework-v2.pdf'),pagesize=(W,H))
c.setTitle('Graph unlearning framework')
doc=E.Element('mxfile',host='app.diagrams.net')
d=E.SubElement(doc,'diagram',name='Framework',id='framework-v2')
m=E.SubElement(d,'mxGraphModel',grid='1',gridSize='5',page='1',pageWidth=str(W),pageHeight=str(H))
r=E.SubElement(m,'root');E.SubElement(r,'mxCell',id='0');E.SubElement(r,'mxCell',id='1',parent='0')
N='#23374B';T='#187F89';O='#BA6025';i=1

def vertex(value,style,x,y,w,h):
 global i
 i+=1
 q=E.SubElement(r,'mxCell',id=str(i),parent='1',vertex='1',value=value,style=style)
 E.SubElement(q,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
 return str(i)

def box(x,y,w,h,fill='#FFFFFF',stroke='#BCCAD5'):
 c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(1)
 c.roundRect(x,H-y-h,w,h,7,fill=1,stroke=1)
 return vertex('',f'rounded=1;arcSize=12;fillColor={fill};strokeColor={stroke};',x,y,w,h)

def text(x,y,w,s,size=14,bold=False,color=N):
 c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.setFillColor(HexColor(color))
 for k,line in enumerate(s.split('\n')):c.drawCentredString(x+w/2,H-y-size-k*size*1.25,line)
 vertex(s,f'text;html=0;whiteSpace=wrap;align=center;verticalAlign=top;spacing=0;fontFamily=Helvetica;fontSize={size};fontStyle={int(bold)};fontColor={color};strokeColor=none;fillColor=none;',x,y,w,size*1.25*len(s.split('\n'))+2)

def line(points,color=N,arrow=True,source=None,target=None):
 global i
 c.setStrokeColor(HexColor(color));c.setLineWidth(1.4)
 p=c.beginPath();p.moveTo(points[0][0],H-points[0][1])
 for x,y in points[1:]:p.lineTo(x,H-y)
 c.drawPath(p)
 if arrow:
  (a,b),(x,y)=points[-2:];theta=math.atan2(y-b,x-a)
  p=c.beginPath();p.moveTo(x,H-y)
  for delta in [-.45,.45]:p.lineTo(x-7*math.cos(theta+delta),H-y+7*math.sin(theta+delta))
  p.close();c.setFillColor(HexColor(color));c.drawPath(p,fill=1,stroke=0)
 i+=1
 attrs=dict(id=str(i),parent='1',edge='1',style=f'edgeStyle=none;rounded=0;strokeColor={color};strokeWidth=1.4;endArrow={"block" if arrow else "none"};endFill=1;')
 if source:attrs['source']=source
 if target:attrs['target']=target
 q=E.SubElement(r,'mxCell',**attrs)
 g=E.SubElement(q,'mxGeometry',relative='1',attrib={'as':'geometry'})
 for name,(x,y) in zip(['sourcePoint','targetPoint'],[points[0],points[-1]]):E.SubElement(g,'mxPoint',x=str(x),y=str(y),attrib={'as':name})
 if len(points)>2:
  arr=E.SubElement(g,'Array',attrib={'as':'points'})
  for x,y in points[1:-1]:E.SubElement(arr,'mxPoint',x=str(x),y=str(y))

def graph(x,y,selected=False):
 pts=[(x,y+23),(x+27,y),(x+36,y+43),(x+63,y+15),(x+82,y+47)]
 for a,b in [(0,1),(0,2),(1,2),(1,3),(2,3),(2,4),(3,4)]:line([pts[a],pts[b]],'#9AAAB7',False)
 for j,(xx,yy) in enumerate(pts):
  fill='#EDB88E' if selected and j in [1,3] else '#D3E9EC';stroke=O if selected and j in [1,3] else T
  c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.circle(xx,H-yy,5,fill=1)
  vertex('',f'ellipse;fillColor={fill};strokeColor={stroke};',xx-5,yy-5,10,10)

# A single access arrow targets the entire selection enclosure.
access=box(148,12,226,59,'#ECF4F8','#A8C0CE')
text(153,18,216,'Access',15,True)
text(152,44,218,'Black-box / Gray-box / White-box',12)
selection=box(148,108,226,164,'#F0F7F7','#98BFC1')
text(153,120,216,'Request selection',16,True)
line([(261,71),(261,108)],T,True,access,selection)

for x,y,w,label in [(164,159,194,'Random / Degree'),(164,212,89,'IM'),(269,212,89,'IF')]:
 box(x,y,w,38,'#FFFFFF','#AECACB');text(x+3,y+10,w-6,label,14,True)

text(12,121,108,'Graph G',15,True)
graph(25,157)
text(9,227,114,'Candidates C\nBudget k',13)
line([(119,190),(148,190)])

text(403,120,100,'Request S',15,True,color=O)
graph(412,160,True)
text(404,227,98,'|S| = k',14)
line([(374,190),(402,190)])

text(529,120,132,'Execution',16,True)
gu=box(535,160,130,42,'#EAF1F8','#A6BCCF');text(540,171,120,'GU method M',14,True)
rt=box(535,224,130,42,'#EAF5F1','#ABC9BD');text(540,235,120,'Full retrain',14,True)
line([(499,190),(518,190),(518,181),(535,181)])
line([(518,190),(518,245),(535,245)])
model=box(535,32,130,39,'#FFFFFF','#A6BCCF');text(538,43,124,'Trained model',13)
line([(600,71),(600,104),(677,104),(677,147),(600,147),(600,160)])

evalbox=box(710,108,130,164,'#FFF8F0','#D5B493')
text(714,120,122,'Comparison',16,True)
text(714,159,122,'Method response',13,True)
text(714,181,122,'Before / Random\n/ Targeted',12)
text(714,222,122,'GU vs. Retrain',13,True)
text(714,245,122,'Utility / predictions',11)
line([(665,181),(687,181),(687,190),(710,190)])
line([(665,245),(697,245),(697,207),(710,207)])

c.showPage();c.save();E.indent(doc)
E.ElementTree(doc).write(OUT/'method-framework-v2.drawio',encoding='utf-8',xml_declaration=True)
pdf=pdfium.PdfDocument(str(OUT/'method-framework-v2.pdf'))
pdf[0].render(scale=2).to_pil().save(OUT/'method-framework-v2.png')
assert len(pdf)==1
assert next(q for q in r if q.get('source')==access).get('target')==selection
print('Created v2. Access edge verified: access -> selection enclosure.')
