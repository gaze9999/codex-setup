# Jev MCP 與 Skill 安裝包

共用一份 Jev API client, 提供 MCP 工具與 CLI; Skill 保存按需使用, 必讀 context 與資料外傳邊界, 可在不同專案共用

需要 Python 3.10+ 與首次安裝時的網路連線; Windows / macOS / Linux 使用相同原始碼, 安裝時建立各平台的獨立 Python runtime, 下載固定版本的官方 MCP SDK

## Wheel 與離線安裝驗證

也可使用 `codex-jev-mcp` wheel, CLI / MCP 與此 Skill 共用同一份 client; 安裝到獨立 Python 環境後, 從任意資料夾以 `python -I -B -m codex_jev_mcp.mcp_server` 啟動, 使用 `jev-verify` 作離線 protocol 檢查; 不自動呼叫付費 API

可由 codex-setup 的 baseline bundle 一次設定預設路徑與既有 runtime 沿用; 使用 `bootstrap-mcp.cmd --apply` 或 `sh bootstrap-mcp.sh --apply`; bundle 必須具備 preset 指定的 wheel; 不宣稱未發佈 wheel 可由 latest release 下載

本機使用紀錄預設關閉, 明確需要時由獨立 `local-activity-monitor` 啟用; 詳細邊界見 [選用監看](references/usage.md#opt-in-local-monitoring)

## 相容 Skill ZIP 安裝

解壓 ZIP 後, 在含 `jev-evaluation/` 的目錄開啟終端; 已設定 Jev Key 的電腦可略過第一行

Windows:

```powershell
python -B jev-evaluation/scripts/jev.py setup-key
python -B jev-evaluation/scripts/install_mcp.py --verify-online
```

macOS / Linux:

```sh
python3 -B jev-evaluation/scripts/jev.py setup-key
python3 -B jev-evaluation/scripts/install_mcp.py --verify-online
```

`setup-key` 隱藏輸入, 預設寫入個人 Codex credentials 目錄; 使用既有 `TYPESAFE_API_KEY` 也可, Key 不會放入 Skill 或 ZIP; 此檔案為本機純文字憑證, macOS / Linux 使用 0600 權限

安裝完成後重新載入 Codex, 核對 `jev` server 下的 `jev_rank`, `jev_evaluate` 與 `jev_status`; 安裝程式會保留其他設定, 備份變動檔案, 並用公開範例驗證真實 MCP 呼叫

新版取代已安裝版本時加上 `--replace`; 只想預覽目的位置時加上 `--dry-run`, 此模式不安裝套件, 不寫檔也不連線

```sh
python3 -B jev-evaluation/scripts/install_mcp.py --replace --verify-online
```

目前 client 已有 `.codex/skills/jev-evaluation` 時沿用該位置; 新安裝預設使用官方文件的 `~/.agents/skills`, `CODEX_HOME` 或 `--skill-root` 可指定已確認的位置, 不重複安裝兩份

## 使用與管理

- MCP 安裝在使用者層級, 各專案可共用; 專案 `AGENTS.md` 只保留該專案的必要邊界
- 工具只接收明確提供的候選摘要或有限問題, 不掃描整個 repository 或讀取對話歷史
- 必讀項目留在 Main; `required` 候選保留 ID 且不傳至 Jev, 排序不刪除任何候選
- Server 使用既有環境變數或本機憑證, 工具參數不包含 Key; API 失敗時回傳 fallback, Main 繼續原有流程
- 原始碼可攜, runtime 與生成的 config 路徑由各台電腦建立; 搬移安裝目錄後重新執行 installer, 保留原本的 Key

詳細輸入、失敗診斷與同步方式見 [usage.md](references/usage.md); 跨平台與 Apple Silicon 的實機結果依當次驗證回報, 不由 Python 語法檢查推論

## iPhone / iPad 的 ChatGPT App

目前官方自訂 MCP apps 說明為 web only, 行動 App 尚不支援; 本套件的支援範圍是 Windows / macOS / Linux 本機 MCP host

手機無法直接連到桌機 stdio 程序; 未來改用支援遠端 MCP 的 client 時, 需另行部署 HTTPS endpoint 與驗證機制, 並確認該 client 的權限及功能支援

參考: [官方 MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), [Codex MCP 設定](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [OpenAI 行動 App 限制](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-apps-in-chatgpt-beta)
