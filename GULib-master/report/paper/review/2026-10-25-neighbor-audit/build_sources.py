"""Record primary sources and local claim/evidence identities for this audit."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
downloads = json.loads((ROOT / 'tmp/pdfs/neighbor-audit-20261025/DOWNLOADS.json').read_text(encoding='utf-8'))
by_id = {r['id']: r for r in downloads}
specs = [
    ('jain-iclr2026', 'Is Graph Unlearning Ready for Practice?', 'ICLR 2026 proceedings', 'Def.2.3; section 4 Eq.2; sections 5.5-5.6; Fig.2; Table10'),
    ('wichert-emnlp2024', 'Rethinking Evaluation Methods for Machine Unlearning', 'Findings EMNLP 2024 proceedings', 'sections 3.1-3.3, 4.4-4.5; Tables2-3'),
    ('mgu-v1', 'Re-understanding Graph Unlearning through Memorization', 'arXiv 2601.14694v1', 'sections 4.2-4.4; Fig.4; Eq.5/16'),
    ('rum-neurips2024', 'What Makes Unlearning Hard and What to Do About It', 'NeurIPS 2024 proceedings', 'sections 4-5; Fig.1'),
    ('attack-unlearning-v1', 'Attack by Unlearning: Unlearning-Induced Adversarial Attacks on GNN', 'arXiv 2603.18570v1', 'sections 4.1 and 6; Appendix E'),
    ('deletion-requests-v1', 'Modeling Deletion Requests in Machine Unlearning', 'arXiv 2610.04310v1', 'sections VII-A/C/D.3; Figs4-5'),
]
papers = []
for identity, title, version, locations in specs:
    item = dict(by_id[identity], title=title, version=version, locations=locations, access='official public PDF; text extracted; decisive pages inspected')
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256']
    papers.append(item)
papers += [
    dict(id='challenging-forgets-v4', title='Challenging Forgets: Unveiling the Worst-Case Forget Sets in Machine Unlearning', version='arXiv 2403.07362v4 (author manuscript for ECCV2024)', url='https://arxiv.org/html/2403.07362v4', locations='sections 4-5; Appendix C.4; FigsA1-A2', access='primary author HTML; ECVA PDF exceeded web tool size limit'),
    dict(id='unlearn-burn-v1', title='Unlearn and Burn: Adversarial Machine Unlearning Requests Destroy Model Accuracy', version='arXiv 2410.09591v1', url='https://arxiv.org/html/2410.09591v1', locations='section 4.2 Fig.5; section 5.1; Appendix B.3', access='primary author HTML; OpenReview verification page prevented reading that version'),
]
worktree = Path('C:/Users/ADMIN/.codex/worktrees/paper-reentry-v1/OpenGU/GULib-master')
claim_files = [Path('E:/project/OpenGU-DocMap/40_论文写作/06_结果.md')]
claim_files += [worktree / 'paper_writing/review/2026-10-25-reentry' / name for name in ['CORE_ARGUMENT.md', 'OUTLINE.v10.1.md', 'POST_REVIEW.md', 'REVIEW_INPUTS.json']]
claim_files += [ROOT / 'report/paper/review/2026-10-25-reentry/XLX_PROGRESS_REPORT.md']
local = [dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), role='claim/version locator; not evidence of neighbor coverage') for p in claim_files]
audit = json.loads((HERE / 'ARITHMETIC_AUDIT.json').read_text(encoding='utf-8'))
fig4 = json.loads((HERE / 'FIG4_ARITHMETIC.json').read_text(encoding='utf-8'))
scalar_evidence = audit['inputs'] + [dict(path=fig4['input'], sha256=fig4['input_sha256'])]
result = dict(date='2026-10-25', scope='Independent primary-paper comparison; no code replication or exhaustive novelty search; no scientific acceptance', papers=papers, local_claim_locators=local, scalar_evidence=scalar_evidence, conference_requirements=dict(url='https://www2027.thewebconf.org/research-track-papers/', locations='Security and Privacy scope; Web relevance; main/total page limits'), unresolved=['Neighbor implementations not independently replicated', 'Preprint versions not silently treated as final proceedings', 'EXP079 actual cross-source Target weight identity not proven by this scalar audit'])
(HERE / 'SOURCES.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Verified 6 PDF hashes; recorded 8 primary papers and local input identities.')
