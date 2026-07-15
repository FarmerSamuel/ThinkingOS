# 技能相依關係

## 目的

相依代表某技能需要另一技能通常產生的推理能力或已驗證語意輸出。它保護分析品質，不是套件安裝相依，也不強制特定介面或 AI。權威清單是 `skills/registry.yaml`。

## 前置關係

| 技能 | 前置技能 | 為什麼要先執行 |
| --- | --- | --- |
| `right-problem` | 無 | 建立下游推理使用的有效問題與目標。 |
| `break-it-down` | `right-problem` | 確認應處理的問題後，分解才有意義。 |
| `constraints` | `right-problem` | 需要有效的問題邊界與結果。 |
| `gap-analysis` | `right-problem`, `constraints` | 有意義的差距需要有效目標、目前與目標狀態及可行空間。 |
| `analogy` | `right-problem` | 結構比較應從明確問題開始，避免只看表面相似。 |
| `heuristic` | `right-problem`, `constraints` | 了解情境與失敗邊界後，捷思法才安全。 |
| `deep-processing` | `right-problem`, `break-it-down` | 深入理解需要有效範圍與可識別元件。 |
| `make-association` | `analogy`, `deep-processing` | 有用品質的連結需要結構比較與充分闡述的概念。 |
| `learning-triangle` | `deep-processing` | 學習計畫應回應已證明的理解缺口。 |
| `mind-map` | `break-it-down`, `make-association` | 概念圖需要元件結構與有意義的交叉連結。 |
| `boundary` | `right-problem`, `constraints` | 系統範圍取決於問題、利害關係人與限制。 |
| `complexity` | `break-it-down`, `boundary` | 沒有元件、相依與邊界就無法可靠評估複雜度。 |
| `emergence` | `complexity`, `make-association` | 湧現行為需要互動結構與跨元素關係。 |

## 相依滿足方式

前置條件可由該技能在目前狀態中產生相容且已驗證的結果，或由其他可信來源提供等價輸入並通過消費技能驗證。只有名稱相同不夠；必須檢查語意、來源、版本、完整性與信心。

## 執行行為

- Engine 在執行技能邏輯前偵測未滿足的前置條件。
- 缺少阻擋性輸出時，要求澄清或建議前置技能。
- 多個已滿足前置技能可以匯入同一技能。
- 依賴圖必須無循環；迭代透過 Conversation State 與重複執行表示。

新增必要前置技能可能是破壞性變更，必須遵循生命週期、語意化版本、一致性測試與 Registry 審查。
