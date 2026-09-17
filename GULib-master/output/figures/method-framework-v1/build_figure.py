"""One geometry source for editable draw.io and vector PDF reference figure."""
from pathlib import Path
import math
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import pypdfium2 as pdfium

OUT = Path(__file__).parent
W, H = 1200, 570
pdf = canvas.Canvas(str(OUT / 'method-framework-v1.pdf'), pagesize=(W,H))
pdf.setTitle('Graph unlearning: request selection and evaluation - draft')
mx = ET.Element('mxfile', host='app.diagrams.net')
diagram = ET.SubElement(mx,'diagram',name='Method framework',id='framework')
model = ET.SubElement(diagram,'mxGraphModel',dx='1200',dy='570',grid='1',gridSize='10',page='1',pageWidth=str(W),pageHeight=str(H))
root = ET.SubElement(model,'root')
ET.SubElement(root,'mxCell',id='0')
ET.SubElement(root,'mxCell',id='1',parent='0')
counter=1
NAVY='#203449'; TEAL='#167D8D'; ORANGE='#C66B28'; GRAY='#576878'

def cell(value,style,x,y,w,h):
    global counter
    counter+=1
    c=ET.SubElement(root,'mxCell',id=str(counter),value=value,style=style,vertex='1',parent='1')
    ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    return str(counter)

def box(x,y,w,h,fill='#FFFFFF',stroke='#CBD5DF',radius=8):
    pdf.setFillColor(HexColor(fill));pdf.setStrokeColor(HexColor(stroke));pdf.setLineWidth(1)
    pdf.roundRect(x,H-y-h,w,h,radius,fill=1,stroke=1)
    return cell('',f'rounded=1;arcSize=10;fillColor={fill};strokeColor={stroke};',x,y,w,h)

def text(x,y,w,s,size=12,color=NAVY,bold=False,align='center'):
    font='Helvetica-Bold' if bold else 'Helvetica'
    pdf.setFont(font,size);pdf.setFillColor(HexColor(color))
    for i,line in enumerate(s.split('\n')):
        yy=H-y-size-i*size*1.32
        if align=='center':pdf.drawCentredString(x+w/2,yy,line)
        else:pdf.drawString(x,yy,line)
    cell(s,f'text;html=0;whiteSpace=wrap;align={align};verticalAlign=top;fontFamily=Helvetica;fontSize={size};fontColor={color};fontStyle={1 if bold else 0};strokeColor=none;fillColor=none;',x,y,w,len(s.split('\n'))*size*1.32+3)

def edge(points,color=NAVY,dashed=False,arrow=True):
    global counter
    pdf.setStrokeColor(HexColor(color));pdf.setLineWidth(1.4);pdf.setDash([4,3] if dashed else [])
    p=pdf.beginPath();p.moveTo(points[0][0],H-points[0][1])
    for x,y in points[1:]:p.lineTo(x,H-y)
    pdf.drawPath(p)
    pdf.setDash([])
    if arrow:
        (a,b),(x,y)=points[-2:];ang=math.atan2(y-b,x-a)
        p=pdf.beginPath();p.moveTo(x,H-y)
        for delta in [-.45,.45]:p.lineTo(x-7*math.cos(ang+delta),H-y+7*math.sin(ang+delta))
        p.close();pdf.setFillColor(HexColor(color));pdf.drawPath(p,fill=1,stroke=0)
    counter+=1
    c=ET.SubElement(root,'mxCell',id=str(counter),style=f'edgeStyle=none;rounded=0;strokeColor={color};strokeWidth=1.4;dashed={int(dashed)};endArrow={"block" if arrow else "none"};endFill=1;',edge='1',parent='1')
    g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
    for name,(x,y) in zip(['sourcePoint','targetPoint'],[points[0],points[-1]]):ET.SubElement(g,'mxPoint',x=str(x),y=str(y),attrib={'as':name})
    if len(points)>2:
        arr=ET.SubElement(g,'Array',attrib={'as':'points'})
        for x,y in points[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))

def graph(x,y):
    pts=[(x+10,y+43),(x+43,y+8),(x+62,y+56),(x+99,y+23),(x+130,y+59)]
    for a,b in [(0,1),(0,2),(1,2),(1,3),(2,3),(2,4),(3,4)]:edge([pts[a],pts[b]],'#8799AA',arrow=False)
    for xx,yy in pts:
        pdf.setFillColor(HexColor('#C6E5EC'));pdf.setStrokeColor(HexColor(TEAL));pdf.circle(xx,H-yy,6,fill=1)
        cell('','ellipse;fillColor=#C6E5EC;strokeColor=#167D8D;',xx-6,yy-6,12,12)

