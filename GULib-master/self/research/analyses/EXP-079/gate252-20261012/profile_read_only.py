import os,sys,json,cProfile,pstats,time
from pathlib import Path
root=Path('/autodl-fs/data/OpenGU/GULib-master');os.chdir(root);sys.path.insert(0,str(root))
from cache_v2 import CacheIndex,ArtifactType,ArtifactRecipe,ProducerVersion
from cache_v2.runtime import _decode_exact_mapping
from experiments.artifact_producer import FormalArtifactRequest,resolve_formal_artifact
idx=CacheIndex(root/'results/cache_v2/index.sqlite')
with idx.read_session():
 rec=idx.get_artifact('eval_908e3612_adf27d5a')
 wrapper=_decode_exact_mapping(rec['recipe'],'evaluation')
 recipe=ArtifactRecipe(wrapper['fields'],recipe_version=wrapper['recipe_version'])
 producer=ProducerVersion(**recipe.fields['producer_version'])
 request=FormalArtifactRequest(ArtifactType.EVALUATION,recipe,producer)
 t=time.perf_counter();hit=resolve_formal_artifact(root/'results/cache_v2',request);wall=time.perf_counter()-t
 assert hit.artifact_id=='eval_908e3612_adf27d5a'
 prof=cProfile.Profile();prof.enable();hit=resolve_formal_artifact(root/'results/cache_v2',request);prof.disable()
 st=pstats.Stats(prof);rows=[]
 for (fn,ln,name),(cc,nc,tt,ct,callers) in st.stats.items():
  rows.append({'file':fn,'line':ln,'name':name,'primitive_calls':cc,'calls':nc,'self_seconds':tt,'cumulative_seconds':ct})
 print(json.dumps({'scope':'One exact Evaluation HIT, read-only, current production Store, before warm runner start; cProfile time is perturbed','artifact_id':'eval_908e3612_adf27d5a','unprofiled_wall_seconds':wall,'profiled_total_seconds':st.total_tt,'top_cumulative':sorted(rows,key=lambda r:r['cumulative_seconds'],reverse=True)[:30],'top_self':sorted(rows,key=lambda r:r['self_seconds'],reverse=True)[:20]}))
