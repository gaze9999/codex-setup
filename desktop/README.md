# Codex Desktop 可編輯設定

此目錄管理 Codex Desktop 的 Git 提示詞與個人化偏好, 可直接編輯 Markdown 與 TOML 來源

## 平常修改的位置

| 要修改的項目 | 來源 | 套用位置 |
|---|---|---|
| Commit message | [commit-message.md](prompts/commit-message.md) | 設定中的 Git / 提交指示 |
| PR 標題與說明 | [pull-request.md](prompts/pull-request.md) | 設定中的 Git / Pull Request 指示 |
| 監看並修正 PR | [watch-pull-request.md](prompts/watch-pull-request.md) | 設定中的 Git / 監看並修正 Pull Request |
| 本機記憶與分支前綴 | [preferences.toml](preferences.toml) | 對應設定 UI, 或合併至本機 config.toml 的既有 section |
| 每輪適用的語言與 coding 偏好 | [global AGENTS.md](../agents/AGENTS.md) | Personalization / Codex 指示; 依 global installer 同步 |

先修改來源檔, 再將提示詞完整貼到對應欄位; 這些欄位保存文字, 不是 Markdown 檔案路徑. 不需要為每個設定另建 Skill 或 agent role

PR watcher 與提交提示使用相同的 commit 格式; PR 標題仍使用 `type(scope): summary`. 不相容變更保留提示詞中明訂的 `type(scope)!:` 形式. 發布 repository 不會自動更改目前 app 內已保存的提示詞

## 產生可合併的 TOML 片段

使用 Python 3.11+ 在 repository 根目錄執行:

```text
python scripts/render_desktop_settings.py
python scripts/render_desktop_settings.py --output desktop-settings.local.toml
```

工具只讀這個目錄的白名單設定與三份提示詞, 驗證後產生 TOML; 不讀本機 config, 不修改 app, 不安裝依賴, 不輸出 secrets. `--output` 不覆寫已存在檔案. 編輯來源後重新產生, 不維護第二份獨立提示詞

合併片段前先備份本機 config.toml, 在既有 `[desktop]`, `[features]`, `[memories]` section 合併同名 keys, 不重複建立 table 或覆蓋整份設定. 保留 model, provider, MCP, permissions 與個人路徑; app 重新讀取方式依當前版本, 存檔不代表執行中的 session 已套用

三個 `desktop.git-*-instructions` keys 與分支前綴來自此次已核對的 Desktop 本機設定; 不保證 CLI / IDE 或未來 Desktop 版本採相同 keys. 設定 UI 是需要相容性確認時的套用入口

## 個人化偏好與證據

2026-10-02 依使用者設定截圖與本機白名單設定核對:

| 項目 | 保存的偏好 | 核對及搬機方式 |
|---|---|---|
| 啟用 Codex 記憶 | 開啟 | 截圖與 features.memories / generate_memories / use_memories 一致 |
| 允許工具對話建立記憶 | 開啟 | 截圖確認; 可攜片段明確設 disable_on_external_context = false, 本機原設定未明列此 key |
| 參考我的寫作風格 | 開啟 | 截圖確認, 到 Personalization / 寫作核對; 尚未確認可攜 config key, 不自行編造 |
| PR 準備就緒時自動合併 | 關閉 | 截圖確認, 到 Git / PR watcher 核對; 不把 watcher 提示詞當合併授權 |
| Custom rules | 保留目的, 依新機器逐條重建 | 截圖未展開細項, 尚未確認完整規則清單; 不複製私人路徑或整份 permission state |

記憶設定參考 [OpenAI 官方記憶設定](https://learn.chatgpt.com/docs/customization/memories#configure-local-memories). `disable_on_external_context = false` 只允許該類對話參與記憶建立, 不保證每則對話都會產生記憶

Custom rules 應核對動作, 資料夾, 外部服務與是否需確認, 只保留新環境所需範圍; 不因工具包搬機擴張權限. 私人規則清單保留個人筆記, 公開 repo 只保存方法

此處保存設定偏好, 不打包 memories/, auth.json, sessions, logs, app state 或個人寫作來源; 也不執行刪除記憶. 新機器是否登入同一帳號或已同步寫作偏好, 必須在該機器核對
