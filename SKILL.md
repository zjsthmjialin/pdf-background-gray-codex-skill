---
name: remove-pdf-background-gray
description: Remove gray or off-white scan backgrounds from image-based PDF pages while preserving original image pixel dimensions, page geometry, and anti-aliased text edges. Use for requests such as PDF 去底灰, 扫描件底色变白, 去除纸张灰底, 保持原分辨率, or avoid jagged/binarized text in scanned PDFs.
---

# Remove PDF Background Gray

Use the bundled script to whiten only the high-value background range. It edits embedded image objects directly, never rasterizes complete PDF pages, never resizes images, and stores cleaned images with lossless Flate compression.

## Workflow

1. Inspect the input with `pdfinfo`, `pdffonts`, and `pdfimages -list`.
2. Use this skill when pages are image-based scans. If meaningful vector text, transparency masks, or non-scan artwork is present, inspect carefully before processing.
3. Render one representative page and inspect its background histogram when possible. The defaults preserve values through 230 and smoothly whiten values from 230 to 252.
4. Run:

```powershell
python scripts/remove_pdf_background_gray.py INPUT.pdf OUTPUT.pdf
```

5. For darker paper, lower `--white-point` gradually. To protect more light detail, raise `--low`.

```powershell
python scripts/remove_pdf_background_gray.py INPUT.pdf OUTPUT.pdf --low 235 --white-point 250
```

6. Verify the output with `pdfinfo`, render representative early/middle/late pages, and visually inspect text edges at high zoom. Report that lossless encoding can increase file size.

## Guardrails

- Keep `0 <= low < white-point <= 255`.
- Do not use hard thresholding or bilevel conversion; it damages anti-aliasing.
- Do not resize, change page boxes, or render/reassemble whole pages.
- Preserve darker pixels exactly; use the continuous smoothstep curve only in the configured highlight range.
- Write user-facing deliverables outside the installed skill directory.