text(20,16,1160,'Strategic deletion requests: selection, execution and evaluation',20,bold=True)
text(20,45,1160,'METHOD FRAMEWORK  /  DISCUSSION DRAFT',9,GRAY)

# Information access is intentionally separate from execution.
box(255,79,480,100,'#F1F7FC','#A8BED2')
text(270,89,450,'Attacker information access',13,bold=True)
text(267,115,225,'Black-box transfer\nIndependent surrogate\nNo target-model queries',11)
text(503,115,220,'White-box\nTarget parameters and gradients',11)
text(753,108,423,'Reference settings; graph and label permissions\nare specified in the threat model.',11,GRAY,align='left')

for x,w,title in [(20,205,'1  Original state'),(255,240,'2  Request selection'),(545,270,'3  Matched execution'),(865,315,'4  Common evaluation')]:
    box(x,214,w,278,'#FAFCFD')
    text(x+8,227,w-16,title,14,bold=True)

graph(46,263)
text(30,347,185,'Graph G, candidates C\nDeletion budget k',12)
box(38,396,169,66,'#EAF1F8')
text(43,406,159,'Trained starting states',11,bold=True)
text(43,426,159,'Canonical / method-specific',10)

for y,title,desc in [(266,'Random / Degree','Random / structural baselines'),(333,'IM selector','Expected spread of a seed set'),(400,'IF selector','Target-loss influence score')]:
    box(271,y,208,54,'#FFFFFF','#9DBBC2')
    text(277,y+7,196,title,12,bold=True)
    text(277,y+28,196,desc,10,GRAY)
edge([(380,179),(380,196),(505,196),(505,427),(479,427)],TEAL,True)
edge([(225,354),(245,354),(245,360),(271,360)])

box(563,264,234,46,'#FFF1E5','#DBA87E')
text(569,271,222,'Deletion request S',12,ORANGE,True)
text(569,290,222,'S is a subset of C; |S| = k',10)
for yy in [293,360,427]:edge([(479,yy),(520,yy),(520,287),(563,287)])

box(563,341,234,50,'#EAF1F8','#9BB3CA')
text(569,348,222,'Graph unlearning M',12,bold=True)
text(569,370,222,'Update method-specific trained state',10)
box(563,423,234,50,'#EAF6F3','#99BFB3')
text(569,430,222,'Full retraining R',12,bold=True)
text(569,452,222,'Fresh training on retained data',10)
edge([(680,310),(680,341)])
edge([(797,287),(807,287),(807,411),(680,411),(680,423)])
edge([(207,436),(235,436),(235,512),(553,512),(553,366),(563,366)])
text(256,515,280,'Starting state feeds GU update only',9,GRAY)

box(881,264,283,57,'#FFFFFF')
text(887,272,271,'Fixed evaluation protocol',12,bold=True)
text(887,292,271,'Original graph, test nodes and labels',10)
edge([(797,366),(842,366),(842,284),(881,284)])
edge([(797,448),(851,448),(851,304),(881,304)])
box(881,337,283,57,'#FFFFFF')
text(887,345,271,'Evaluation endpoints',12,bold=True)
text(887,366,271,'F0  |  FM,0  |  FM(S)  |  FR(S)',12)
edge([(1022,321),(1022,337)])
box(881,410,283,66,'#FFF6EE','#DBA87E')
text(887,418,271,'Metrics and decomposition',12,ORANGE,True)
text(887,439,271,'Random-relative effects; GU-Retrain gap\nPrediction differences',10)
edge([(1022,394),(1022,410)])
text(873,506,299,'Matched-budget random requests follow\nthe same execution and evaluation path.',10,GRAY)
text(20,546,1160,'Baseline endpoints F0 and FM,0 are evaluated before deletion. Solid arrows: execution. Dashed arrow: selector information access.',10,GRAY)
pdf.showPage();pdf.save()
ET.indent(mx)
ET.ElementTree(mx).write(OUT/'method-framework-v1.drawio',encoding='utf-8',xml_declaration=True)
doc=pdfium.PdfDocument(str(OUT/'method-framework-v1.pdf'))
doc[0].render(scale=1.6).to_pil().save(OUT/'method-framework-v1.png')
print('Created drawio, vector PDF and PNG preview in', OUT)
