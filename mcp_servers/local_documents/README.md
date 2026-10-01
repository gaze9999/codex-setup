# Local Documents MCP

本目錄維護 MCP server, service, OCR 相依, guarded installer 與 stdio verifier; 公開文件與 Markdown 功能使用已安裝的 `my-py-document-core` API 1, 不讀取另一個 repo 的原始碼位置

本 repo 是原始碼來源, server 不需要部署在此資料夾; `codex-local-documents-mcp` wheel 安裝到使用者的 Python 環境後, 可透過模組或 console command 啟動

- [安裝與獨立部署](../../docs/mcp.md)
- [日常操作教學](../../docs/local-documents-usage.md)

## 開發驗證

先將核心與 server 的 wheel 安裝到測試 runtime, 再在 repo 根目錄執行 source tests; 核心未安裝時 service tests 會顯示 skipped, 不把缺少測試相依當成通過

```text
python -B -m unittest discover -s tests -p test_document_mcp.py -v
python -B -m unittest discover -s tests -p test_install_mcp.py -v
python -I -B -m mcp_servers.local_documents.verify_document_mcp
```

第三行使用已安裝 server 與核心, 以臨時 fixture 驗證 stdio, 原生格式, OCR 與寫入防護; 不依賴目前工作目錄或 `MY_PY_TOOLS_ROOT`

原 `my-py-tools/mcp_tools/` 已退休; 更新 runtime 使用新 wheel, 搬移或重建 runtime 後重新註冊, 不搬移既有 virtual environment
