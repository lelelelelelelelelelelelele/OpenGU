"""F01 color/composition candidate. Reuse the native SVG/draw.io geometry helpers.

GTA supplies cyan/apricot object fills; KiOP supplies outlined objects and attached
role labels. No experimental values or scientific connections are added.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import xml.etree.ElementTree as ET
import vector_primitives as f
NAME = 'teaser'
W, H = (1280, 280)
INK, MUTED, LINE = ('#0F1423', '#5D626A', '#BABFC3')
CYAN, APRICOT, TEAL = ('#CBF2EF', '#F6E5D9', '#156E69')
NEUTRAL = '#E7E9E8'
f.INK, f.MUTED, f.LINE, f.ACCENT = (INK, MUTED, LINE, TEAL)
f.root.set('viewBox', f'0 0 {W} {H}')
f.model.set('pageWidth', str(W))
f.model.set('pageHeight', str(H))

def label(x, y, w, text, fill=NEUTRAL, fg=INK, size=19):
    f.rect(x, y, w, 26, fill, fill, 3, 0)
    f.text(x + w / 2, y + 19, text, size, True, '#000000', 'middle')

def graph(x, y, selected=False, scale=0.59):
    coords = [(x + a * scale, y + b * scale) for a, b in f.POINTS]
    for a, b in f.EDGES:
        f.line([coords[a], coords[b]], '#8B9799', 1.45)
    for i, (xx, yy) in enumerate(coords):
        active = selected and i in f.SELECTED
        if active:
            f.circle(xx, yy, 10.8, '#FFFFFF', TEAL, 1.8)
        fill = TEAL if active else NEUTRAL if i in f.ELIGIBLE else '#FFFFFF'
        f.circle(xx, yy, 6.7, fill, TEAL if active else INK if i in f.ELIGIBLE else '#A5ABAF', 1.5, f"{('selected' if selected else 'input')}-{i}")
    f.graph_records.append({'origin': [x, y], 'coords': coords, 'selected': sorted(f.SELECTED) if selected else []})

def data(x, y):
    for row in range(3):
        for col in range(3):
            f.rect(x + col * 7, y + row * 7, 6, 6, ['#F5F5F3', '#CDD1CF', '#929B9A'][(row + col) % 3], INK, 0, 0.45)
    for row in range(3):
        f.rect(x + 26, y + row * 7, 7, 6, '#CDD1CF' if row == 1 else '#929B9A', INK, 0, 0.45)

def view():
    f.eye(221, 57)
    f.text(239, 64, 'Attacker’s view', 19, True, '#000000')
    for x in [319, 446]:
        f.line([(x, 73), (x, 126)], LINE, 0.7, layer='shapes')
    f.small_graph(247, 88)
    f.network(284, 99, 0.6, '#929B9A')
    f.lock(300, 95)
    f.text(258, 137, 'Topology', 18, False, '#000000', 'middle')
    f.small_graph(351, 84)
    data(383, 73)
    f.network(348, 107, 0.57, INK)
    f.rich(366, 108, [('θ', False), ('s', True)], 19, '#000000')
    f.text(402, 112, 'X, y', 18, False, '#000000', 'middle', True)
    f.text(382, 137, 'Surrogate', 18, False, '#000000', 'middle')
    f.small_graph(477, 84)
    data(509, 73)
    f.network(470, 107, 0.57, INK)
    f.text(502, 112, 'θ*,∇', 18, False, '#000000', 'middle', True)
    f.text(547, 112, 'X, y', 18, False, '#000000', 'middle', True)
    f.text(509, 137, 'Target-direct', 18, False, '#000000', 'middle')
    f.line([(229, 142), (229, 147), (557, 147), (557, 142)], LINE, 0.9, layer='shapes')
    f.line([(389, 147), (389, 153)], INK, 1.5, True)

def selector():
    f.rect(196, 167, 386, 84, '#FFFFFF', INK, 5, 1.8)
    f.rect(211, 154, 285, 30, CYAN, TEAL, 3, 1.4)
    f.circle(229, 162, 4.7, 'none', TEAL, 1.4)
    f.line([(220, 177), (220, 173), (224, 169), (234, 169), (238, 173), (238, 177)], TEAL, 1.4, layer='shapes')
    f.text(249, 176, 'Red-team Selector', 23, True, '#000000')
    f.line([(196, 217), (208, 217)], INK, 1.4, layer='shapes')
    f.line([(208, 200), (208, 234)], INK, 1.4, layer='shapes')
    for yy in [200, 234]:
        f.line([(208, yy), (221, yy)], INK, 1.4, True, layer='shapes')
    label(225, 187, 44, 'IM', CYAN, INK, 23)
    f.text(280, 207, 'Coverage', 19, False, '#000000')
    f.circle(423, 200, 13, CYAN, TEAL, 1.1)
    for xx, yy in [(410, 189), (437, 191), (438, 211)]:
        f.line([(423, 200), (xx, yy)], INK, 1, layer='shapes')
        f.circle(xx, yy, 3, '#FFFFFF', INK, 1)
    f.circle(423, 200, 3.8, TEAL, INK, 1)
    label(225, 221, 44, 'IF', APRICOT, INK, 23)
    f.text(280, 241, 'Sensitivity', 19, False, '#000000')
    f.network(414, 234, 0.6, INK)
    f.text(456, 241, '∇L', 21, False, '#000000', 'middle', True)
    f.line([(460, 200), (551, 200), (551, 217)], TEAL, 1.4, layer='shapes')
    f.line([(479, 234), (551, 234), (551, 217)], TEAL, 1.4, layer='shapes')
    f.text(514, 223, 'OR', 19, True, '#000000', 'middle')
    f.circle(551, 217, 2.5, TEAL, TEAL, 0)
    f.line([(551, 217), (582, 217)], TEAL, 1.4, layer='shapes')
    f.text(389, 273, 'Baselines · Random / Degree / PR', 18, False, '#000000', 'middle')

def request_document():
    f.line([(607, 95), (746, 95), (766, 115), (766, 224), (607, 224), (607, 95)], TEAL, 1.5, layer='shapes')
    f.line([(746, 95), (746, 115), (766, 115)], TEAL, 1.2, layer='shapes')
    f.text(620, 118, 'Request S', 20, True, '#000000')
    graph(620, 135, True)
f.rect(0, 0, W, H, stroke='#FFFFFF', layer='background')

view()
selector()
label(46, 94, 104, 'Graph G', NEUTRAL, INK, 20)
graph(34, 135)
f.circle(28, 237, 5.2, NEUTRAL, INK, 1.4)
f.text(40, 244, 'Eligible pool C', 19, False, '#000000')
f.text(98, 267, 'Fixed data / split', 18, False, '#000000', 'middle')
f.line([(178, 186), (185, 186), (185, 217), (194, 217)], INK, 1.7, True)
f.line([(584, 217), (603, 217)], TEAL, 1.8, True)
request_document()
f.text(687, 244, 'Deletion targets', 19, False, '#000000', 'middle')
f.text(687, 270, 'S ⊆ C, |S| = k', 22, False, '#000000', 'middle', True)
f.line([(766, 186), (780, 186)], TEAL, 1.8)
f.circle(780, 186, 2.6, TEAL, TEAL, 0)
f.line([(780, 166), (780, 226)], TEAL, 1.5)
f.line([(780, 186), (780, 62), (800, 62)], MUTED, 1.2, True, True)
f.text(810, 69, 'Full retrain ref.', 18, False, '#000000')
f.line([(944, 62), (983, 62)], MUTED, 1.2, True, True)
f.rich(1000, 69, [('U', False), ('R', True), ('(S)', False)], 21, '#000000')
f.text(804, 102, 'GU → response', 19, True, '#000000')
f.text(1044, 102, 'Retrain gap', 19, True, '#000000', 'middle')
f.text(1190, 102, 'Excess gap', 19, True, '#000000', 'middle')
f.rich(1044, 133, [('G', False), ('M', True), ('\u2009=\u2009U', False), ('R', True), ('\u2009−\u2009U', False), ('M', True)], 21, '#000000', 'middle')
f.rich(1190, 133, [('E', False), ('M', True), ('\u2009=\u2009G', False), ('M', True), ('\u2009−\u2009', False), ('G', 'bar'), ('M,r', True)], 21, '#000000', 'middle')
f.line([(802, 147.5), (1258, 147.5)], LINE, 0.7, layer='shapes')
f.layers['shapes'][-1].set('data-role','diagnostic-divider')
for suffix, y in [('1', 166), ('m', 226)]:
    f.line([(780, y), (799, y)], TEAL, 1.5, True)
    f.network(816, y, 0.69, INK)
    f.rich(838, y + 6, [('M', False), (suffix, True)], 23, '#000000')
    f.line([(879, y), (899, y)], INK, 1.4, True)
    f.rich(913, y + 6, [('U', False), ('M' + suffix, True)], 23, '#000000')
    f.line([(965, y), (992, y)], INK, 1.4, True)
    f.rich(1044, y + 6, [('G', False), ('M' + suffix, True)], 24, '#000000', 'middle')
    f.line([(1082, y), (1121, y)], MUTED, 1.2, True)
    f.rich(1190, y + 6, [('E', False), ('M' + suffix, True)], 24, '#000000', 'middle')
for x in [848, 936, 1044, 1190]:
    for yy in [191, 197, 203]:
        f.circle(x, yy, 1.15, MUTED, MUTED, 0)
f.text(876, 261, 'Trained models', 18, False, '#000000', 'middle')
f.text(1044, 261, 'same S', 18, False, '#000000', 'middle')
f.text(1190, 261, 'same k · Random', 18, False, '#000000', 'middle')
# Reclaim the old heading band and place conventional panel captions below.
BODY_DY = -32
for layer_name, layer in f.layers.items():
    if layer_name != 'background':
        layer.set('transform', f'translate(0 {BODY_DY})')
# Draw.io has native cells rather than SVG layer transforms.
for cell in f.mxroot.findall('mxCell'):
    geo=cell.find('mxGeometry')
    if geo is None or cell.get('id')=='2':
        continue
    if cell.get('vertex')=='1':
        geo.set('y',str(float(geo.get('y','0'))+BODY_DY))
    for point in geo.iter('mxPoint'):
        point.set('y',str(float(point.get('y','0'))+BODY_DY))
caption_layer=ET.SubElement(f.root,f'{{{f.SVG}}}g',id='panel-captions')
f.layers['labels']=caption_layer
f.text(389,271,'(a) Request selection',19,False,'#000000','middle')
f.text(1023.5,271,'(b) GU responses & diagnosis',19,False,'#000000','middle')
(f.OUT/'panel-layout.json').write_text(json.dumps({
    'body_translation':[0,BODY_DY],
    'caption_baseline':271,'caption_size':19,
    'captions':[{'text':'(a) Request selection','center_x':389},
                {'text':'(b) GU responses & diagnosis','center_x':1023.5}],
    'canvas':[W,H]},indent=2),encoding='utf-8')

relative = lambda g: [(round(x - g['origin'][0], 5), round(y - g['origin'][1], 5)) for x, y in g['coords']]
assert relative(f.graph_records[0]) == relative(f.graph_records[1])
assert f.SELECTED <= f.ELIGIBLE
f.save(NAME, 'F01: choose existing nodes, issue one request, audit each GU method', 'An attacker-view-conditioned red-team Selector chooses existing eligible nodes. The input graph is shared by the IM coverage OR IF sensitivity selection routes. OR denotes alternative selection rules, not mutually exclusive access permissions. A deletion-request document preserves all node positions and marks only S. The graph is not poisoned or modified; no nodes are added. The same request S fans out to trained GU methods M1 through Mm and full retraining. Each method row aligns utility U_M, retrain gap G_M and excess gap E_M. Same-request full retraining and same-budget Random are separate references. All outputs are symbolic; no results, rankings or evaluation feedback to the Selector are shown.')
(f.OUT / 'semantic-check.json').write_text(json.dumps({'candidate': NAME, 'canvas': [W, H], 'date': '2026-10-25', 'control': 'selector-04-header-spacing', 'node_ids': list(range(len(f.POINTS))), 'edges': f.EDGES, 'graphs': f.graph_records, 'eligible_node_ids': sorted(f.ELIGIBLE), 'selected_node_ids': sorted(f.SELECTED), 'fixed_node_positions': relative(f.graph_records[0]) == relative(f.graph_records[1]), 'selected_subset_of_candidates': f.SELECTED <= f.ELIGIBLE, 'same_S_for_each_GU_and_retrain': True, 'method_rows': ['M1', 'ellipsis', 'Mm'], 'method_level_frames': 0, 'row_outputs': ['U_M', 'G_M', 'E_M'], 'IM_OR_IF_visible': True, 'same_budget_random_reference': True, 'experimental_values': False, 'evaluation_feedback_to_selector': False, 'scope': 'Coordinate/subset assertions; other relationships manually reviewed against the generator and rendered figure.'}, ensure_ascii=False, indent=2), encoding='utf-8')
print('Generated ' + NAME + '.svg / .drawio in ' + str(f.OUT))
