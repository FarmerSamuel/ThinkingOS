# ThinkingOS 命名慣例

一致命名讓技能可攜、可搜尋且可由機器驗證。

## DSL 識別字

ThinkingOS Language 的符號後一律使用 **PascalCase**。

| 概念 | 格式 | 範例 |
| --- | --- | --- |
| Skill | `#PascalCase` | `#RightProblem`, `#GapAnalysis` |
| Element | `$PascalCase` | `$Goal`, `$InitialState` |
| Context | `@PascalCase` | `@Budget`, `@Organization` |
| State | `%PascalCase` | `%Validating`, `%LogicTesting` |
| Evaluation | `!PascalCase` | `!Valid`, `!Incomplete` |

名稱要簡短、具體且表達語意。元素與情境偏好名詞，對話狀態使用狀態詞，評估使用結果詞。避免供應商名稱、實作技術、不明縮寫與版本號。

## JSON

JSON 屬性使用 **camelCase**：

```json
{
  "thinkingElements": [],
  "conversationState": "%Validating",
  "nextSkill": "#GapAnalysis"
}
```

DSL 參照的 enum 保留符號與 PascalCase；Schema 檔名使用小寫 kebab-case 與 `.schema.json`。

## Markdown 文件

- 每份文件只使用一個一級標題。
- 標題使用句式大小寫。
- DSL 與 JSON 範例使用 fenced code block。
- 儲存庫內資源使用相對連結。
- 檔名使用小寫 kebab-case，例如 `thinking-language.md`。

## 技能與目錄

DSL 的技能名稱使用 PascalCase；檔案系統或套件識別使用語意相同的小寫 kebab-case，例如 `#GapAnalysis` 對應 `gap-analysis`。

名稱屬於公開契約。重新命名已發布概念需要遷移指南與適當版本變更；別名必須明確且暫時。
