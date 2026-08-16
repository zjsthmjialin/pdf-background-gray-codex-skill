# dsh-pdf-background-gray

「Remove PDF Background Gray」技能的 **DeepSeek Harness (DSH) 插件化分发包**。

安装后自动向 DSH 技能系统注册 `remove-pdf-background-gray` 技能：去除扫描 PDF 的灰色/米白底色，**保持原始分辨率、页面几何与抗锯齿文字边缘**（不做硬阈值/二值化、不重采样、无损 Flate 压缩）。

## 安装

```sh
dsh plugin --profile web add dsh-pdf-background-gray
```

重启 DSH Web 后，向 Agent 说"把这份扫描 PDF 去底灰"即自动走技能工作流。

## 运行时要求（Python）

- Python 3.10+
- `python -m pip install pypdf Pillow numpy`

## 用法（技能内嵌，直接给 agent 即可）

```sh
python scripts/remove_pdf_background_gray.py INPUT.pdf OUTPUT.pdf
# 深色纸张：--low 235 --white-point 250
```

## 内容

- `SKILL.md`：工作流与护栏（pdfinfo 检查 → 直改图像对象 → 验证）
- `scripts/remove_pdf_background_gray.py`：核心脚本（单文件，124 行）

## 发布 / 维护

```sh
npm pack --dry-run
npm publish
```

维护纪律：技能本体改动 → 同步 `skills/remove-pdf-background-gray/` 快照 → 版本迭代重发。
完整迁移流程见 [SKILL-TO-DSH-PLUGIN.md](SKILL-TO-DSH-PLUGIN.md)（同目录模板）。
