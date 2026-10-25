# 论文分块审阅台

在仓库的 `GULib-master` 目录启动（Python 标准库、TeX Live 的 `pdflatex` 与 Poppler 的 `pdftoppm`）：

```powershell
python -B -X utf8 -m scripts.paper_review.server --state-dir <持久记录目录> --port 8129
```

打开 `http://127.0.0.1:8129`。`--state-dir` 必须放在论文源码目录外；其中
`reviews.jsonl` 保存意见、修改原因、源码快照和前后差异，`cloud.json` 与
`cloud-latest.zip` 保存同步核验记录。备份此目录可保留审阅历史。
`preview/` 是可重新生成的编译缓存。正文只保存在 LaTeX 中。

Fig3 与 Fig4 通过 `sections/results.tex` 的现有 subsection 标题定位；
EXP-014 使用 `sections/selector_cost.tex`。修改后刷新会从当前 LaTeX 编译；
保存时使用文件版本检查，拒绝覆盖已经被外部编辑更新的源码。
意见绑定提交时的源码版本与快照。Git diff 提供相对 HEAD 的全文修改，
历史意见中的 diff 提供逐次修改。独立预览适配浮动位置，不代替投稿全文排版检查。

## Overleaf 同步

1. 在页面链接指向的既有 Overleaf 项目中下载最新源码 ZIP，并在审阅台选择“检查最新云端源码 ZIP”。页面列出差异与云端独有文件。
2. 检查后才能下载差异包。后续云端快照相对基线有变化时，导出被阻止；选择“取回云端修改并合并”。工具通过 Git 三方合并保留双方独立修改，遇到冲突会拒绝本次全部源码写入；此时在源码中解决冲突，再重新检查。云端新文件和未冲突修改会被取回，云端删除会在本地无修改时对应移除；此前快照仍保留在核验目录中。
3. 上传前再次下载云端源码核对。将差异包中的文件上传至项目的对应路径；不能把 ZIP 作为普通附件留在项目里。工具不自动上传或删除云端文件。云端独有文件不会被打包删除。
4. 上传后重新编译，检查日志和 PDF，再次下载源码。只有实际逐文件一致且实际核对编译结果后，才能通过 `Cloud.verify` 写入明确的核验回执。接口有意不提供普通“标记已同步”按钮。

“已同步”只描述回执所列时间点。后续本地变化立即撤销该显示；后续云端变化
须通过重新下载检查发现。下载 ZIP 本身不证明成功编译；没有核验回执时显示未验证。
源 ZIP 来自用户选择，项目身份由操作者在既有项目页面核对，工具不将任意 ZIP 当成已认证云端会话。

核验回执（在实际核对后，从 Python 调用）：

```python
from pathlib import Path
from scripts.paper_review.model import Desk
from scripts.paper_review.sync import Cloud
desk = Desk(Path('report/paper/overleaf'), Path('<同一持久记录目录>'))
Cloud(desk).verify(Path('<上传后重新下载的源码ZIP>').read_bytes(),
                   '<本项目实际编译PDF的下载地址>',
                   '<实际观察到的错误数、页数与版面核对结果>')
```

EXP-014 生成器只改 `selector_cost_rows.tex`，不改手写叙述。
RR65536 的两小时超时、6–8 小时估计及 selector-only 边界保留。
