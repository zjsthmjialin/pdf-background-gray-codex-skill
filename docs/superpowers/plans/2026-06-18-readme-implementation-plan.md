# Comprehensive README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a comprehensive Chinese `README.md` for users and developers, including verified results and author contact information.

**Architecture:** Keep the project root as an installable Codex Skill while adding one GitHub-facing README. Organize the README in progressive layers: overview and quick start first, technical design and validation next, then limitations and project maintenance details.

**Tech Stack:** Markdown, Codex Skills, Python 3, Pillow, NumPy, pypdf, Git

---

### Task 1: Create the README

**Files:**
- Create: `README.md`
- Reference: `SKILL.md`
- Reference: `scripts/remove_pdf_background_gray.py`
- Reference: `docs/superpowers/specs/2026-06-18-readme-design.md`

- [x] **Step 1: Write the complete document**

Create a Chinese README with these sections in order: project overview, core features, suitable and unsuitable inputs, verified result, installation, Codex invocation, command-line usage, parameters, technical principle, creation process, validation, limitations, troubleshooting, repository structure, dependencies, contribution, and author contact.

Use these verified facts exactly:

```text
Pages: 194
Unique image objects processed: 713
Verified unchanged: page count, page geometry, embedded image pixel dimensions
Contact: zjsthm@gmail.com
```

- [x] **Step 2: Check document integrity**

Run:

```powershell
rg -n "TODO|TBD|PLACEHOLDER|待定|占位" README.md
git diff --check
```

Expected: `rg` finds no placeholders and `git diff --check` reports no whitespace errors.

- [x] **Step 3: Check required coverage**

Run:

```powershell
rg -n "194|713|原分辨率|抗锯齿|Flate|smoothstep|zjsthm@gmail.com" README.md
```

Expected: every required term appears in a relevant section.

- [x] **Step 4: Present for user review**

Do not commit or push `README.md` yet. Provide the local file path and summarize its coverage so the user can review it first.

- [x] **Step 5: Commit and push after approval**

Run only after the user approves the README:

```powershell
git add -- README.md docs/superpowers/plans/2026-06-18-readme-implementation-plan.md
git commit -m "Add comprehensive project documentation"
git push origin main
```

Expected: `main` and `origin/main` point to the new documentation commit.
