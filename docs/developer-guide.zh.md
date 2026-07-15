# 開發者指南

## 必要工具

- Git
- Python 3.11 或更新版本
- 建議使用 Virtual Environment

儲存庫驗證器可在沒有額外套件時執行基本檢查；完整 Schema 與 YAML 驗證使用 `requirements-dev.txt`，文件建置使用 `requirements-docs.txt`。

## 設定儲存庫

```bash
git clone https://github.com/FarmerSamuel/ThinkingOS.git
cd ThinkingOS
python -m venv .venv
```

啟用環境後安裝相依套件：

```bash
python -m pip install -r requirements-dev.txt -r requirements-docs.txt
```

## 驗證與測試

```bash
python tools/validate_repository.py
python -m unittest discover -s tests -v
```

驗證器檢查 Registry 參照與循環、必要技能檔案、JSON 與 YAML、Schema、Metadata 一致性、測試數量、文件連結及生命週期狀態。

## 建置雙語文件

```bash
mkdocs build --strict
```

本機預覽：

```bash
mkdocs serve
```

英文位於 `/`，繁體中文位於 `/zh/`。新增或修改英文頁面時，必須同步更新同名的 `.zh.md`；Strict 模式將導覽或文件警告視為失敗。

## 產生技能套件

```bash
python tools/generate_skill_packages.py constraints
```

產生內容只是起始契約，不代表自動核准。提交前必須審查領域用語、範例、邏輯、轉換與參考資料。

## 開發規則

- 分離 Core、Engine、Specification、Skill、Knowledge 與 Adapter 責任。
- 除 `adapters/` 外保持 AI 與平台中立。
- 公開契約使用語意化版本，提交使用 Conventional Commits。
- 行為變更要同步更新測試、Registry、文件與 Changelog。
- Pull Request 前執行完整驗證、測試及文件建置。

## 疑難排解

- 相依循環是 Registry 設計錯誤，不能在驗證器中忽略。
- 缺少前置條件應產生澄清或轉換建議，不得虛構輸入。
- 平台欄位應在 Adapter 邊界映射，不得默默擴充技能語意。
