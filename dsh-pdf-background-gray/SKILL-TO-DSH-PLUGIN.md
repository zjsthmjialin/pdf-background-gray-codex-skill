# SKILL → DSH 插件迁移模板（可复用清单）

把现成的 SKILL.md 技能包转成 DeepSeek Harness (DSH) 插件（`dsh plugin add` 可安装）的标准流程。
2026-08-16 由「灵感演示工坊」全流程实测沉淀（npm v0.1.1 / GitHub / awesome PR #819）。

## 前置条件

- Node ≥ 18、pnpm、dsh CLI（`node <dsh路径>/lib/bin.js`）；
- 技能本体是**纯 SKILL.md**（无宿主逻辑、无客户端 UI）；需要 UI/宿主逻辑的请走真插件路线（cordis patch + client 注入），另做评估。

## 1. 建壳（目录结构）

```
dsh-<name>/                 # 包名建议 dsh-<name>
├── package.json            # 见下方骨架
├── cordis.patch.yml        # 挂载行
├── index.js                # ctx.skills.register 注册技能
├── README.md               # 安装 + 用法 + 发布说明
└── skills/<name>/          # 技能本体快照（SKILL.md + 全部资源）
```

### package.json 骨架

```json
{
  "name": "dsh-<name>",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml", "skills/"],
  "engines": { "node": ">=18" },
  "repository": { "type": "git", "url": "git+https://github.com/<you>/<repo>.git" },
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
}
```

### index.js 骨架

```js
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

export const name = '<name>'
export const inject = ['skills']

const SKILL_DIR = fileURLToPath(new URL('skills/<name>/', import.meta.url))

export function apply(ctx, config = {}) {
  ctx.skills.register({
    name: '<name>',
    description: '<SKILL.md frontmatter 的 description>',
    content: '<SKILL.md 正文，可附加 DSH 运行提示>',
    resourceBase: { kind: 'directory', path: SKILL_DIR },
  })
}
```

### cordis.patch.yml

```yaml
- insert:
    - id: <name>
      name: 'dsh-<name>'
```

## 2. 本地接入（先验证，再发布）

```powershell
# 用户全局技能目录（所有会话生效）
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.dsh\skills"
Copy-Item <技能文件夹> "$env:USERPROFILE\.dsh\skills\<name>" -Recurse
# 新开会话 → 技能目录出现该技能即成功
```

## 3. 打包检查

```powershell
cd dsh-<name>
npm pack --dry-run     # 检查 files 清单：必须含 index.js/cordis.patch.yml/skills/，不得混入多余 tgz
```

## 4. 发布（npm）

```powershell
npm view dsh-<name>                    # E404 = 包名可用
npm publish                            # 2FA：会走浏览器授权；或 npm publish --otp <码>
```

- npm 2025-11 起只接受**细粒度令牌**；自动化发布用带 "Bypass 2FA for publishing" 的 Granular Access Token：
  `npm config set //registry.npmjs.org/:_authToken=<token>`
- 验证：`npm view dsh-<name>` → 本机 `dsh plugin --profile web add dsh-<name>`（reconcile 自动挂 bundle）

## 5. 仓库 + Release + 可见性

```powershell
git clone <repo>                        # Windows git 报 schannel 错：git -c http.sslBackend=openssl clone …
git add dsh-<name>/ README.md
git -c user.name=<you> -c user.email=<email> commit -m "feat: add DSH plugin packaging"
git -c http.sslBackend=openssl push origin master
gh -R <you>/<repo> release create v0.1.0 --title "v0.1.0" --notes-file notes.md
```

- awesome-dsh-plugin PR：Fork `awesome-dsh-plugin/awesome-dsh-plugin` → README.md 与 README.zh.md 的对应分类（如 `### Skills` / `### 🧩 技能包`）加一行：
  `- [<you>/<repo>](https://github.com/<you>/<repo>) - <英文描述，≤ 1 行>`

## 6. 维护纪律（重要）

**技能本体每次改动 → 同步三处：**
1. 插件壳 `skills/<name>/` 快照（重新复制）；
2. `npm version patch && npm publish`；
3. 仓库同步提交。

## 常见坑速查

| 坑 | 解法 |
|---|---|
| pnpm 报 `ERR_PNPM_IGNORED_BUILDS` | `profiles\web\pnpm-workspace.yaml` 的 allowBuilds 加 `包名: true` 后重跑 add |
| npm publish 卡住 / OTP 提示不渲染 | `npm publish --otp <码>`；先杀挂死的 node 进程 |
| 2FA 403（无有效验证器） | 用恢复码重绑，或 Granular Token 勾 Bypass 2FA |
| `dsh plugin add` 提示 "declares no dsh.bundle" | pnpm 发布冷静期压旧版：显式 `add <pkg>@latest` |
