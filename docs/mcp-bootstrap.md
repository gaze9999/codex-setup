# Baseline MCP 與本機監看安裝

統一入口以 `mcp_servers/presets/baseline.json` 為準, 管理 server 清單, wheel 版本, tool 清單與選用項目; `codex-setup` 是維護來源, 安裝後 runtime 不依賴 checkout 路徑

## 使用者操作

需要 Python 3.11+ 與相符的本機 bundle; 首次安裝平台相依需網路或事先準備的 wheel cache; 不複製另一台電腦的 virtual environment

Windows 執行 `bootstrap-mcp.cmd`; macOS / Linux 執行 `sh bootstrap-mcp.sh`; 預設只預覽, `--apply` 才安裝與註冊

```powershell
.\bootstrap-mcp.cmd
.\bootstrap-mcp.cmd --apply
.\bootstrap-mcp.cmd --read-root C:\path\approved-documents --apply
```

```sh
sh bootstrap-mcp.sh
sh bootstrap-mcp.sh --read-root /absolute/approved-documents --apply
```

也可使用 `python scripts/install_mcp.py bootstrap` 或 `python scripts/bootstrap_mcp.py`; 原 `install_mcp.py local_documents`, `workspace_inspection` 與 `jev` 參數仍保留

| 項目 | 預設處理 |
| --- | --- |
| Jev | 安裝 `codex-jev-mcp` wheel, 保留憑證優先順序; Key 缺少只列 pending setup; 不自動呼叫付費 API |
| Local Documents | 使用既有 core + server wheel; 新安裝只提供 read roots, 未指定則 pending roots; 既有 read/write roots 保留 |
| Workspace Inspection | 同樣需明確 read roots; 未提供時保留未設定, 不開放 cwd, home 或整台電腦 |
| OpenAI Docs | 官方唯讀 HTTP endpoint; 相同 endpoint 或 enabled plugin 已提供時沿用, 不建立第二份 |
| Context7 | 只有 `--context7` 才新增 hosted HTTP server; OAuth 可另用 `codex mcp login context7`, 安裝流程不要求或保存 Key |
| 既有 node_repl | 保留原設定; 不轉成 Python wheel, 不換 runtime |

已有同名但無法辨識來源的 server 會標示 conflict 並保留; 既有停用的同名 HTTP provider 保持停用; 不改動 plugin 或 AGENTS; GitHub, browser, Figma, Notion 等能力依實際用途另行設定

## 路徑與非機敏設定

- 使用者 config: `$CODEX_HOME/config.toml`, 或 `~/.codex/config.toml`; `--config` 可指定
- 新 Windows runtime: `%LOCALAPPDATA%/codex-setup/mcp/<server>/`; `LOCALAPPDATA` 無效時使用使用者的 `AppData/Local`
- 新 macOS runtime: `~/Library/Application Support/codex-setup/mcp/<server>/`
- 新 Linux runtime: 絕對 `$XDG_DATA_HOME/codex-setup/mcp/<server>/`, 否則 `~/.local/share/codex-setup/mcp/<server>/`
- `--runtime-root` 可覆蓋新環境的父目錄; 健康的既有環境優先沿用, 不自動搬移舊 cache runtime
- 已指定的新 server read roots 與選用 `--cert /absolute/cert.pem` 存入 `$CODEX_HOME/mcp-bootstrap.json`, 供重跑沿用; 不保存 Key, Token 或密碼
- Windows Store 程序可能看到套件虛擬路徑; 安裝前檢查 preview 的實際 interpreter 可讀性, 不將這台機器的 sandbox 路徑當成跨機預設

這些 durable data 路徑是此 repo 的部署選擇, 不是 OpenAI 強制規定; 不把新程式或 wheel 放進 Cache

Preview 顯示目的位置, package 版本與 SHA-256, existing/new/pending 狀態; 不建立 runtime, 不寫 config 或設定, 不安裝相依

