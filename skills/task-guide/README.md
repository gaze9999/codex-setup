# Task Guide

依目標專案的實際規格與已確認決策, 建立按功能載入的任務指引, 工作項目 ID 規則與精簡中文歷史快照

以下訂單查詢, ID, SHA 與時間均為虛構格式示範, 不代表實際需求, commit 或驗證結果

## 安裝

將 ZIP 中完整的 `task-guide/` 資料夾放入目前 Codex 使用的 Skills 目錄; 保留同層檔案與子目錄, 不只複製 `SKILL.md` 或單一 script

```text
<Codex Skills 目錄>/
└── task-guide/
    ├── SKILL.md
    ├── README.md
    ├── agents/openai.yaml
    ├── assets/
    │   ├── task-guide.example.json
    │   ├── history.example.json
    │   └── history-commit.example.json
    ├── references/task-guide.md
    └── scripts/
        ├── create_task_guide.py
        └── record_history.py
```

已安裝不同版本時, 先備份及比對, 不覆蓋其他本機修改; repository 是來源, 本機目錄是安裝鏡像

Windows 與 macOS 使用相同 Skill; scripts 需 Python 3.10+, 僅使用標準函式庫, 不需要 MCP, API Key 或固定 repository 路徑; Windows 常用 `python`, macOS 依實際安裝可用 `python3`; 路徑有空白時加引號; 無 Python 時仍可由 agent 依 Skill 格式直接編輯, 並回報產生器未執行

## 快速使用

| 需求 | 處理方式 |
| --- | --- |
| 新功能指引 | 指定專案, 功能與來源; 由 agent 查證後產生 `.codex/agent-guidance/<feature>.md` 或指定位置 |
| 工作項目 ID | 沿用專案分類與編號; 先讀目前及歷史紀錄, 新 ID 從各分類最大序號續編 |
| 已修正項目 | 原列與原 ID 保留, 完全修正的 ID 畫線; 部分完成保留剩餘待辦 |
| 歷史快照 | 使用精簡中文, 時間到分鐘; 有 commit 同時記短 SHA 與實際變更內容, 無 commit 直接紀錄 |

可在目標專案使用以下完整要求, 將功能與來源替換成實際內容:

```text
使用 $task-guide, 依目前專案的 AGENTS.md, 實作, 已確認決策與我指定的規格, 為訂單查詢建立可重用任務指引

依目前任務與來源資訊找出相符的 Markdown 抽出版, 先讀相關段落, 不限定檔名或資料夾; 需要畫面證據, 抽出內容缺漏, 不明確, 過期, 衝突或明確核對原始來源時才回查截圖與原始規格; 保留原始規格與已確認決策的判定權, 無可用抽出版時讀相關原始範圍, 不自行重做抽出

先核對來源與授權範圍; 依標題重要性安排章節, 重要結論與阻擋事項在前, 主要表格接著呈現, 詳細條列與補充說明放後面; 使用精簡中文, 未確認內容保留為待決事項

沿用專案既有工作項目 ID, 原 ID 不因名稱或狀態改變而重編; 已修正 ID 畫線並保留原列, 不替補或重用; 新 ID 從各分類目前及歷史最大序號續編, 登記前核對最新紀錄

只有本次要求或既有文件流程需要時才追加歷史快照; 標題時間使用 yyyy-mm-dd hh:mm; 有已確認 commit 時同時記唯一短 SHA 與 diff 中的實際變更內容, 沒有 commit 就直接紀錄; 未提交變更分別說明; 保留既有歷史原文
```

## 指引格式範例

| 順序示例 | 標題 | 內容 |
| --- | --- | --- |
| 開頭 | 功能與範圍 | 本次授權, 必要前提 |
| 1 | 來源優先序 | 哪份來源控制欄位, API 或行為 |
| 2 | 未確認事項 | 會阻擋相依行為的決策 |
| 3 | 依任務讀取 | 任務 -> 應讀來源與證據 |
| 4 | 工作項目 ID | 紀錄位置, 前綴表與續編規則 |
| 後續 | 實作邊界, 驗證, 文件與紀錄 | 依本次重要性排列; 表格後放詳細條列 |

