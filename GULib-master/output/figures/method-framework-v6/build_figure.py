"""Editable vector framework and a comparison at the ICLR text width."""
from pathlib import Path
import math
import xml.etree.ElementTree as ET

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter, Transformation
import pypdfium2 as pdfium

OUT = Path(__file__).resolve().parent
W, H = 720, 180
INK, TEAL, ORANGE = '#23374B', '#187F89', '#BA6025'
pdf_path = OUT / 'method-framework-v6.pdf'
c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
c.setTitle('Compact graph-unlearning framework - v6')
doc = ET.Element('mxfile', host='app.diagrams.net')
diagram = ET.SubElement(doc, 'diagram', name='Compact framework', id='framework-v6')
model = ET.SubElement(diagram, 'mxGraphModel', grid='1', gridSize='5', page='1',
                      pageWidth=str(W), pageHeight=str(H))
root = ET.SubElement(model, 'root')
ET.SubElement(root, 'mxCell', id='0')
ET.SubElement(root, 'mxCell', id='1', parent='0')
counter = 1


def cell(value, style, x, y, width, height):
    global counter
    counter += 1
    node = ET.SubElement(root, 'mxCell', id=str(counter), parent='1', vertex='1',
                         value=value, style=style)
    ET.SubElement(node, 'mxGeometry', x=str(x), y=str(y), width=str(width),
                  height=str(height), attrib={'as': 'geometry'})
    return str(counter)


def box(x, y, width, height, fill, stroke):
    c.setFillColor(HexColor(fill))
    c.setStrokeColor(HexColor(stroke))
    c.setLineWidth(.9)
    c.roundRect(x, H-y-height, width, height, 6, fill=1, stroke=1)
    return cell('', f'rounded=1;arcSize=12;fillColor={fill};strokeColor={stroke};',
                x, y, width, height)


def text(x, y, width, value, size=14, bold=False, color=INK):
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    c.setFillColor(HexColor(color))
    for row, line in enumerate(value.split('\n')):
        c.drawCentredString(x+width/2, H-y-size-row*size*1.2, line)
    cell(value, f'text;html=0;whiteSpace=wrap;align=center;verticalAlign=top;spacing=0;'
         f'fontFamily=Helvetica;fontSize={size};fontStyle={int(bold)};fontColor={color};'
         'strokeColor=none;fillColor=none;', x, y, width, size*1.2*len(value.split('\n'))+2)


def line(points, color=INK, arrow=True, source=None, target=None):
    global counter
    c.setStrokeColor(HexColor(color))
    c.setLineWidth(1.2)
    p = c.beginPath()
    p.moveTo(points[0][0], H-points[0][1])
    for x, y in points[1:]:
        p.lineTo(x, H-y)
    c.drawPath(p)
    if arrow:
        (a, b), (x, y) = points[-2:]
        theta = math.atan2(y-b, x-a)
        p = c.beginPath()
        p.moveTo(x, H-y)
        for delta in [-.45, .45]:
            p.lineTo(x-6*math.cos(theta+delta), H-y+6*math.sin(theta+delta))
        p.close()
        c.setFillColor(HexColor(color))
        c.drawPath(p, fill=1, stroke=0)
    counter += 1
    attrs = dict(id=str(counter), parent='1', edge='1',
                 style=f'edgeStyle=none;rounded=0;strokeColor={color};strokeWidth=1.2;'
                 f'endArrow={"block" if arrow else "none"};endFill=1;')
    if source:
        attrs['source'] = source
    if target:
        attrs['target'] = target
    node = ET.SubElement(root, 'mxCell', **attrs)
    geom = ET.SubElement(node, 'mxGeometry', relative='1', attrib={'as': 'geometry'})
    for name, (x, y) in zip(['sourcePoint', 'targetPoint'], [points[0], points[-1]]):
        ET.SubElement(geom, 'mxPoint', x=str(x), y=str(y), attrib={'as': name})
    if len(points) > 2:
        arr = ET.SubElement(geom, 'Array', attrib={'as': 'points'})
        for x, y in points[1:-1]:
            ET.SubElement(arr, 'mxPoint', x=str(x), y=str(y))


def graph():
    pts = [(10, 92), (29, 65), (37, 113), (61, 79), (71, 118)]
    for a, b in [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]:
        line([pts[a], pts[b]], '#9AAAB7', False)
    for x, y in pts:
        c.setFillColor(HexColor('#D3E9EC'))
        c.setStrokeColor(HexColor(TEAL))
        c.circle(x, H-y, 3.4, fill=1, stroke=1)
        cell('', f'ellipse;fillColor=#D3E9EC;strokeColor={TEAL};', x-3.4, y-3.4, 6.8, 6.8)


