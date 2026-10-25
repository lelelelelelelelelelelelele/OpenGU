# Code and private research repositories

Code remains at `E:/project/OpenGU` (`GULib-master` is the project subdirectory). Independent research lives at `E:/project/OpenGU-research`; [its entry](E:/project/OpenGU-research/README.md) owns manuscript, analysis and scientific navigation. Formal datasets, Cache V2, results and SSH checkout stay at their existing locations.

Code Git owns training/GU/selectors/metric definitions, cache/runners, SyncMate adapters, software tests, formal execution YAML and submission Recipes. Research Git owns paper/analysis/figure generators and scientific decisions; their recorded execution SHA is always the actual run's code SHA. Research commits never enter private-bundle readiness identity.

Rebuild Work Plan from code tools, supplying both explicit roots:

```powershell
python -B -X utf8 scripts/dashboard/gen_research_overview.py --canonical-root E:/project/OpenGU/GULib-master --research-root E:/project/OpenGU-research --check-links
```

`--canonical-root` reads runtime evidence and referenced WorkItems. `--research-root` reads current experiment records, saved analyses and navigation, and owns generated pages. YAML is read from the tool's code checkout. Neither source path is inferred from the other; missing research does not fall back to retired code-owned research paths. SSH run/submit commands never call this presentation tool.

Historical code Git retains original execution SHAs. No history rewriting or public push is part of this change; removing current research files cannot make old commits safe to publish. Private delivery continues to require exact local code main / verified bundle / SSH main alignment. Changes to scientific YAML, Recipes or algorithms still require their normal review, code commit and preflight.
