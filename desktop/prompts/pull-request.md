依目前分支相對 PR 實際 target/base branch 的完整 PR 差異, 產生 PR 標題與說明

以 PR 的 merge-base 後最終交付內容為準, 不預設 target/base branch 為 `master` 或 `main`使用繁體中文, 技術名稱, API, Symbol, 模組名稱與專有名詞保留原文

若 repository 存在 PR template, 優先沿用其欄位與結構, 並依以下規則填入實際內容; 刪除不適用的空白段落

PR 標題格式:

`<type>(<scope>): [<ticket>] <summary>`

規則:

* `type` 依整份 PR 的主要目的選擇
* `scope` 優先使用交易碼, 功能群組或主要模組名稱, 統一小寫; 沒有明確 scope 時可省略
* `ticket` 僅使用已提供或已確認的需求單號; 沒有時省略整個 `[<ticket>]`
* `summary` 描述整份 PR 最終交付的結果, 不以單一 commit 或中間操作作為標題

PR 說明依實際需要包含:

### 變更目的

說明:

* 原本存在的具體問題或需求
* 問題的觸發情境
* 本次 PR 完成後的預期行為

避免只寫「功能調整」, 「Bug fix」或其他無法讓 reviewer 理解目的的描述

### 主要變更

整理整份 PR 最終保留的重要變更, 使未參與前置討論的 reviewer 能理解:

* 修改了哪些主要功能, 模組或資料流
* 關鍵行為如何改變
* 必須知道的 Architecture, API, Component 或介面規格變更
* 影響 review 判斷的重要技術取捨

省略操作流水帳, 嘗試過但未採用的方案, 逐 commit 重述, 以及從 diff 即可直接看出的瑣碎細節

### 驗證結果

僅列出實際執行過的檢查與真實結果, 例如:

* Type Check
* Build
* Unit Test
* Integration Test
* E2E
* Lint
* 實際操作驗證
* API / 相容性檢查

明確區分:

* 通過
* 失敗
* 未執行
* 無法驗證

未執行或無法驗證時, 簡短說明原因

不得臆造任何驗證結果

### 影響與部署注意事項

僅在適用時說明:

* API / 資料格式變更
* Database migration
* Dependency 變更
* Environment / Config 變更
* Feature flag
* 不相容變更
* 部署順序
* 跨系統依賴
* 回復方式

沒有特殊部署或相容性影響時省略本段

### 關聯資訊

僅加入已確認的:

* Requirement / Ticket
* Issue
* PR
* 來源 commit
* cherry-pick 來源
* hotfix 回補安排

不可臆造需求單號, 核准狀態, issue, 來源 commit 或回補安排

補充規則:

* 以 PR 實際 target/base branch 為比較基準, 不預設為 `master` 或 `main`
* PR 說明反映整份 PR 的最終狀態, 不逐一重述 commit message
* 簡單 PR 保持精簡; 只有在變更複雜度需要時才增加說明
* 若 PR 同時包含無關變更, 指出其範圍與可能需要拆分之處, 不以文字包裝成單一目的
* 跨不同 runtime / framework 或 Host / custom-element 邊界時, 若適用, 明確交代受影響的:

  * selector
  * inputs / outputs 或 properties / events
  * routing
  * shared assets
  * API / 資料格式
  * bundle / 載入規格
  * 相容性限制
* 不臆造測試結果, 需求內容, review 核准狀態或部署資訊
* 不包含機敏資料, 個人環境資訊, 未遮蔽 Log 或無關修改
* 僅輸出 PR 標題與 PR 說明, 不加額外前言或解說