# One visual level: selection, matched execution, and diagnostic comparisons.
text(1, 5, 271, '1  Construct a deletion request', 16, True)
text(317, 5, 158, '2  Paired execution', 16, True)
text(519, 5, 195, '3  Diagnose the drop', 16, True)
text(0, 35, 79, 'Graph G', 15, True)
graph()
text(0, 133, 80, 'Candidates C\nBudget k', 13)

selection = box(94, 35, 178, 133, '#F0F7F7', '#98BFC1')
text(99, 43, 168, 'Access (Sec. 3.2)', 13, color=TEAL)
line([(108, 67), (258, 67)], '#C3DADA', False)
text(99, 74, 168, 'IM  /  IF', 18, True)
text(98, 109, 170, 'Baselines', 14, True)
text(98, 132, 170, 'Random / Degree /\nPageRank', 13)
line([(77, 102), (94, 102)])

request = box(281, 90, 33, 28, '#FFF1E4', '#D6AD8B')
text(281, 92, 33, 'S', 18, True, ORANGE)
text(276, 65, 43, '|S| = k', 13, color=ORANGE)
line([(272, 104), (281, 104)], ORANGE, True, selection, request)

gu = box(334, 47, 139, 50, '#F4F7FB', '#A6BCCF')
text(339, 60, 129, 'GU method M', 16, True)
retrain = box(334, 119, 139, 44, '#EAF5F1', '#ABC9BD')
text(339, 130, 129, 'Full retrain', 16, True)
line([(314, 104), (324, 104), (324, 72), (334, 72)], source=request, target=gu)
line([(324, 104), (324, 141), (334, 141)], source=request, target=retrain)

evaluation = box(519, 35, 195, 133, '#FFF8F0', '#D5B493')
text(524, 43, 185, 'GU gap', 16, True)
text(524, 65, 185, 'Same-request retraining', 13)
line([(532, 86), (701, 86)], '#E6CFB8', False)
text(524, 92, 185, 'Gap amplification', 16, True)
text(524, 114, 185, 'Budget-matched Random', 13)
text(524, 146, 185, 'Starting point / random response', 12.5)
line([(473, 72), (519, 72)], source=gu, target=evaluation)
line([(473, 141), (496, 141), (496, 80), (519, 80)], source=retrain, target=evaluation)

c.showPage()
c.save()
ET.indent(doc)
ET.ElementTree(doc).write(OUT / 'method-framework-v6.drawio', encoding='utf-8', xml_declaration=True)

# Compose both vector figures at an identical 396 pt manuscript width.
comparison = OUT / 'method-framework-v5-v6-comparison.pdf'
labels = OUT / 'comparison-labels.pdf'
p = canvas.Canvas(str(labels), pagesize=(612, 612))
p.setTitle('Method framework v5 / v6 - same-width comparison')
p.setFillColor(HexColor(INK))
p.setFont('Helvetica-Bold', 17)
p.drawString(50, 575, 'Method framework: v5 vs. compact v6')
p.setFont('Helvetica', 10)
p.drawString(50, 554, 'Both figures use the same 396 pt width (ICLR manuscript text width).')
p.setFont('Helvetica-Bold', 12)
p.drawString(108, 519, 'v5  |  original layout')
p.drawString(108, 304, 'v6  |  compact candidate')
old_h = 396 * 355 / 925
new_h = 396 * H / W
p.setFont('Helvetica', 10)
p.drawString(108, 344, f'Height: {old_h:.1f} pt   |   Smallest original label: {10*396/925:.1f} pt')
p.drawString(108, 175, f'Height: {new_h:.1f} pt   |   Smallest label: {12.5*396/W:.1f} pt')
p.drawString(108, 155, f'{100*(1-new_h/old_h):.0f}% less height at the same width.')
p.setFont('Helvetica', 10)
for i, value in enumerate([
    'Access is an inline reference; trained-model icons are removed.',
    'The same request still branches to GU and full retraining.',
    'Diagnosis labels follow the current Section 4.3 draft.',
    'The original v5 and the current manuscript are preserved.',
]):
    p.drawString(108, 120-i*16, value)
p.showPage()
p.save()
page = PdfReader(labels).pages[0]
for source, y in [(OUT.parent/'method-framework-v5/method-framework-v5.pdf', 358),
                  (pdf_path, 193)]:
    figure = PdfReader(source).pages[0]
    scale = 396/float(figure.mediabox.width)
    page.merge_transformed_page(figure, Transformation().scale(scale).translate(108, y))
writer = PdfWriter()
writer.add_page(page)
writer.write(comparison)
labels.unlink()
for path in [pdf_path, comparison]:
    with pdfium.PdfDocument(str(path)) as rendered:
        rendered[0].render(scale=3).to_pil().save(path.with_suffix('.png'))
print(f'Created v6 and same-width comparison; height reduction {100*(1-new_h/old_h):.1f}%.')
