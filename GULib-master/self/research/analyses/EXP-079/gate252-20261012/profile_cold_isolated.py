import os,sys,json,cProfile,pstats,tempfile,time
from pathlib import Path
root=Path('/autodl-fs/data/OpenGU/GULib-master');os.chdir(root);sys.path.insert(0,str(root))
from cache_v2 import CacheIndex,ArtifactType,ArtifactRecipe,ProducerVersion,ArtifactHeader
from cache_v2.runtime import _decode_exact_mapping
from cache_v2.formal_store import FormalArtifactStore
from cache_v2.output_evaluation import OutputEvaluationPayload
from experiments.artifact_producer import FormalArtifactRequest,resolve_formal_artifact,store_formal_artifact
source=root/'results/cache_v2';idx=CacheIndex(source/'index.sqlite')
def recipe_for(rec):
 w=_decode_exact_mapping(rec['recipe'],'recipe');return ArtifactRecipe(w['fields'],recipe_version=w['recipe_version'])
def profile_rows(prof):
 st=pstats.Stats(prof);rows=[]
 for (fn,ln,name),(cc,nc,tt,ct,callers) in st.stats.items():rows.append({'file':fn,'line':ln,'name':name,'calls':nc,'self_seconds':tt,'cumulative_seconds':ct})
 return {'total_seconds':st.total_tt,'top_self':sorted(rows,key=lambda x:x['self_seconds'],reverse=True)[:20],'top_cumulative':sorted(rows,key=lambda x:x['cumulative_seconds'],reverse=True)[:25]}
results=[]
with idx.read_session():
 for label,aid in {'base': 'eval_2ac8154d_93b79103', 'post_unlearning_utility_and_retrain_gap': 'eval_0bad760d_c86ef369', 'post_unlearning_flip_hop': 'eval_908e3612_adf27d5a'}.items():
  rec=idx.get_artifact(aid);recipe=recipe_for(rec);producer=ProducerVersion(**recipe.fields['producer_version']);req=FormalArtifactRequest(ArtifactType.EVALUATION,recipe,producer)
  value=resolve_formal_artifact(source,req);assert value.artifact_id==aid
  records={};edges=[]
  def visit(parent):
   if parent in records:return
   r=idx.get_artifact(parent);records[parent]=r
   with idx._read_connection() as conn:links=conn.execute('SELECT parent_artifact_id,relation FROM dependencies WHERE child_artifact_id=?',(parent,)).fetchall()
   for link in links:
    visit(link['parent_artifact_id']);edges.append((link['parent_artifact_id'],parent,link['relation']))
  for rel,parent in value.payload.dependencies:visit(parent)
  with tempfile.TemporaryDirectory(prefix='exp079-cold-profile-',dir=root/'.syncmate') as tmp:
   target=Path(tmp);assert target.parent==root/'.syncmate' and target!=source
   store=FormalArtifactStore(target,producer_version=producer);store.initialize()
   with store.index.transaction() as writer:
    for r in records.values():
     writer.register_artifact(ArtifactHeader(artifact_type=r['artifact_type'],recipe=recipe_for(r),content_hash=r['content_hash'],producer_version=ProducerVersion(**_decode_exact_mapping(r['producer_version'],'producer')),status=r['status'],verification_status=r['verification_status'],artifact_id=r['artifact_id'],semantic_path=r['semantic_path'],compute_seconds=r['compute_seconds'],created_at=r['created_at'],metadata=_decode_exact_mapping(r['metadata'],'metadata')))
    for parent,child,rel in edges:writer.add_dependency(parent,child,relation=rel)
   assert store.index.find_artifact(ArtifactType.EVALUATION,recipe.recipe_hash) is None
   prof=cProfile.Profile()
   with store.index.read_session():
    start=time.perf_counter();prof.enable()
    payload=OutputEvaluationPayload(recipe.fields['evaluation_identity'],value.payload.values)
    saved=store_formal_artifact(target,req,payload,compute_seconds=0)
    prof.disable();elapsed=time.perf_counter()-start
    assert not saved.hit and saved.artifact_id==aid and saved.content_hash==value.content_hash
    checked=resolve_formal_artifact(target,req);assert checked.artifact_id==aid
   results.append({'case':label,'artifact_id':aid,'isolated_cold_write_seconds':elapsed,'dependency_records':len(records),'dependency_edges':len(edges),'payload_bytes':len(payload.canonical_bytes),'profile':profile_rows(prof)})
  assert not target.exists()
print(json.dumps({'scope':'Three exact Cora Evaluation payloads written once each through normal Store API into disposable metadata-only fixture Stores on the same filesystem; source Store read-only. Small indexes, not production-sized cold benchmark. Profile perturbs time. Ancestor metadata registered through API; no source artifacts modified. Temporary fixture Stores removed.','results':results}))
