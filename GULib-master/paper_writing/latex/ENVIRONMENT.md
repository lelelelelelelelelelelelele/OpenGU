# 本地 LaTeX 环境与模板验证

日期：2026-10-24（Asia/Shanghai）。状态：**本地命令行编译通过，可以在提纲审查后开始第一版论文写作。** 当前 `main.tex` 仅包含环境验证内容，未撰写新的科研正文。

## 1. 已使用的环境

本机已有 TeX Live 2026，位于 `E:\Programs\texlive\2026\bin\windows`，这些命令已在当前终端的 PATH 中。没有重复安装发行版，也没有修改系统环境变量。

| 项目 | 核验结果 |
|---|---|
| pdfLaTeX | pdfTeX 3.141592653-2.6-1.40.29，TeX Live 2026 |
| BibTeX | 0.99e，TeX Live 2026 |
| latexmk | 4.87，2025-06-15 |
| XeLaTeX | XeTeX 3.141592653-2.6-0.999998，可用；本轮构建使用 pdfLaTeX |
| LuaLaTeX | LuaHBTeX 1.24.0，可用；本轮构建使用 pdfLaTeX |
| ACM 文档类 | `acmart.cls`，2025-08-27 v2.16 |
| ACM 参考文献样式 | `ACM-Reference-Format.bst`，已通过 `kpsewhich` 定位 |
| 模板依赖 | `amsmath`、`amsfonts`、`bm`、`booktabs`、`graphicx`、`microtype`、`xcolor` 均由实际编译加载成功 |

## 2. 模板来源与保留范围

来源是此前已经从 Overleaf 同步的 [main.tex](../../report/paper/overleaf/main.tex)。本轮没有再次访问 Overleaf，也没有修改这个来源目录。沿用的设置如下：

```tex
\documentclass[sigconf,anonymous,review]{acmart}
\setcopyright{none}
\settopmatter{printacmref=false}
\acmConference[WWW '27]{The ACM Web Conference 2027}{May 10--14, 2027}{Dublin, Ireland}
\acmYear{2027}
\copyrightyear{2027}
\acmDOI{}
\acmISBN{}
\bibliographystyle{ACM-Reference-Format}
```

`math_commands.tex` 和 `references.bib` 按原文件字节复制。`main.tex` 仅保留模板设置并加入显式标识的环境验证内容，避免把旧稿视为已审查的新正文。

来源目录当前含未提交修改，因此观察时的仓库 HEAD `57c5f21c0403d9d6f34dc27b82051c624b62e161` 只用于说明仓库上下文，不能代表这些来源文件的精确内容。精确来源以 [template-source.json](template-source.json) 中的 17 个文件 SHA-256 为准。

| 来源文件 | SHA-256 |
|---|---|
| `main.tex` | `44b4099f5d79c8db3e6574bef346afbbc02d1b0fdd8217df6e0dd139379f2d27` |
| `math_commands.tex` | `ab6c49175eeb9cd4d4d8c02405785f8b18c82aa81f25490b0708c902106bba3d` |
| `references.bib` | `3e7d9e5958113b89264cb758baaa721369f081807e24bd8ea6e964665a4f0e97` |

## 3. 一条命令构建

在仓库根目录运行：

```powershell
.\paper_writing\tools\build-paper.ps1
```

构建脚本通过 `latexmk` 调用 pdfLaTeX 和 BibTeX，直到引用稳定；本轮首次构建实际执行了三遍 pdfLaTeX 和 BibTeX。所有输出进入 Git 忽略的 `paper_writing/latex/build/`。默认关闭 shell escape。脚本遇到编译失败、缺失 PDF、未解析的引用或交叉引用会返回失败。

可选：同时用当前 Overleaf 完整稿核验模板依赖：

```powershell
.\paper_writing\tools\build-paper.ps1 -ValidateOverleaf
```

完整稿的输入仍来自 `report/paper/overleaf/`，输出独立进入 `paper_writing/latex/build/overleaf-validation/`；此操作不会把旧稿内容复制到新写作项目。脚本只为当前子进程设置 Perl 可识别的 `LC_ALL=C`，结束后恢复原值。

## 4. 验证结果

| 验证对象 | 结果 | 说明 |
|---|---|---|
| 新写作项目 `main.tex` | 通过，1 页 | 0 编译错误；0 未定义引用；0 overfull/underfull 警告 |
| 数学宏与公式 | 通过 | AMS、粗体数学宏、带编号公式正常 |
| 图、表、交叉引用 | 通过 | 图表编号和三个交叉引用正常；单页 PNG 已查看，无截断或重叠 |
| BibTeX | 通过 | 示例引用解析为 `[1]`，参考文献正常输出 |
| 当前完整 Overleaf 稿 | 通过，12 页 | 0 编译错误；0 未定义引用；实际 PDF 图像依赖加载成功 |
| 输出隔离 | 通过 | `git check-ignore` 确认生成的 PDF 被 `paper_writing/.gitignore` 排除 |

查看产物：

- [环境验证 PDF](build/main.pdf)
- [环境验证截图](build/preview.png)
- [环境验证最终日志](build/main.log)
- [完整 Overleaf 本地编译 PDF](build/overleaf-validation/main.pdf)
- [完整 Overleaf 最终日志](build/overleaf-validation/main.log)

## 5. 已知警告与写稿前处理项

环境已具备完整的本地构建能力。以下警告来自现有模板或文献数据，需要在论文收口时处理：

- 环境验证引用的 `chen2022graph` 缺 publisher、address、页码三个 BibTeX 字段；完整原稿共 57 条同类 BibTeX 警告。没有擅自补写未核实的文献元数据。
- `epstopdf` 提醒 shell escape 已关闭。本轮输入的图为 PDF，无需启用；这不影响构建。
- 完整原稿保留了 Overleaf 当前的 `printacmref=false` 和未提供 CCS 的状态，触发 2 条 ACM 类警告。投稿最终设置需在正式正文收口时统一核对。
- 完整原稿存在 7 处 overfull hbox 和 6 处 underfull vbox。它们属于原稿排版问题，与环境缺依赖无关。
- 本机 ACM 类由现有 TeX Live 提供。云端的 TeX Live 或 ACM 类版本尚未在本轮查询，不能承诺本地和云端分页逐字一致。

用户审查提纲后，再将通过审查的章节内容与图表接入此项目。本轮没有生成第一版研究正文，也没有提交 Git、覆盖云端稿或安装额外软件。
