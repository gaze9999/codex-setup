依本次實際 staged diff 產生 Git commit message使用繁體中文, 技術名稱, API, Symbol, 模組名稱與專有名詞保留原文

格式:

`[scope] <type>: [<ticket>] <summary>`

規則:

* `type` 依實際變更選擇:
  `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore` 或 `revert`
* `scope` 優先使用交易碼, 功能群組或主要模組名稱, 統一小寫; 沒有明確且有意義的 scope 時省略
* `ticket` 僅使用使用者提供, repository 明確記載或已確認的需求單號; 沒有時省略整個 `[<ticket>]`, 不可臆造或推測
* `summary` 簡短描述本次提交實際完成的具體行為與目的
* 避免使用「更新」, 「修改」, 「調整」, 「修正問題」等無法單獨理解變更內容的模糊摘要
* summary 不加句尾句號
* 一個 commit 應對應一個可獨立說明, 審查與回復的目的
* staged diff 若包含彼此無關的變更, 不強行產生單一 commit message; 指出應拆分的變更範圍
* 簡單變更只輸出標題
* 複雜變更可加入 body, 僅補充 reviewer 從標題與 diff 無法直接得知的重要資訊, 例如:

  * 修改原因
  * 重要技術取捨
  * 相容性或影響範圍
  * 實際執行的驗證及結果
* 不臆造 Build, Test, Lint, Type Check 或其他驗證結果
* 發生不相容變更時使用:
  `<type>(<scope>)!: <summary>`
  並於 footer 加入:
  `BREAKING CHANGE: <影響與遷移方式>`
* issue, 需求單或 cherry-pick 來源僅在已確認時加入
* 不包含機敏資料, 個人環境資訊, 未遮蔽 Log 或與本次提交無關的內容
* 僅輸出最終 commit message, 不加前言, 解說或 Markdown 程式碼圍欄

範例:

`[date] fix: 保留缺值日期的原始空白狀態`

`[orders] feat: 顯示訂單處理狀態`
