"""Compact framework: editable mxGraph primitives and matching vector PDF."""
from pathlib import Path
import xml.etree.ElementTree as E
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import pypdfium2 as pdfium

OUT=Path(__file__).parent
W,H=925,355
c=canvas.Canvas(str(OUT/'method-framework-v3.pdf'),pagesize=(W,H))
c.setTitle('Graph unlearning framework')
doc=E.Element('mxfile',host='app.diagrams.net')
d=E.SubElement(doc,'diagram',name='Framework',id='framework-v3')
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

box(164,153,194,49,'#FFFFFF','#AECACB')
text(167,158,188,'Baselines',14,True)
text(167,180,188,'Random / Degree',12)
for x,y,w,label in [(164,217,89,'IM'),(269,217,89,'IF')]:
 box(x,y,w,38,'#FFFFFF','#AECACB');text(x+3,y+10,w-6,label,14,True)

text(12,121,108,'Graph G',15,True)
graph(25,157)
text(9,227,114,'Candidates C\nBudget k',13)
line([(119,190),(148,190)])

text(403,120,100,'Request S',15,True,color=O)
graph(412,160,True)
text(404,227,98,'|S| = k',14)
line([(374,190),(402,190)])

text(494,88,226,'For each deletion request S',12,color=O)
group=box(535,108,150,165,'#F4F7FB','#A6BCCF')
text(540,120,140,'GU methods',16,True)
for yy,label in [(158,'GU method 1'),(208,'GU method 2')]:
 box(549,yy,122,35,'#FFFFFF','#A6BCCF')
 text(552,yy+9,116,label,14,True)
text(550,246,120,'...',17,True)
rt=box(535,299,150,40,'#EAF5F1','#ABC9BD');text(540,310,140,'Full retrain',14,True)
line([(499,190),(535,190)])
line([(518,190),(518,319),(535,319)])
model=box(535,22,150,42,'#FFFFFF','#A6BCCF');text(539,28,142,'Trained models',13,True)
text(539,46,142,'Method-specific',10)
# Starting states enter the GU family, never the full-retrain branch.
line([(685,43),(701,43),(701,148),(685,148)])

evalbox=box(745,108,168,231,'#FFF8F0','#D5B493')
text(751,120,156,'Evaluation',16,True)
text(751,162,156,'Metrics',14,True)
text(751,187,156,'Utility\nPrediction differences',12)
text(751,243,156,'Decomposition',14,True)
text(751,270,156,'Method response\nGU-Retrain gap',12)
line([(685,190),(745,190)])
line([(685,319),(719,319),(719,284),(745,284)])

c.showPage();c.save();E.indent(doc)
E.ElementTree(doc).write(OUT/'method-framework-v3.drawio',encoding='utf-8',xml_declaration=True)
pdf=pdfium.PdfDocument(str(OUT/'method-framework-v3.pdf'))
pdf[0].render(scale=2).to_pil().save(OUT/'method-framework-v3.png')
assert len(pdf)==1
assert next(q for q in r if q.get('source')==access).get('target')==selection
print('Created v3. Access edge verified: access -> selection enclosure.')
