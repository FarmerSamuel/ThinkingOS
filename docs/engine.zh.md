# 推理引擎

ThinkingOS Engine 的規範版本位於 [`core/engine.md`](https://github.com/FarmerSamuel/ThinkingOS/blob/main/core/engine.md)。本頁讓引擎出現在網站導覽中，同時避免複製版本化契約。

## 管線摘要

```text
收集輸入
↓ 驗證輸入
↓ 偵測缺少資訊
↓ 評估思考元素
↓ 執行邏輯規則
↓ 評估推理
↓ 產生評估
↓ 產生輸出
↓ 建議下一個技能
```

完整階段責任與退出條件請閱讀[正式 Engine 規格](https://github.com/FarmerSamuel/ThinkingOS/blob/main/core/engine.md)。