此順序只是範例; agent 按標題對目前任務的重要性選擇 `section_order`, 不把表格或條列格式當成重要性; 詳細 schema 見 [格式與工具說明](references/task-guide.md)

## 規格導覽範例

| 任務 | 先讀 | 有需要才回查 |
| --- | --- | --- |
| 欄位與互動 | 依來源資訊找到對應目前查詢規格的 Markdown 抽出版, 讀相關章節 | 由抽出版來源標示定位原始規格的缺漏或衝突段落; 畫面配置需要時看截圖 |
| API mapping | 依來源資訊找到對應目前 API 規格的 Markdown 抽出版, 讀相關 operation | 原始規格的不明確欄位或型別, 或明確要求的原始來源核對 |

抽出版不需與原始檔同名或放在固定資料夾; 新增或改名後依來源標示及目前任務解析. 原始規格及已確認決策仍保留判定權; 只讀抽出版時據實標示證據範圍, 不宣稱已核對原始檔; 無可用抽出版時直接讀必要原始範圍, 不自動產生新抽出檔

## ID 保留與續編範例

| 顯示 ID | 項目 | 狀態 |
| --- | --- | --- |
| UI-01 | 查詢區 | 部分完成, 保留剩餘待辦 |
| ~~UI-07~~ | 已修正的欄位驗證 | 原列及原 ID 保留 |
| UI-08 | 新增條件連動 | 新項目, 從原最大序號 07 續編 |
| API-03 | response mapping 核對 | API 分類從原最大序號 02 續編 |

`~~UI-07~~` 只改顯示; 邏輯 ID 仍是 `UI-07`, 關聯引用與歷史紀錄保留原值; 已修正 ID 與歷史空號不分配給其他項目; 分拆或合併時在既有紀錄保存關聯

可用 [指引與 ID 範例輸入](assets/task-guide.example.json) 預覽; 以下路徑以 Skill 根目錄為基準, macOS 可依實際環境將 `python` 換成 `python3`:

```text
python scripts/create_task_guide.py assets/task-guide.example.json --dry-run
python scripts/create_task_guide.py assets/task-guide.example.json --allocate-ids
```

ID 輸出是依已提供資料產生的建議, 不自動修改工作清單; 寫入前由同一登記 owner 核對目前及歷史紀錄

## 歷史快照範例

有 commit 時, 同時記短 SHA 與具體變更; 本例也包含未提交內容:

```markdown
## 2026-10-01 10:05 完成查詢欄位驗證

Git: example@abcdef1234 + 未提交變更

commit 已完成 UI-07 欄位格式檢核與錯誤提示; 未提交部分新增 UI-08 條件連動待辦; 現況表保留原列並將 UI-07 畫線

- 驗證: 欄位格式 focused Test 通過; 正式 API 未驗證
- 未完成: UI-08 條件連動, API-03 mapping 核對
```

無 commit 時省略 Git 行, 直接紀錄實際內容:

```markdown
## 2026-10-01 10:10 盤點查詢待辦

新增 UI-08 與 API-03 待辦, 保留原 ID 與 ~~UI-07~~ 原列; 尚未實作

- 驗證: 僅文件與編號核對, 未執行 application Test
```

可用 [無 commit 輸入](assets/history.example.json) 與 [有 commit 輸入](assets/history-commit.example.json) 預覽; 真正寫入前需以當次實際時間, commit diff 與驗證結果替換範例:

```text
python scripts/record_history.py assets/history.example.json --dry-run
python scripts/record_history.py assets/history-commit.example.json --dry-run
```

新增或追加快照時加 `--output <history.md>`; script 保留原文與換行格式, 相同時間及標題不重複追加; 時間由目前使用者/task 時區提供, 不以未知時區的執行主機猜測
