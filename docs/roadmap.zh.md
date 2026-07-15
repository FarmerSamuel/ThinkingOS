# ThinkingOS 路線圖

ThinkingOS v1.0 已完成原始五階段路線圖。後續開發依相容性政策與[未來工作](future-work.md)進行。

## v1.0 里程碑狀態

| 階段 | 成果 | 狀態 |
| --- | --- | --- |
| 1. Framework | Core、Engine、規格、Schema、語言與圖譜 | 完成 |
| 2. Core Skills | 十三個合規且經過測試的思考技能 | 完成 |
| 3. Knowledge Engine | 與技能邏輯分離、具來源的重用知識 | 完成 |
| 4. Multi-AI Adapters | OpenAI、Claude、Gemini、Cursor、Copilot 與 MCP | 完成 |
| 5. ThinkingOS SDK | Registry、圖遍歷、技能驗證、狀態、測試與套件 | 完成 |

## 階段 1：Framework

完成通用角色、哲學、原則、對話狀態、驗證模型、推理 Engine、技能生命週期、Thinking Language、JSON Schema、Registry 與有向圖譜。

## 階段 2：Core Skills

完成 Right Problem、Break It Down、Constraints、Gap Analysis、Analogy、Heuristic、Deep Processing、Make Association、Learning Triangle、Mind Map、Boundary、Complexity 與 Emergence。每個套件都符合正式技能規格，並有版本化測試與評估標準。

## 階段 3：Knowledge Engine

完成批判思考、問題解決、決策與系統思考基礎，以及共用詞彙與來源政策。知識可在不修改技能邏輯的情況下替換。

## 階段 4：Multi-AI Adapters

完成平台中立 Adapter 契約、失敗關閉的回應解析、模型 API 映射與 MCP Host Bridge。憑證、網路、模型選擇及供應商生命週期都位於框架之外。

## 階段 5：ThinkingOS SDK

完成 Python 3.11+ SDK，支援 Registry 載入、決定性圖遍歷、技能探索與 Schema 驗證、可重用對話狀態及 Adapter。CI 驗證測試與發行套件。

## 發布政策

新工作依序經過 `planned`、`draft`、`review`、`testing`、`released` 與 `deprecated`。已發布公開契約遵循語意化版本，破壞性變更必須附遷移說明。
