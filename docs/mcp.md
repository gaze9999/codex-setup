# 本機 MCP 安裝與獨立部署

`codex-setup` 是 MCP 原始碼與安裝工具的維護來源, 不是固定的部署位置; Local Documents 以兩個 wheel 部署, 使用者不需要 clone `codex-setup` 或 `my-py-tools`

| 元件 | 原始碼 | 部署方式 |
| --- | --- | --- |
| `my-py-document-core` | `my-py-tools` | 安裝 versioned wheel, 公開 API 為 `my_py_document_core`, 目前 API 1 |
| `codex-local-documents-mcp` | 本 repo `mcp_servers/local_documents/` | 安裝 server wheel, 使用模組或 console command 啟動 |
| `my-py-workspace-core` | `my-py-tools` | 安裝 versioned wheel, 公開 API 為 `my_py_workspace_core`, 目前 API 1 |
| `codex-workspace-inspection-mcp` | 本 repo `mcp_servers/workspace_inspection/` | 唯讀查詢驗證證據與環境差異 |
| Jev | 本 repo `skills/jev-evaluation/` | `codex-jev-mcp` wheel 與相容 Skill installer, 可獨立部署 |

核心 wheel 從同一份 CLI 原始碼建置 namespaced package, 不複製另一份核心到本 repo; MCP runtime 使用已安裝的套件, 不修改 `sys.path` 來匯入另一個 working tree, 不保留 CLI repo 路徑

## Baseline 快速安裝

[統一安裝與監看說明](mcp-bootstrap.md) 提供預設位置, 本機 wheel bundle, read roots, preview/apply 與環境沿用; 使用 `bootstrap-mcp.cmd --apply` 或 `sh bootstrap-mcp.sh --apply`, 不必逐一填 core/server wheel 路徑; 未設定 roots 的新工具先列 pending

## 任意位置部署 Local Documents

準備 `my_py_document_core-0.2.0-py3-none-any.whl` 與 `codex_local_documents_mcp-0.2.0-py3-none-any.whl`, 在使用者選擇的位置建立 Python 3.11+ 環境; 首次安裝公開相依套件需網路或對應平台的本機 wheel cache

Windows 範例, 請換成該電腦的真實路徑:

```powershell
python -m venv C:\path\document-runtime
C:\path\document-runtime\Scripts\python.exe -m pip install C:\path\wheels\my_py_document_core-0.2.0-py3-none-any.whl C:\path\wheels\codex_local_documents_mcp-0.2.0-py3-none-any.whl
C:\path\document-runtime\Scripts\python.exe -m pip check
```

macOS/Linux 使用 `/absolute/document-runtime/bin/python` 與對應路徑; 不直接搬移既有 virtual environment, 在新環境重新安裝

其他 MCP client 的 stdio 設定可使用:

```json
{
  "command": "/absolute/document-runtime/bin/python",
  "args": ["-I", "-B", "-m", "mcp_servers.local_documents.document_server", "--read-root", "/absolute/documents"]
}
```

Windows 的 command 換成 `C:\path\document-runtime\Scripts\python.exe`; `-I` 排除目前工作目錄與 `PYTHONPATH` 對套件來源的影響; 各 client 的設定格式自行依實際支援核對, 上述只有 command 與 args

也可使用環境中的 `local-documents-mcp --read-root /absolute/documents`; server 會等待 MCP JSON-RPC stdin, 由支援 stdio 的 client 管理程序

## 註冊到 Codex, 不需要 repo

在已安裝兩個套件的 Python 環境執行; 需已有使用者 Codex `config.toml`, 預設由 `CODEX_HOME` 或 `~/.codex` 定位, `--config` 可指定實際位置

```text
python -I -B -m mcp_servers.local_documents.install_document_mcp --read-root /absolute/documents
python -I -B -m mcp_servers.local_documents.install_document_mcp --read-root /absolute/documents --apply
python -I -B -m mcp_servers.local_documents.verify_document_mcp
```

第一行只預覽, `--apply` 才備份並更新 `local_documents` 設定; 其他設定保留, 重複相同設定回傳 unchanged; 預設 Python 是目前 interpreter, 必要時可用 `--python` 明確指定

每個讀取範圍分別提供 `--read-root`, 都必須是存在的絕對路徑; 預設不允許寫入, 需要時另加 `--write-root /absolute/output`; 不因 preview 或模型呼叫自動放寬範圍

三個 console command 分別是 `local-documents-mcp`, `local-documents-register`, `local-documents-verify`; 使用環境的絕對執行檔或 Python 模組方式, 不依賴 shell 選到哪個 Python

## 從 codex-setup 統一管理

已有 runtime 時, 可從本 repo 的入口註冊與驗證, 不必指定另一個 repo:

```text
python scripts/install_mcp.py local_documents --python /absolute/document-runtime/bin/python --read-root /absolute/documents
python scripts/install_mcp.py local_documents --python /absolute/document-runtime/bin/python --read-root /absolute/documents --apply --verify
```

首次建立 runtime 時提供兩個 wheel:

```text
python scripts/install_mcp.py local_documents --runtime /absolute/document-runtime --core-wheel /absolute/wheels/my_py_document_core-0.2.0-py3-none-any.whl --server-wheel /absolute/wheels/codex_local_documents_mcp-0.2.0-py3-none-any.whl --read-root /absolute/documents --apply --verify
```

- 預設或 `--dry-run` 只顯示 plan 與 wheel metadata/SHA-256, 不建立環境, 安裝套件或寫檔
- `--core-wheel` 與 `--server-wheel` 可更新各自套件; 先核對 wheel 名稱與內容, 不使用 editable install
- 新 runtime 必須提供兩個 wheel; 已存在的非 virtual environment 目錄會被拒絕, runtime 不放進本 repo
- `--apply` 先安裝明確提供的 wheel, 檢查套件相容性, 再呼叫 runtime 內的 guarded installer
- `--verify` 驗證 stdio discovery, 六種原生格式, 抽出版定位, OCR 與 Markdown 防護, 只使用臨時 fixture

原 `--documents-repo`, server 的 `--tools-root` 與 `python -m mcp_tools.*` 入口已退休; 舊版需重新安裝套件並註冊, 新設定使用已安裝模組, 不包含 repo 的 server.py 路徑

## 建置與版本

核心建置方式見 `my-py-tools/docs/python-document-core.md`; 本 repo 的 server wheel 可在具備 setuptools/wheel 的 Python 環境建置:

```text
python -m pip wheel --no-deps --no-build-isolation --wheel-dir /absolute/wheels .
```

目前 Local Documents server 固定使用 `my-py-document-core==0.2.0`, Workspace Inspection server 固定使用 `my-py-workspace-core==0.1.0`, 並要求各自的 `API_VERSION=1`; 核心公開參數, 回傳資料或錯誤語意有變更時, 先檢查相容性再更新依賴; 每個 MCP 可使用自己的相容版本與獨立環境

## Workspace Inspection

此 server 只有 `workspace_status`, `validation_evidence`, `compare_environment` 三個唯讀工具; 不執行同步, 安裝, build, test 或 Git 寫入

```text
python scripts/install_mcp.py workspace_inspection --runtime /absolute/workspace-runtime --core-wheel /absolute/wheels/my_py_workspace_core-0.1.0-py3-none-any.whl --server-wheel /absolute/wheels/codex_workspace_inspection_mcp-0.1.0-py3-none-any.whl --read-root /absolute/workspaces --apply --verify
```

已存在 runtime 時可改用 `--python`; 每個 `--read-root` 都必須是存在的絕對資料夾, 工具只能讀取其下路徑; 環境比對預設排除 `.env`, credentials, private key, VCS 與 cache, 詳細開發介面見 [Workspace Inspection MCP](../mcp_servers/workspace_inspection/README.md)

修改或搬移原 repo 不會直接改變已安裝 runtime; 更新以 wheel 與 hash 為單位, 不用跨 repo source path 或 submodule working tree 當作啟動相依

## Jev

保留既有 Skill installer 的備份, credentials 與驗證流程; 統一入口預設只預覽, `--apply` 才安裝, 其他參數直接傳給既有 installer

```text
python scripts/install_mcp.py jev
python scripts/install_mcp.py jev --apply
python scripts/install_mcp.py jev --apply --replace --verify-online
python scripts/install_mcp.py jev --help
```

安裝位置可使用 `--skill-root`, `--runtime` 與 `--config` 指定; 獨立 Skill ZIP 的 installer 不需要完整 repo, 詳見 [Jev 安裝文件](../skills/jev-evaluation/README.md)

`--verify-online` 以內建公開範例呼叫 Jev API; 未指定時沿用離線 MCP 驗證, 不把私人專案內容當作驗證資料

## 操作與驗證

- [Local Documents 操作教學](local-documents-usage.md)
- [Jev 操作教學](jev-usage.md)
- [Local Documents 開發驗證](../mcp_servers/local_documents/README.md)

註冊後重新載入支援 MCP 的 client, 再核對工具清單; installer 或獨立 stdio 驗證通過, 不代表目前對話已 reload

這是 stdio 部署; 遠端 HTTP endpoint 需另行選擇 transport, authentication 與 host; Windows/macOS/Linux 的 native 相依需依平台安裝, 實機支援範圍以驗證結果為準
