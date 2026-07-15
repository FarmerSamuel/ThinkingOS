# Claude 使用指南

本指南說明如何在 Claude 中運用 ThinkingOS 提升思考品質，以及如何把真實的
Claude 對話轉化為技能改進。框架本身維持供應商中立；所有 Claude 專屬內容都
位於生成的發行套件與 `adapters/claude/` 之中。

## 選擇整合路徑

| 路徑 | 適合情境 | 使用內容 |
| --- | --- | --- |
| Claude Code | 日常思考工作與迭代本儲存庫 | `.claude/skills/` 中生成的 Agent Skills |
| claude.ai | 不需本機檢出的對話式使用 | 以 `core/` 建立的 Project 指令，以及在支援 Agent Skills 的方案上傳技能套件 |
| Claude API | 嵌入 ThinkingOS 的應用程式 | `adapters/claude/` 中的 `ClaudeAdapter` |
| MCP 主機 | 需要人工把關的工具式整合 | `adapters/mcp/` 中的 MCP adapter |

## Claude Code

Claude Code 會自動載入專案層級的 Agent Skills。將儲存庫 clone 下來並在其中
啟動 Claude Code：

```bash
git clone https://github.com/FarmerSamuel/ThinkingOS.git
cd ThinkingOS
claude
```

`.claude/skills/` 會載入十四個技能：每個思考技能各一個套件
（`right-problem`、`break-it-down`、`constraints` 以及 Registry 中的其餘技
能），加上一個 `thinkingos` 路由技能，內含通用角色、核心原則、引擎流程與技
能圖譜。

使用方式：

- 直接描述問題或決策。技能描述以觸發條件為導向，Claude 會選出對應的思考紀
  律——例如一個已經預設解法的請求會觸發 `right-problem`。
- 明確指名技能：「用 right-problem 分析這個」或「先跑 constraints，再跑
  gap-analysis」。
- 請求路由：「哪個 ThinkingOS 技能適合這個情境？」`thinkingos` 技能會依
  Registry 圖譜回答。

每個生成的技能都會執行其契約：先收集必要輸入再分析、驗證關卡先於邏輯規則、
一次只問一個釐清問題，並以通用輸出格式回傳評分、假設、缺少的資訊與下一步
建議。

`.claude/skills/` 中的套件由正典契約生成。切勿直接編輯；請修改技能套件後重
新生成：

```bash
python tools/export_claude_skills.py
```

## claude.ai

若不想檢出儲存庫、以對話為主：

1. 建立一個 Project，並以 Core 契約組成其指令：`core/persona.md`、
   `core/principles.md`、`core/workflow.md` 與 `core/questioning-style.md`。
   這讓每段對話都具備「驗證優先」的行為，而不綁定單一技能。
2. 將 `knowledge/` 的參考資料（例如 `knowledge/problem-framing.md`）加入
   Project，讓批判引用可重複使用的思考知識，而不是即興發揮。
3. 在支援 Agent Skills 的方案上，上傳 `.claude/skills/` 中生成的套件——每個
   目錄都是自足的技能，內含 `SKILL.md` 契約。
4. 在對話中要求 Claude 執行該紀律：「先套用 Right Problem 再提出任何方案」，
   或貼上 ThinkingOS Language 區塊，例如：

```text
#RightProblem
$Goal
$Obstacle
@Constraint
%Validating
```

## Claude API

應用程式透過 provider adapter 呼叫 Messages API；adapter 會把驗證過的技能情
境對應為 `system` 指令與單一使用者訊息。傳輸、憑證、模型選擇、重試與最終輸
出驗證由你的應用程式負責：

```python
from adapters.base import AdapterRequest
from adapters.claude import ClaudeAdapter

adapter = ClaudeAdapter()
request = AdapterRequest(
    skill="right-problem",
    instructions=open("core/persona.md", encoding="utf-8").read(),
    inputs={
        "problemStatement": "We need a new CRM because sales are declining.",
        "goal": "Restore qualified-pipeline conversion from 14% to 20%.",
    },
)
provider_request = adapter.build_request(request, model="claude-sonnet-5", max_tokens=2048)
```

載入技能與遍歷 Registry 請見 SDK 指南；payload 細節請見
`adapters/claude/`。

## MCP 主機

`adapters/mcp/` 中的 MCP adapter 為 Model Context Protocol 主機對應技能請
求。依照 adapter 文件與專案安全政策的要求，重大決策務必保留人工把關。

## 迭代循環

ThinkingOS 把技能失準視為契約缺陷，而不是提示詞微調。以 Claude 對話作為測
試場，把失敗回饋到正典套件：

```text
在真實對話中使用技能
  -> 發現失準（漏掉歧義、過早給解法、問錯問題）
  -> 把案例記錄到 skills/<id>/examples.md 與 tests.md
  -> 在 skill.json 中編入修正（驗證關卡、邏輯規則、never 規則）
  -> 更新版本與變更紀錄
  -> 重新生成 Claude 發行套件
  -> 驗證並提交
```

具體步驟：

1. **記錄。** 把失準的對話寫成 `skills/<id>/examples.md` 的案例，並在
   `skills/<id>/tests.md` 新增一列一致性測試。
2. **編碼。** 把修正表達為 `skills/<id>/skill.json` 中可被機器檢查的規
   則——新的驗證關卡、邏輯規則或 never 規則——而不是鬆散的敘述。
3. **版本。** 同步更新 `skill.json`、`metadata.yaml` 與
   `skills/registry.yaml` 的 `version`，並在技能的 `CHANGELOG.md` 與根目錄
   `CHANGELOG.md` 記錄變更。
4. **重新生成。** 執行 `python tools/export_claude_skills.py`，讓 Claude 發
   行套件反映新契約。
5. **驗證。** 提交前執行儲存庫檢查：

```bash
python tools/validate_repository.py
python -m unittest discover -s tests
python tools/export_claude_skills.py --check
mkdocs build --strict
```

持續整合會執行相同的檢查（包含匯出同步測試），因此 Claude 發行套件永遠不會
悄悄偏離正典契約。

在 Claude Code 中工作時，儲存庫的 `CLAUDE.md` 會把這個循環教給工作階段本
身：請 Claude 套用修正，它就會遵循同樣的記錄、編碼、版本、重新生成與驗證
流程。

## 相關頁面

- [開發者指南](developer-guide.md)：儲存庫驗證。
- [技能作者指南](skill-author-guide.md)：撰寫新技能。
- [SDK 指南](sdk-guide.md)：程式化存取。
- [問對問題指南](right-problem-guide.md)：Golden Skill。
