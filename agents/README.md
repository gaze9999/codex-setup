# Agent 治理與同步

此目錄的 [AGENTS.md](./AGENTS.md) 是跨專案 global 指示的可版控來源 在其他電腦 clone repository 後, 仍須將它安裝至該電腦的 `$CODEX_HOME/AGENTS.md` 或預設的 `~/.codex/AGENTS.md`; repository 內的副本不會自動套用為 global 指示

## 分層

- Global `AGENTS.md` 保存穩定的語言偏好, 授權邊界, 執行原則與驗證誠實性
- 專案 root 與 nested `AGENTS.md` 保存該 repository 的架構, 規格, 工作範圍與驗證方式
- Custom Skill 保存只在特定任務需要的詳細程序 [task-routing](../skills/task-routing/SKILL.md) 負責分流與交接判斷, 不自行授予建立 task 或委派的權限
- 目前 task 保存具體目標, 當次授權, 工作區狀態, 未解問題與停止條件

專案的 role 設定, 未提交變更與本機 exclude 策略屬專案層, 不複製到此 global 來源檔 使用者若更改 task 名稱, 跨 task 回報仍須以實際 `threadId` 定位

新專案的 root, nested, subagent 與 task 範本收在 [agent-governance project starter](../skills/agent-governance/assets/project-starter/README.md) 使用時先依專案實際內容改寫, 不把範本當成已啟用的指示 Skill ZIP 也包含這些範本, 可在另一台電腦獨立使用

## 跨電腦同步

先修改本 repository 的 `agents/AGENTS.md` 與相關 profile 檔, 審查 diff 與公開內容, 再以 `python scripts/install_global_agents.py --install` 單向安裝 不帶參數時比對 `AGENTS.md` 與 `subagents.config.toml`; 已安裝版本不同時預設整批拒絕寫入, 可先人工合併, 或明確加上 `--replace` 並保留自動備份

Skills 仍從 repository 的 `skills/` 目錄獨立安裝, 依根目錄 [README](../README.md) 執行驗證與鏡像比對 Release 僅提供各 Skill 的 ZIP asset; global 指示由 repository 來源檔與安裝 script 管理

## 個人 model defaults

[Global AGENTS.md](./AGENTS.md) 的 Delegation 與 model selection 保存短版 Sol / Luna 選擇原則與 Main 的責任, 不要求額外讀取分流文件 [subagents.config.toml](./subagents.config.toml) 提供 unpinned subagent `gpt-6.1-sol` 的 model 預設, Main 由開啟對話時選擇, 不要求每次派工指定 effort; 專案 role ownership 與限制由各專案治理檔保存

安裝 script 只複製這兩個公開檔案, 不覆寫既有 `config.toml`, secrets, permissions 或 MCP 設定 CLI 可用 `codex --profile subagents`; Desktop / IDE 若要作為一般預設, 將 profile 的 `agents.default_subagent_model` 合併到本機 `config.toml` 對應位置, 保留其他設定 專案與當次明確選擇仍可能優先; 不把 profile 安裝完成描述為現有 task 已切換 model

Project role 檔若需要依 slice 選擇 Sol 或 Luna, 應保持 model/effort 未固定; 職責穩定且範圍明確的角色可依[官方 subagent 文件](https://learn.chatgpt.com/docs/agent-configuration/subagents)與可驗證結果固定 model; Main 的直接實作能力與最終驗收責任保留, 獨立 reviewer 依風險使用

Codex 先依 explicit spawn, `[agents]` defaults 與 parent 解析設定, 再套用 custom role; role 的 model/effort pin 優先; explicit spawn 或 `[agents]` default 選定 model 且都未指定 effort 時, 使用該 model 的預設 effort; 兩者都未指定 model/effort 時才繼承 parent; role 只固定 model 時保留此前解析的 effort, 必須確認支援; 需要改用另一個 tier 時, 使用相同 ownership 與權限限制的 unpinned role; 不把顯示名稱, model 自述或 TOML 解析成功當成 runtime reload 證據

2026-09-30 核對 [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) 與 [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol): 標準 API 每 1M tokens 的 input / output 同為 USD 2 / 10, cached input 分別為 USD 0.10 / 0.20; 此 profile 改用 6.1 Sol, 不宣稱已量測 latency 或 Codex 帳號用量差異

## 指示結構依據

2026-09-29 回查 [OpenAI GPT-6 instruction guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) 與 [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md); 簡短且跨專案的選擇原則可放 global `AGENTS.md`, 較長的程序才使用有明確觸發條件的 guide 或 Skill reference, 並移除重複內容

[近期 GPT-6 使用者案例](https://www.reddit.com/r/codex/comments/1wqwkza/astra_ultra_with_solluna_subagents_has_been/) 採短版 global 指示搭配 config; [較大型 community pipeline](https://github.com/bohewu/agents_pipeline/blob/main/docs/codex-gpt6-routing-guidance.md) 則將操作建議與量測依據另放文件, 實際 routing 仍由 configuration 管理 這些是不同規模的使用案例, 不代表固定檔案布局的共識或已量測的成本改善

## 最小足夠驗證的依據

2026-09-29 回查 [r/ClaudeAI 的局部重測案例](https://www.reddit.com/r/ClaudeAI/comments/1ws8tv3/the_code_review_gap_i_see_in_the_aiagent_era/) 與 [r/ExperiencedDevs 的測試層級討論](https://www.reddit.com/r/ExperiencedDevs/comments/1uxzx4w/frustrations_with_e2eonly_approach_to_automated/); 採納先針對 diff 與需求驗證, 修復後重測受影響範圍, 並選擇能充分檢驗該行為的最小測試層級; 這些是案例與意見, 不代表所有變更都能只跑單一測試

[Microsoft Test Impact Analysis](https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops) 與 [Paul Hammant 的工程方法說明](https://martinfowler.com/articles/rise-test-impact-analysis.html) 以修改與測試相依選擇相關子集; 範圍無法可靠判定時需要較廣驗證; 此處採用選擇原則, 不假設該工具支援目前專案, 不導入新測試基礎設施, 並保留適用的 CI / release 門檻
