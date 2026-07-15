# 貢獻指南

本指南補充儲存庫根目錄的 `CONTRIBUTING.md`，說明框架特有的審查流程。

## 選擇正確層級

| 變更 | 位置 |
| --- | --- |
| 通用行為或原則 | `core/` |
| 執行順序 | `core/engine.md` |
| 公開契約與 Schema | `schemas/` 與規格文件 |
| 一種思考習慣 | `skills/<id>/` |
| 可重用證據或術語 | `knowledge/` |
| 供應商或介面轉換 | `adapters/` |
| 公開 Python API | `thinkingos/` |

不要在多個技能中複製共同行為，也不要讓供應商假設向上滲漏。

## 貢獻流程

1. 搜尋現有 Issue、Registry 與技能，確認沒有重疊。
2. 實作前先討論重大架構或公開契約變更。
3. 建立聚焦分支並使用小型語意提交。
4. 更新驗證、範例、測試、參考資料與 Changelog。
5. 同步更新英文與 `.zh.md` 繁體中文文件。
6. 執行測試、`python tools/validate_repository.py` 與 `mkdocs build --strict`。
7. 使用專案範本開啟 Pull Request 並說明相容性影響。

## 審查標準

審查範圍、層級責任、證據、AI 中立、Schema 合規、相依正確性、測試、雙語文件、版本與遷移影響。

## 破壞性變更

公開識別、必要輸入、邏輯語意、評估含義、輸出欄位或相依變更可能需要主版本升級。必須提供遷移指南，且不可就地改寫已發布成品。

## 社群標準

所有參與均受 [Code of Conduct](https://github.com/FarmerSamuel/ThinkingOS/blob/main/CODE_OF_CONDUCT.md) 管理；疑似安全問題請私下回報，不要公開建立 Issue。
