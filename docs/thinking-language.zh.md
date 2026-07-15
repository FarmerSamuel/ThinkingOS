# ThinkingOS 語言規格

## 目的

ThinkingOS Language（TOL）是一種小型、平台中立的領域專用語言，用來表達可重複使用的思考結構。它識別技能、思考元素、情境、狀態、評估與邏輯關係，不依賴 LLM、提示格式、API 或 Runtime。

語言只描述思考，不實作技能，也不規定應用程式如何呈現。

## 詞法形式

參照由符號緊接 PascalCase 識別字組成：

```text
Reference  := Sigil Identifier
Sigil      := "#" | "$" | "@" | "%" | "!"
Identifier := PascalCaseName
```

符號與名稱之間不能有空白；每行一個陳述。空白行可增加可讀性，`//` 開頭代表註解。

## 核心概念

### Skill：`#Skill`

代表目前套用或引用的 Thinking Skill。

```text
#RightProblem
#BreakItDown
#GapAnalysis
```

### Element：`$Element`

代表技能檢查或轉換的思考單元。

```text
$Goal
$Obstacle
$Constraint
$InitialState
$TargetState
```

### Constraint 或 Context：`@Context`

代表管理分析的環境條件、邊界或情境因素。

```text
@Budget
@Time
@Organization
```

`$Constraint` 是被分析的思考元素；`@Constraint` 是作用中的治理情境。

### State：`%State`

代表目前對話或推理生命週期狀態，且不可編碼供應商特有的 Session 行為。

```text
%CollectingInputs
%Validating
%LogicTesting
```

### Evaluation：`!Evaluation`

代表結構化評估結果或狀態。它不能取代 Output Schema 所要求的證據與推理。

```text
!Valid
!Invalid
!Incomplete
```

### Logic

`->` 表示「導向」、「產生」或「支持轉換到」，但本身不證明因果；適用技能仍須定義並測試關係。

```text
$ObstacleRemoved -> $GoalAchievable
```

`↓` 表示「分解為」、「精煉為」或「移至下一分析表達」。

```text
$InitialProblem ↓ $MinimumTractableUnit
```

運算子由左至右。版本 1 不包含括號、優先序、否定或布林運算；複雜邏輯應拆成多個明確陳述。

## 文件結構

語言文件應宣告一個主要技能，接著列出元素、情境、選填狀態、邏輯與評估：

```text
#Skill
$Element
@Context
%State
$Element -> $Element
!Evaluation
```

## 範例

```text
#RightProblem
$Goal
$Obstacle
@Constraint
%Validating
!Valid
```

```text
#BreakItDown
$InitialProblem
$InitialProblem ↓ $MinimumTractableUnit
$MinimumTractableUnit
```

```text
#GapAnalysis
$InitialState
$TargetState
@Time
$InitialState -> $TargetState
!Incomplete
```

## 序列化與合規

文字表示是標準的人類可讀格式；交換與驗證使用符合 `schemas/thinking-language.schema.json` 的 JSON AST。序列化必須保留概念型別、識別字、陳述順序、運算子與操作數。

合規文件至少宣告一個技能，只使用已定義符號與運算子，符號後使用 PascalCase，將平台設定留在語言外，並只在符合目前技能推理與輸出要求時使用評估 Token。