Apply 核對 wheel CRC / metadata / hash, 建立個別 venv 或沿用現有環境, 安裝固定版本套件, 執行 `pip check` 與離線 stdio fixture 驗證, 然後備份與寫入變動設定; 新 Jev 登錄使用 `-I -B -m codex_jev_mcp.mcp_server`

重複執行相同 bundle 時不重裝 wheel, 不改寫相同設定; 仍執行套件與離線 protocol 檢查; unknown Skill 檔案保留並拒絕覆蓋; managed Skill 變動先備份到 Skill 目錄外並核對內容; config 使用寫入前比對與 readback

套件步驟失敗會保留該 server 註冊, 不阻擋其他獨立項目; runtime 可能已部分安裝, 回報失敗後需檢查該環境; 不把失敗當作已成功; 含未設定 roots 的成功結果仍清楚列 pending 項目

其他維護者正在處理 Skill 鏡像時, 可加入 `--no-skill-sync`; 仍安裝與驗證 runtime, 只略過 managed Skill 同步

Apply 顯示是否需要重新載入 Codex; 檔案與 wheel 已安裝不代表已開啟對話的 MCP process 自動更換; baseline 本身不執行 Jev 語意比較, 不啟用永久紀錄

## Bundle 維護

維護者先取得 preset 指定的五個 wheel, 再整理成同一個本機 bundle; 一般使用者不用逐一填 core/server wheel 或 runtime 路徑

```text
python scripts/prepare_mcp_bundle.py --wheel-dir /absolute/all-built-wheels
```

預設產物 `dist/mcp/bootstrap/` 包含 wheel, `bundle.json` 與可攜 `installer/`; 使用者在 `installer/` 執行 wrapper 即可, 不必 clone repo; checkout 入口預設也查同一 bundle 位置; `--bundle` 可覆蓋

產物標示 `local_unpublished_bundle`, 不由既有 release 腳本自動發佈; 目前 release assets 提供 Skill ZIP 與 Local Documents / Workspace Inspection server wheel, 不包含 Jev wheel 或 baseline bundle; 缺少 bundle / matching wheel 時顯示具體 pending 說明

Jev wheel 建置:

```text
python -m pip wheel --no-deps --wheel-dir /absolute/wheels skills/jev-evaluation
```

CLI 與 MCP 使用同一份 `scripts/jev.py`, wheel 以 `codex_jev_mcp` namespace 封裝; public entry points 是 `jev`, `jev-mcp`, `jev-verify`; 單獨 CLI script 與既有 Skill installer 繼續可用

## 獨立監看 repo

`local-activity-monitor` 維護本機網頁與 Jev / Codex collectors, 不維護 API client 或 Skill; Jev metadata writer 保留在 `codex-setup`, 文件核心保留在 `my-py-tools`

監看工具安裝後, 使用 `local-activity-monitor --enable-jev --configure-only` 明確啟用本機紀錄; 以 `--codex --open` 啟動頁面; 預設 `http://127.0.0.1:8787/`, 關閉終端或 Ctrl+C 停止; `--disable-jev --configure-only` 停用紀錄並保留歷史

只保存 timestamps, operation/source, model, known tokens, latency, body bytes 與安全狀態; 不保存 prompt, query, rubric, candidates, answers, Key 或 raw error; 寫入失敗不影響 Jev; 舊 process 需 reload; 畫面是本機觀察統計, 不代表帳戶總用量或剩餘額度

Codex 只讀近期本機 JSONL metadata, 增量追蹤, 使用 thread 最新累計快照; 不將重複快照加總, 不解析 exec 內容或讀取對話文字 / auth.json; Mac M5 / Linux 的原生執行尚未驗證

## 官方依據

- [Codex MCP 設定](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp): stdio / HTTP 與官方唯讀 docs endpoint
- [Context7 client 設定](https://github.com/upstash/context7/blob/master/docs/resources/all-clients.mdx): hosted endpoint 與 client-specific 設定, 只在選用時使用
- [PyPA virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), [XDG data directory](https://specifications.freedesktop.org/basedir/latest/): 隔離環境與 Linux durable data 的依據
