監看目前 PR 的檢查, 審查與合併狀態, 依以下原則處理: 

* 以 PR 實際 target/base branch 為準, 確認其為本次指定的 release / project 分支, 不預設為 `master`, `main` 或其他固定分支
* 僅處理由本次 PR 變更造成的檢查失敗, 以及具體, 有效且屬於本次範圍的審查意見
* 採取能完整解決問題的最小必要修改, 保留與本次問題無關的既有修改, 避免順帶 Refactor, 重新命名或格式化
* 修正前先確認失敗原因與變更內容的因果關係; 無法確認為本次 PR 所造成時, 不自行修改無關程式碼
* 修正後重新執行受影響範圍的必要檢查, 依實際結果明確區分: 

  * 通過
  * 失敗
  * 未執行
  * 無法驗證
* 不宣稱未實際執行的 Build, Test, Lint, Type Check 或其他檢查已通過
* 需要新增 commit 時, 依實際 staged diff 產生提交訊息, 格式為: 
  `[scope] <type>: [<ticket>] <summary>`
  沒有已確認的 ticket 時省略 `[<ticket>]`
* 遇到以下情況時停止修改並說明原因: 

  * 需求或 reviewer 意圖不明
  * 需要改變既有 API, 資料結構或其他公開介面或資料格式
  * 修改明顯超出本次 PR 範圍
  * 需要 rebase, reset, force push 或其他共享 Git history 重寫
  * 無法安全判斷應採取的行為
* 僅在使用者已授權合併, 且同時符合以下條件時, 依 repository 既定流程合併: 

  * 必要 CI / 檢查已通過
  * 必要 review 已核准
  * 沒有未解決的 blocking comment
  * 沒有 merge conflict
  * 符合 branch protection 與 repository 規則
* 不繞過必要檢查或 branch protection, 不自行批准自己的 PR, 不擅自變更 target/base branch, 不進行未授權的 force push
* PR 狀態沒有實質變化時保持安靜; 僅在需要使用者處理, 出現阻礙, 發現新的有效 review / check failure, 或合併完成時通知
