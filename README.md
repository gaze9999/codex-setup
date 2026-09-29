# Codex Setup

可跨電腦與 repository 使用的 global `AGENTS.md` 與 ChatGPT / Codex Skills

此 repository 是 [global `AGENTS.md`](./agents/AGENTS.md) 與自訂 Skill 的可版控來源 本機 Codex 設定目錄只作為安裝鏡像, 避免不同電腦雙向手動修改後產生漂移 [Agent 治理說明](./agents/README.md) 記錄分層與同步邊界

建立新專案治理架構時, 可用 [agent-governance project starter](./skills/agent-governance/assets/project-starter/README.md) 依實際專案類型產生精簡的 root 與 nested `AGENTS.md`, Codex subagent 角色及條件式 task 指引 範本隨該 Skill ZIP 提供, 不依賴固定的本機 repository 路徑

## Skill catalog

| 類別 | Skill | 用途 |
|---|---|---|
| Agent 與 context | [Agent Governance](./skills/agent-governance/SKILL.md) | 重整 global, root, nested `AGENTS.md`, tool-specific routing 與 subagent 職責 |
| Agent 與 context | [Task Routing](./skills/task-routing/SKILL.md) | 判斷直接執行, 新 task, fork 與 subagent, 並整理必要交接資訊 |
| Agent 與 context | [Coding Prompt](./skills/coding-prompt/SKILL.md) | 僅在明確要求 prompt 或 handoff 時產生可執行的 coding prompt 與當下 model 建議 |
| Agent 與 context | [Context Brief](./skills/context-brief/SKILL.md) | 將已指定規格, API, schema 或整合文件整理成可重用 implementation contract |
| AI 與媒體 | [AI Application Engineering](./skills/ai-application-engineering/SKILL.md) | 實作或診斷 LLM, Agent, Tool Calling, RAG, Embedding 與 model runtime |
| AI 與媒體 | [ComfyUI Workflow](./skills/comfyui-workflow/SKILL.md) | 維護可重現的 Stable Diffusion / ComfyUI graph, model 與硬體設定 |
| AI 與媒體 | [Editorial Illustration](./skills/editorial-illustration/SKILL.md) | 依固定 editorial illustration 視覺方向處理使用者提供的圖片 |
| Frontend 與遊戲 | [Component Member Order](./skills/component-member-order/SKILL.md) | 安全整理 Angular Component class member 與可選 Signal I/O 遷移 |
| Frontend 與遊戲 | [Unity Development](./skills/unity-development/SKILL.md) | 依實際 Unity version, package, serialized asset 與 build target 開發及驗證 |
| Frontend 與遊戲 | [Vue Development](./skills/vue-development/SKILL.md) | 依實際 Vue, Nuxt 或 Vite stack 開發並保留 component, state, SSR 與 build contracts |
| 文件 | [Doc Updater](./skills/doc-updater/SKILL.md) | 實作後依 verified diff 同步必要的 docs, memo, changelog 或 API reference |
| 文件 | [Document Production](./skills/document-production/SKILL.md) | 產生可交付的 PDF, DOCX 或 Markdown 正式文件 |
| 文件 | [README Maintainer](./skills/readme-maintainer/SKILL.md) | 依 repository 證據建立或大幅重整 README |
| Rules 與 Filter | [Filter Rule Maintenance](./skills/filter-rule-maintenance/SKILL.md) | 維護 AdGuard, uBlock Origin, DNS, hosts 與相似 filter/rewrite rules |

## 分層原則

- Global `AGENTS.md` 只保留跨專案且長期穩定的使用者偏好, 安全邊界與執行原則
- Repository `AGENTS.md` 保留該專案的 Architecture, Runtime, Contract, Ownership 與驗證邊界
- Custom Skill 保存會跨專案重複使用但只在特定任務需要的流程與領域知識
- 單次任務 prompt 保存目前 goal, scope, acceptance criteria, authorization, progress 與 stop condition
- `SKILL.md` 保持短而可判斷何時使用, 詳細但非每次需要的內容放入 `references/` 並由任務條件載入
- 不將單一專案路徑, 交易規格, 私有 endpoint, model workaround 或暫時環境狀態寫成通用 Skill

