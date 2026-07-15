# ThinkingOS SDK 指南

Python SDK 提供決定性的框架契約存取；它不執行語言模型，也不取代 Thinking Skill 的推理規則。

## 開發安裝

```console
python -m pip install -e .
```

需要 Python 3.11 以上。Runtime 相依只包含 Registry 使用的 PyYAML 與技能契約驗證使用的 `jsonschema`。

## 探索與遍歷技能

```python
from thinkingos import SkillRegistry

registry = SkillRegistry.from_file("skills/registry.yaml")

for skill_id in registry.topological_order():
    skill = registry.get(skill_id)
    print(skill.id, skill.dependencies)

available = registry.available(completed={"right-problem"})
```

Registry 會拒絕重複 ID、未知相依、自我相依與循環；`available` 只回傳直接前置條件已滿足的技能。

## 載入技能套件

```python
from thinkingos import SkillLoader

loader = SkillLoader("skills", "schemas/skill.schema.json")
skill = loader.load("gap-analysis")
print(skill.version, skill.next_skills)
```

`SkillLoader` 依 Draft 2020-12 JSON Schema 驗證 `skill.json`，確認套件目錄與識別字一致，並防止路徑穿越。

## 保存對話狀態

```python
from thinkingos import ConversationState

state = ConversationState(
    current_skill="right-problem",
    current_goal="Reduce avoidable delivery delays",
)
state.merge_inputs({"timeframe": "Q3"})

serialized = state.to_json()
restored = ConversationState.from_json(serialized)
```

應用程式只應保存與目標相關的資料，並自行落實隱私與保留政策。

## 連接 AI 或 Host

先載入並驗證技能，再使用 Adapter。Adapter 只產生 Payload；應用程式負責傳輸、驗證、重試及輸出檢查。詳見 [`adapters/README.md`](https://github.com/FarmerSamuel/ThinkingOS/blob/main/adapters/README.md)。

## 相容性

`thinkingos` 匯出的公開名稱遵循語意化版本。技能契約、Registry、Schema 與 Adapter 各自版本化。SDK 主版本可能移除或改變公開 Python API；技能主版本則可能改變輸入或輸出語意。
