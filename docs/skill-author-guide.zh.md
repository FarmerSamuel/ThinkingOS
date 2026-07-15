# 技能作者指南

## 先確認是否需要新技能

新技能必須代表一種可重複使用且未被現有技能擁有的思考習慣。若需求只是領域知識、平台整合或現有規則的重複，應放在 Knowledge、Adapter 或共用 Core。

## 必要套件結構

```text
skills/<skill-id>/
├── README.md
├── metadata.yaml
├── skill.json
├── workflow.md
├── validation.md
├── evaluation.md
├── rubric.md
├── examples.md
├── tests.md
├── references.md
└── CHANGELOG.md
```

以 `skills/right-problem/` Golden Skill 為參考；已策展的 Registry 項目可透過 `tools/generate_skill_packages.py` 建立骨架。

## 撰寫契約

1. 定義目的、範圍與思考元素。
2. 宣告有型別的必要與選填輸入。
3. 先寫驗證關卡，再寫邏輯規則。
4. 讓邏輯有順序、可觀察、可重現。
5. 定義評估面向與校準 Rubric。
6. 在不破壞通用輸出 Schema 的前提下映射總分與各面向發現。
7. 加入中立對話規則與明確 Never Rules。
8. 宣告相依安全的下一技能轉換。

## 測試技能

至少加入十個案例，涵蓋有效輸入、缺少資訊、歧義、矛盾、無證據假設、缺少相依、替代解釋、邊界、低證據、輸出合規、狀態保存與轉換限制。測試驗證契約結果，不驗證模型逐字措辭。

## 發布技能

- 從 `0.1.0` 與 `draft` 開始。
- 經過審查與測試後才發布。
- 保持 Registry、Metadata、`skill.json`、測試與 Changelog 版本一致。
- 遵循[技能生命週期](skill-lifecycle.md)與語意化版本。

## 驗證

```bash
python tools/validate_repository.py
mkdocs build --strict
```

結構驗證通過但邏輯仍空泛、無證據、責任重疊或依賴平台的技能，不得發布。