## 安裝與同步

每個 Skill 可獨立安裝 Repo 內容是 source of truth, 同步方向固定為 repository `skills/<skill-name>` → 本機 Codex skills 目錄

### Global AGENTS.md

跨電腦使用時, 先 clone 此 repository, 再從 repository `agents/AGENTS.md` 單向安裝至 `$CODEX_HOME/AGENTS.md`; 未設定 `CODEX_HOME` 時使用個人目錄的 `.codex/AGENTS.md` Repo 內的檔案不會因 clone 而自動成為 global 指示

```powershell
python scripts/install_global_agents.py
python scripts/install_global_agents.py --install
```

第一行只比對內容, 第二行只在目標不存在或內容已相同時安裝 若另一台電腦已有不同的 global 設定, 先檢視與合併; 確認要以 repo 版本取代時, 使用 `--install --replace`, script 會先將舊檔備份在該電腦的 Codex 設定目錄下 執行後再次用不帶參數的指令比對

### Skills

本機安裝或更新時:

1. 確認 repository working tree 與預期變更
2. 驗證目標 Skill 的 `SKILL.md` 與 `agents/openai.yaml`
3. 僅複製需要新增或更新的 Skill 目錄, 不覆寫 `.system`, plugin 或其他非此 repository 管理的 Skill
4. 比對 repo 與本機鏡像的相對路徑及檔案 hash
5. 重新載入支援 Skill discovery 的用戶端

不要直接在本機安裝鏡像做永久修改 若需要變更, 先改 repository, 驗證後再單向同步

## Repository 驗證

以單一精簡指令檢查所有 Skill metadata, Markdown links 與 Python syntax, 避免逐檔讀取與重複輸出:

```powershell
python scripts/audit_skills.py
```

同步本機鏡像後可一併比對檔案清單與 hash:

```powershell
python scripts/audit_skills.py --installed-root "$env:USERPROFILE\.codex\skills"
```

### ChatGPT App

行動端可從 [GitHub Releases](https://github.com/gaze9999/codex-setup/releases) 下載單一 Skill ZIP, 再到 `Plugins → Skills → Create → Upload from your computer` 上傳

ZIP 頂層需保留單一同名 Skill 目錄:

```text
skill-name.zip
└── skill-name/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
```

### Desktop / Web

用戶端支援 GitHub repository 安裝時指定:

```text
Repository: gaze9999/codex-setup
Skill path: skills/<skill-name>
```

各 Skill 可獨立安裝, 不需要一次載入整個 `skills/` 目錄

## Release 封裝

- 每個 release 為每個 Skill 提供獨立 ZIP asset, 不只依賴 GitHub 自動產生的 source archive
- ZIP asset basename 與 Skill 目錄相同, 頂層只包含該 Skill 目錄
- 封裝前排除 `__pycache__`, `*.pyc`, local logs, temporary output, secret 與 machine-specific files
- 發布前驗證 Skill metadata, ZIP 結構, repository diff 與實際 asset 清單

## 檔案角色

- `agents/AGENTS.md`: 跨專案常駐指示的可攜 source of truth
- `agents/README.md`: Agent 指示的分層, 授權與同步方式
- `agents/subagents.config.toml`: 可攜式 subagent model fallback profile, 不含 credentials 或 permissions
- `SKILL.md`: Skill 的啟用條件, 工作流程, 邊界與輸出
- `agents/openai.yaml`: Skill 的 interface metadata 與預設啟用 prompt
- `references/`: 只在相關子任務才載入的詳細知識
- `assets/`: Icon, template 或不需常駐 context 的素材
- `scripts/`: 可重複的掃描, 驗證或轉換流程
