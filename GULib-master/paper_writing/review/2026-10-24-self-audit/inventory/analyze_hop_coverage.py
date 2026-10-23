# -*- coding: utf-8 -*-
"""Audit persisted Hop fields, without loading datasets or prediction caches."""
from pathlib import Path
import csv
import hashlib
import json
from collections import Counter, defaultdict
from statistics import mean, stdev

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SPECS = [
    ('EXP-011','exp011-t2','e11r1','exp011-20261023-e11r1',1449),
    ('EXP-079','exp079-surrogate-multiseed','e79r6','exp079-20261023-e79r6',2520),
    ('EXP-080','exp080-cc-base','e80r305','exp080-20261018-e80r305',1764),
    ('EXP-080','exp080-cc-cora-high','e80r302','exp080-20261018-e80r302',105),
    ('EXP-080','exp080-cc-citeseer-high','e80r306','exp080-20261019-e80r306',147),
]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_write(name, rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def json_write(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def request_key(cell):
    co=cell['conditions']
    return (co['dataset_name'],co['training_seed'],co['selector_ref'],co['budget_ratio'],
            co.get('random_selector_seed'),co.get('im_selector_seed'),cell['selection_id'])


idx={i['path']:i for i in read(ROOT/'.syncmate/artifact_index.json')['peers']['gpu4090']['items']}
raw=[];hop=[];geom={};coverage=[];statuses=Counter();protocols=Counter();status_rows=[];source_hashes=[];stage_inventory=Counter()
for exp,experiment,rid,job,ncell in SPECS:
    root=ROOT/'results/runs/gpu4090'/experiment/rid
    prefix=f'results/runs/{experiment}/{rid}/'
    delivery_path=ROOT/f'.syncmate/deliveries/{job}.json'
    delivery=read(delivery_path); result=delivery['result']
    assert result['ok'] and result['gate_passed'] and result['project_acceptance']['passed']
    assert result['project_acceptance']['accepted_cells']==ncell
    manifest=result['completed_job']['result']['manifest']; assert manifest['status']=='verified'
    expected={i['path']:i['sha256'] for i in manifest['artifacts']}
    p=root/'run.json'; assert sha(p)==expected[prefix+'run.json']==idx[prefix+'run.json']['sha256']
    run=read(p);assert len(run['cells'])==ncell and run['status']=='completed'
    source_hashes.append({'run':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'delivery':str(delivery_path.relative_to(ROOT)).replace('\\','/'),'delivery_sha256':sha(delivery_path)})
    retrains={}
    for c in run['cells']:
        if c['conditions']['method']=='Retrain':
            key=request_key(c)
            assert retrains.setdefault(key,c['output'])==c['output']
    local_hop=0;empty=0;stat=Counter()
    for c in run['cells']:
        co=c['conditions'];p=root/c['path']/'metrics.json';ref=prefix+c['path']+'/metrics.json'
        assert sha(p)==c['files']['metrics.json']['sha256']==expected[ref]==idx[ref]['sha256']
        m=read(p);assert m['cell_id']==c['cell_id']; stages={x['stage']:x for x in m['rows']}
        stem=Path(co['selector_ref']).stem
        source=next((s for s in ['SGC','GAT','GIN'] if stem.endswith('_'+s.lower())), 'GCN') if co['selector'] in ['r_point','gt_full'] else 'baseline'
        selector=stem if exp=='EXP-011' else co['selector']
        meta={'experiment':exp,'run_id':rid,'dataset':co['dataset_name'],'method':co['method'],'source':source,'selector':selector,
              'ratio':co['budget_ratio'],'seed':co['training_seed'],'random_seed':co.get('random_selector_seed'),
              'im_seed':co.get('im_selector_seed'),'selection_id':c['selection_id'],'cell_id':c['cell_id']}
        for stage in stages:stage_inventory[(exp,co['method'],stage)]+=1
        base=stages['method']['values'];status=base.get('update_detection_auc_status','absent_status')
        if status=='computed': assert base['update_detection_auc'] is not None and 0<=base['update_detection_auc']<=1
        elif status=='missing_original_predictions': assert base['update_detection_auc'] is None and stages['utility']['values']['f1_before'] is None
        stat[(co['method'],status)]+=1;statuses[(exp,co['method'],status)]+=1
        status_rows.append(dict(meta,update_detection_auc=base.get('update_detection_auc'),status=status))
        if co['method']=='Retrain':
            assert 'post_unlearning_flip_hop' not in stages
            continue
        assert 'post_unlearning_flip_hop' in stages
        f=stages['post_unlearning_flip_hop'];v=f['values'];pr=f['identity']['protocol']
        assert pr['comparison']=='argmax_gu_vs_same_request_retrain_first_index_ties'
        assert pr['evaluation_mask']=='test_mask_excluding_selected_nodes'
        assert pr['hop_graph']=='bound_pre_deletion_edge_index'
        assert pr['grouping']=='undirected_multi_source_shortest_distance_1_2_3_gt3_or_unreachable'
        assert f['identity']['unlearning_output']==c['output']
        assert f['baseline_output']==f['identity']['retrain_output']==retrains[request_key(c)]
        protocols[(pr['version'],pr['hop_graph'],pr['grouping'])]+=1
        counts=[v[b+'_hop_count'] for b in ['1','2','3','gt3']];flips=[v[b+'_hop_flipped_count'] for b in ['1','2','3','gt3']]
        assert sum(counts)==v['node_count'] and sum(flips)==v['flipped_count']
        assert abs(v['fraction_flipped']-sum(flips)/sum(counts))<1e-12
        for band,count,changed in zip(['1','2','3','gt3'],counts,flips):
            assert 0<=changed<=count
            rate=v[band+'_hop_flip_rate']
            assert (rate is None and count==0) or (count>0 and abs(rate-changed/count)<1e-12)
            empty+=int(count==0)
            hop.append(dict(meta,band=band,nodes=count,flipped=changed,rate_pct=None if rate is None else 100*rate,
                            test_nodes=sum(counts),test_disagreements=sum(flips),node_share_pct=100*count/sum(counts)))
        geometry={'test_nodes':sum(counts),'hop1_count':counts[0],'hop2_count':counts[1],'hop3_count':counts[2],'gt3_count':counts[3],
                  'within2_share_pct':100*sum(counts[:2])/sum(counts),'hop1_share_pct':100*counts[0]/sum(counts),
                  'gt3_share_pct':100*counts[3]/sum(counts)}
        gkey=(exp,co['dataset_name'],source,selector,co['budget_ratio'],co['training_seed'],co.get('random_selector_seed'),co.get('im_selector_seed'),c['selection_id'])
        assert geom.setdefault(gkey,geometry)==geometry
        raw.append(dict(meta,overall_D_pct=100*v['fraction_flipped'],
                        one_hop_D_pct=None if counts[0]==0 else 100*flips[0]/counts[0],
                        far_D_pct=None if counts[3]==0 else 100*flips[3]/counts[3],
                        local_minus_far_pp=None if counts[0]==0 or counts[3]==0 else 100*flips[0]/counts[0]-100*flips[3]/counts[3],
                        within2_disagreement_share_pct=None if sum(flips)==0 else 100*sum(flips[:2])/sum(flips),
                        **geometry))
        local_hop+=1
    coverage.append({'experiment':exp,'run_id':rid,'cells':ncell,'gu_with_hop':local_hop,'retrain_hop_not_applicable':ncell-local_hop,
                     'empty_hop_bands':empty,'update_detection':[{'method':k[0],'status':k[1],'cells':v} for k,v in sorted(stat.items())]})

# Average request draws inside training seed; do not multiply n by request repeats.
KEYS=['experiment','dataset','method','source','selector','ratio','band']
seed_groups=defaultdict(list)
for r in hop:seed_groups[tuple(r[k] for k in KEYS)+ (r['seed'],)].append(r)
seed=[]
for key,items in seed_groups.items():
    rates=[r['rate_pct'] for r in items if r['rate_pct'] is not None]
    seed.append(dict(zip(KEYS+['seed'],key),request_draws=len(items),nonempty_draws=len(rates),
                     rate_pct=None if not rates else mean(rates),mean_nodes=mean(r['nodes'] for r in items),
                     mean_node_share_pct=mean(r['node_share_pct'] for r in items),
                     pooled_draw_rate_pct=None if sum(r['nodes'] for r in items)==0 else 100*sum(r['flipped'] for r in items)/sum(r['nodes'] for r in items)))
summary=[];groups=defaultdict(list)
for r in seed: groups[tuple(r[k] for k in KEYS)].append(r)
for key,items in groups.items():
    rates=[r['rate_pct'] for r in items if r['rate_pct'] is not None]
    summary.append(dict(zip(KEYS,key),training_seed_count=len(items),nonempty_training_seed_count=len(rates),
                        rate_mean_pct=None if not rates else mean(rates),rate_sd_pp=None if len(rates)<2 else stdev(rates),
                        mean_nodes=mean(r['mean_nodes'] for r in items),mean_node_share_pct=mean(r['mean_node_share_pct'] for r in items)))

geoms=[]
for key,v in geom.items():
    fields=['experiment','dataset','source','selector','ratio','seed','random_seed','im_seed','selection_id']
    geoms.append(dict(zip(fields,key),**v))
gseed=defaultdict(list)
for r in geoms:gseed[tuple(r[k] for k in ['experiment','dataset','source','selector','ratio','seed'])].append(r)
gs=[]
for key,items in gseed.items():
    gs.append(dict(zip(['experiment','dataset','source','selector','ratio','seed'],key),request_draws=len(items),
                   **{f:mean(r[f] for r in items) for f in ['test_nodes','hop1_share_pct','within2_share_pct','gt3_share_pct']}))
gg=defaultdict(list)
for r in gs:gg[tuple(r[k] for k in ['experiment','dataset','source','selector','ratio'])].append(r)
gsummary=[]
for key,items in gg.items():
    gsummary.append(dict(zip(['experiment','dataset','source','selector','ratio'],key),training_seed_count=len(items),
                        **{f:mean(r[f] for r in items) for f in ['test_nodes','hop1_share_pct','within2_share_pct','gt3_share_pct']}))

csv_write('hop_cells.csv',hop);csv_write('hop_seed_values.csv',seed);csv_write('hop_summary.csv',summary)
csv_write('request_geometry.csv',geoms);csv_write('request_geometry_summary.csv',gsummary)
csv_write('locality_cells.csv',raw);csv_write('update_detection_coverage.csv',status_rows)
old080=list(csv.DictReader((ROOT/'self/research/analyses/EXP-080/full-20261021/hop_summary.csv').open(encoding='utf-8')))
new080={(r['dataset'],r['method'],r['selector'],r['ratio'],r['band']):r for r in summary if r['experiment']=='EXP-080'}
assert len(old080)==len(new080)
for r in old080:
    n=new080[r['dataset'],r['method'],r['selector'],float(r['ratio']),r['band']]
    assert abs(float(r['rate_mean'])-n['rate_mean_pct'])<1e-10
    assert abs(float(r['nodes_mean'])-n['mean_nodes'])<1e-10
audit={'passed':True,'metric_files_hash_verified':len(status_rows),'gu_with_hop':len(raw),'hop_band_rows':len(hop),
       'geometry_rows_without_repeated_method_coordinates':len(geoms),'source_runs':source_hashes,'coverage':coverage,
       'exp080_existing_hop_summary_rows_recomputed':len(old080),
       'stage_inventory':[dict(experiment=k[0],method=k[1],stage=k[2],cells=v) for k,v in sorted(stage_inventory.items())],
       'protocols':[dict(version=k[0],hop_graph=k[1],grouping=k[2],cells=v) for k,v in protocols.items()],
       'update_detection_status_counts':[dict(experiment=k[0],method=k[1],status=k[2],cells=v) for k,v in sorted(statuses.items())],
       'semantics':'GU vs same-request Retrain argmax disagreements, on fixed retained test nodes; distances on pre-deletion undirected graph. Not GU-vs-Original collateral damage. >3 includes unreachable. Empty bands retain null rates.',
       'limits':'The underlying predictions and Dataset remain remote. This audits persisted counts/ratios, exact output pairing, run/delivery/trusted-index hashes; it does not recompute per-node BFS or probabilities from raw tensors. Runs remain separate; overlapping011/079 are not pooled independent samples.'}
json_write('HOP_VALIDATION.json',audit)
geometry_table=[]
for dataset in ['Cora','CiteSeer','PubMed']:
    for selector in ['random','degree','r_point','gt_full','rr_65536']:
        r=next(r for r in gsummary if r['experiment']=='EXP-011' and r['dataset']==dataset and r['selector']==selector)
        geometry_table.append('| '+dataset+' | '+selector+' | '+' | '.join(f'{r[k]:.2f}' for k in ['hop1_share_pct','within2_share_pct','gt3_share_pct'])+' |\n')
local_table=[]
for dataset in ['Cora','CiteSeer','PubMed']:
    for method in ['GIF','GNNDelete','MEGU','GraphEraser','GraphRevoker']:
        values=[]
        for selector in ['random','r_point','gt_full','rr_65536']:
            values.append(' / '.join(f'{next(r for r in summary if r["experiment"]=="EXP-011" and r["dataset"]==dataset and r["method"]==method and r["selector"]==selector and r["band"]==band)["rate_mean_pct"]:.2f}' for band in ['1','gt3']))
        local_table.append('| '+dataset+' | '+method+' | '+' | '.join(values)+' |\n')
report='''# Hop / locality 与 update-detection 覆盖补充审查

**Hop分层已真实计算，详细提纲遗漏了一层可直接分析的空间响应证据。** 本轮从当前e11r1/e79r6及EXP080三个采用批次逐格读取5,985份metrics，逐一验证run、delivery manifest及trusted index SHA，以及同请求Retrain完整Output引用。5,124个GU配对都有1/2/3/>3-hop的分母、分歧数、分歧率；全部20,496个分层非空，分层计数相加严格还原总D。没有只凭case名称判为完成。

| 实验/批次 | GU有完整Hop | Retrain不适用 | GU update-detection computed | Retrain missing_original_predictions |
|---|---:|---:|---:|---:|
| EXP011 / e11r1 | 1,242 | 207 | 1,242 | 207 |
| EXP079 / e79r6 | 2,160 | 360 | 2,160 | 360 |
| EXP080 / e80r305+r302+r306 | 1,722 | 294 | 1,722 | 294 |

011/079有重叠请求和训练seed，这些是字段覆盖计数，不能求和为5,124个独立科学样本。080保持旧分片协议，新011/079保持新loss+300轮协议，分别分析。

## 指标真实含义与缺失

- `experiments/flip_hop_metrics.py:27–37,40–68`：在原图edge_index上计算到删除集合的**无向、多源最短距离**；按1、2、3、>3（含不可达）分组。测试mask排除选中节点，比较GU与同请求Retrain的argmax类别。距离图与预测图语义分开保存。
- `1_hop_count / 1_hop_flipped_count / 1_hop_flip_rate`等四组字段俱全；`fraction_flipped`是整体GU–Retrain分歧。它不是GU相对Original的翻转，也不是遗忘节点成员泄漏，不应直接命名为collateral damage。
- 全部GU更新检测AUC已为computed且数值合法；全部Retrain是missing_original_predictions，值与before均为null。`experiments/output_metrics.py:31–47`实际比较原模型/删后概率向量的L2变化，用selected nodes为正、test nodes为负，按n=min(二组数量)取各自前n个。不是随机匹配采样或通用MIA。不能因Retrain缺before而声称所有GU更新检测都没计算。
- 本批metrics没有节点到shard/partition的交叉分母与分歧数。GraphRevoker的GPA+optimal方法名和num_shards元数据不等于有空间分区响应。现有本地metrics可以做hop分析；按实际分片归属归因需要独立可核验的assignment/Output证据。

## 新提取：请求覆盖几何

下表仅用EXP011/e11r1、10%预算，Random十抽样和IM三抽样先在各训练seed内平均，再对3个训练seed等权；geometry按请求去重方法坐标，不重复计六份相同分母。百分数是测试节点落入相应距离带的比例，**不是IC传播概率或RR覆盖估计**。

| 数据集 | selector | 1-hop测试节点% | <=2-hop测试节点% | >3-hop测试节点% |
|---|---|---:|---:|---:|
'''+''.join(geometry_table)+'''

IM-RR65536的测试节点两跳覆盖在Cora/CiteSeer/PubMed为83.52/59.81/86.49%，R-point为53.32/37.34/57.75%。这说明不同请求使测试节点处于不同的几何暴露范围，提供“传播导向选点与局部梯度选点构成不同空间请求”的描述性支撑。但它不能独立证明IM实现优化了IC扩散目标，也不证明更广覆盖导致更大GU损害。Degree在Cora/PubMed的一跳覆盖还更高，故不能称其为IM独有结构。

## 新提取：完整方法面板的局部分歧

每格为 **1-hop D / >3-hop D (%)**，仍是EXP011/e11r1、10%和3训练seed均值；所有请求重复先在训练seed内平均。GIF/IDEA近重复，表中只显示GIF；完整CSV仍保留IDEA、PageRank和三RR规模，以及079所有source、080所有预算。

| 数据集 | GU | Random | R-point | D-full | IM-RR65536 |
|---|---|---:|---:|---:|---:|
'''+''.join(local_table)+'''

可供写作检验的候选认识：在Cora，R-point对GIF/GNNDelete/MEGU的1-hop D为26.87/52.61/21.59%，>3-hop均约0.25%；IM对应1-hop为3.63/26.14/4.53%、远处约0。分片方法则有明显远处背景分歧：GraphEraser在R-point/IM的>3-hop D为9.86/14.54%，GraphRevoker为18.63/14.08%。CiteSeer同样要保留分片的远处分歧，PubMed MEGU等条件还存在远处高于近处的反例。**不能把全方法面板概括为分歧仅局部传播。** 分片与单GCN Retrain的架构差异仍在背景D中。

这些数据支持把“几何覆盖广度”与“条件距离带内的分歧强度”分开，而不是用一个整体D解释空间机制。跨selector的hop组成员不相同、分母不同；在更大预算下大批测试节点会移入近距离带，曲线变化也可能受组构成影响。当前数据没有给出因果中介/反事实对照，不能宣布IM传播机制或IF局部机制已被因果验证。

## 对提纲与后续分析的建议

1. 在R0“请求差异”或附录B加入紧凑的**测试节点距离分布**表，补选集overlap以外的结构差异；使用“two-hop reach of the request”而非IC spread。
2. 在Q2或附录D加入**按hop分层的GU–Retrain分歧**图，必须同时给节点占比/分母。可用3数据集×5去重方法、selector不同颜色的1/2/3/>3带剖面；完整矩阵已经可从本目录CSV生成，无需GPU补算。
3. 若主文空间不足，只在机制解释段给一个严格限定的近/远对照，并指向全矩阵附录。不能只展示Cora/GIF而忽略分片远处背景与PubMed的反例。
4. 当前只能称“空间分层响应”或“locality diagnostic”；GU–Original collateral、概率距离、实际shard assignment、重复Ret自然变化仍需其各自证据。update-detection已有值，但不应为了填隐私主题将它升级成MIA结论。

## 复核材料与统计层级

- `hop_cells.csv`：20,496行，每个原始GU×四距离带的nodes/flipped/rate及完整坐标。
- `hop_seed_values.csv`：先在训练seed内对请求draw等权平均；另保留按draw节点数合并的比率供敏感性检查，两者不混用。
- `hop_summary.csv`：每条件训练seed均值/样本SD、有效seed数及节点分母；没有把节点或draw当作独立seed。
- `request_geometry.csv`、`request_geometry_summary.csv`：对方法坐标去重后的请求结构；<=2-hop是几何描述。
- `locality_cells.csv`：每cell的1-hop/远处D、差值及<=2-hop分歧份额；零分歧时份额保留null。
- `update_detection_coverage.csv`：5,985个cell的状态与AUC，缺失原预测明确保留。
- `HOP_VALIDATION.json`：来源SHA、5,985 metrics哈希/精确baseline/分子分母检查、全部case覆盖；080既有hop_summary每行均独立重算一致。没有重新加载正式Dataset或远端预测张量，因此未声称本轮重算了逐节点BFS/概率，只审计可信持久化计数与协议。

本轮仅本地CPU读取与生成分析，科学接受状态未改变。
'''
(OUT/'HOP_REPORT.md').write_text(report,encoding='utf-8')
print(json.dumps({'metric_files':len(status_rows),'gu_hop_pairs':len(raw),'hop_rows':len(hop),'empty_bands':sum(r['nodes']==0 for r in hop),'coverage':coverage},ensure_ascii=False))
