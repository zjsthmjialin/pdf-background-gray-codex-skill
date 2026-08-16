// dsh-pdf-background-gray
// 把「Remove PDF Background Gray」技能（remove-pdf-background-gray）注册为 DSH 技能：
// 去除扫描 PDF 的灰色/米白底色，保持分辨率、页面几何与抗锯齿文字边缘。
// 技能本体（SKILL.md + scripts/remove_pdf_background_gray.py + README）随包分发在 skills/ 下。
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

export const name = 'remove-pdf-background-gray'
export const inject = ['skills']

const SKILL_DIR = fileURLToPath(new URL('skills/remove-pdf-background-gray/', import.meta.url))
const SKILL_MD = readFileSync(new URL('skills/remove-pdf-background-gray/SKILL.md', import.meta.url), 'utf8')

// 去掉 YAML frontmatter，保留 Markdown 正文作为技能内容。
function stripFrontmatter(md) {
  if (!md.startsWith('---')) return md
  const end = md.indexOf('\n---', 3)
  return end === -1 ? md : md.slice(end + 4).trimStart()
}

const DSH_NOTE = `
## DSH 运行提示

- 技能资源目录即 <skill_resources> 对应的目录；核心脚本：\`<资源目录>/scripts/remove_pdf_background_gray.py\`。
- 运行时要求：Python 3.10+，依赖 \`python -m pip install pypdf Pillow numpy\`。
- 用法：\`python "<资源目录>/scripts/remove_pdf_background_gray.py" 输入.pdf 输出.pdf [--low 235 --white-point 250]\`。
- 处理前可用 \`pdfinfo\` / \`pdfimages -list\` 确认页面是图像型扫描件；处理后用 \`pdfinfo\` + 高倍渲染检查文字边缘。
- 输出文件写到会话工作区，不要写进技能资源目录。
`

export function apply(ctx, config = {}) {
  ctx.skills.register({
    name: 'remove-pdf-background-gray',
    description: 'Remove gray or off-white scan backgrounds from image-based PDF pages while preserving original image pixel dimensions, page geometry, and anti-aliased text edges. Use for requests such as PDF 去底灰、扫描件底色变白、去除纸张灰底、保持原分辨率, or avoid jagged/binarized text in scanned PDFs.',
    whenToUse: '用户要求去除扫描 PDF 的灰色/米白底色（去底灰、底色变白），且需保持分辨率、页面几何与抗锯齿文字边缘的场景。',
    content: stripFrontmatter(SKILL_MD) + DSH_NOTE,
    resourceBase: { kind: 'directory', path: SKILL_DIR },
  })
}
