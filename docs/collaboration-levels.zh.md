# 協作等級

協作等級必須與後果、可逆性、不確定性及契約影響成比例；更多 Actor 並不必然更好。

## 等級定義

| 等級 | 組成 | 適用情境 | 必要控制 |
| --- | --- | --- | --- |
| L1 — 單一 | 一個 Actor 執行一個 Skill | 日常、低成本且可逆的思考 | Schema 驗證、揭露假設、人類保有一般決策責任 |
| L2 — 對抗 | Analyst 加 Critic，可選 Evidence Reviewer | 成本明顯、難以逆轉、因果有爭議或不確定性有重大後果 | 共用 Request Identity、單一 Arbiter、分歧診斷、只有一個已提交後繼狀態 |
| L3 — 全席 | 獨立角色、仲裁紀錄、受控角色輪替 | Schema 或 Skill 變更、安全、法律、高成本或跨組織決策 | 合成 Conformance 證據、明確人類核准、完整 Record 與 State Chain、可信 Release Anchor |

## 升級條件

當以下任一條件具有實質影響時，應提高等級：

- 決策難以逆轉；
- 失敗具有安全、法律、財務或廣泛利害關係人後果；
- 證據薄弱或因果解釋仍有爭議；
- Actor 反覆產生互不相容的分類；
- 提議修改穩定的 ThinkingOS 契約。

不要只因為另一個模型可用就升級。爭議變數解決且剩餘工作屬於例行作業後，應降低等級。

## L1 協定

一個 Actor 接收固定的 Framework 與 Skill Identity、經驗證的輸入、序列化狀態與 Output Schema。Host 驗證結果，人類保留決策責任。L1 是預設等級。

## L2 協定

1. 從相同 Base State 與 Case Identity 建立候選執行。
2. 指派不同認知角色，但不把角色永久綁定到 Provider。
3. 保持候選輸出不可變，並禁止直接寫入狀態。
4. 評估結論前先診斷差異。
5. 產生一筆仲裁紀錄與一個已提交後繼狀態。

當同一平台持續擔任相同角色，或結論似乎依賴角色時，建議輪替角色。

## L3 協定

L3 增加獨立證據審查、受控角色輪替、完整審計紀錄、明確人類核准與 Release-grade Conformance。Delegated Agent 或 Policy 可以準備仲裁，但不能取代 L3 的人類核准。

穩定契約發布前，Conformance 至少涵蓋一個具有 Structured Output 能力的 Provider Adapter 與 MCP Adapter。Live Interoperability 使用合成或經明確授權的非敏感輸入。

## 決策規則

仲裁依據是證據、契約符合度、Never Rules、Rubric Findings、不確定性與已驗證目標，而不是多數決。Blocking Failure 不能被數個正向輸出平均掉。

## 回饋

分類後的分歧進入相應改進路徑。只有可重現的 Contract Ambiguity 會成為契約迴歸測試；其他發現用於改進 Adapter、Validation、Provider 組態或 Host Control。
