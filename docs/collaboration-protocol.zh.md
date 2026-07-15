# 多 AI 協作協定

> **生命週期：** Draft · **穩定性：** Experimental · **協定版本：** `0.1.0-draft.1`

ThinkingOS 定義平台中立、版本化的多 AI 協作契約，並可提供無狀態參考實作；專案不經營中央執行平台，也不保存使用者憑證或私人對話狀態。

本文件是 Draft 協作契約的規範性文件。Draft 欄位可能在正式發布前改變，不受 v1 穩定相容性保證保護。

## 責任邊界

ThinkingOS 負責：

- 角色、執行信封、仲裁、譜系與 Conformance 語意；
- 可由 Schema 驗證的交換格式；
- 依證據進行分歧分類；
- 合成 Fixtures 與確定性契約測試。

呼叫端應用程式負責：

- 選擇 Provider 與模型；
- 網路、憑證、重試、流量限制、隱私與保存政策；
- 排程候選執行；
- 保存或傳輸信封與紀錄；
- 取得必要的人類核准。

Provider 特定傳輸留在 `adapters/`，思考邏輯留在 `core/` 與 `skills/`。

## 角色與平台分離

角色描述認知責任，不代表偏好的 Provider。標準角色包括 `analyst`、`critic`、`evidence-reviewer` 與 `arbiter`；應用程式可以宣告其他角色，但不得把角色永久綁定到平台。

L1 可不輪替角色；L2 可用輪替進行診斷；受控 L3 Conformance 至少應輪替一次。同一角色換平台後結論改變時，必須先檢查指令、輸入、狀態、Adapter、模型與契約差異，不能直接把分歧當成證據。

## 執行信封

每個候選執行都產生 `collaboration-envelope`，內容包括：

- Session、Run、等級、Actor、角色、Provider 與模型識別；
- Framework Release、來源 Commit、Skill ID 與 Skill Version；
- 基礎狀態版本與 Digest；
- 編譯後指令、輸入、狀態與完整請求識別的 Digest；
- 一份符合 Schema 的 ThinkingOS 通用輸出；
- 產生時間與 Draft 生命週期資訊。

`instructionsDigest` 涵蓋 Provider Mapping 前最後的 `AdapterRequest.instructions` 編譯結果，而不只是來源模板或角色標籤。

協作信封包在通用輸出外層，絕不將協作欄位加入 `schemas/output.schema.json`。

## Digest Profile

Draft 協作 Digest 使用：

- 演算法：SHA-256；
- 正規化：RFC 8785 JSON Canonicalization Scheme（JCS）；
- 表示法：`sha256:` 加上 64 個小寫十六進位字元；
- 字串編碼：正規化後的 UTF-8。

分別計算 `instructionsDigest`、`inputsDigest` 與 `stateDigest`，讓分歧診斷能辨認改變的部分。`caseDigest` 涵蓋 Framework Identity、Skill Identity、Input Digest 與 State Digest，讓不同角色能歸屬同一案例；`requestDigest` 再涵蓋角色與 Instruction Digest，用來識別完整執行請求。

Digest 用於確認相等性與連續性，不是簽章、身分證明、機密控制，也不能證明來源內容為真。低熵敏感值即使經過雜湊仍可能被猜中；Host 應減少敏感輸入，而不是依靠 Digest 保護隱私。

## 單一寫入者與狀態譜系

AI Actor 不得直接修改已提交的 Conversation State，只能根據宣告的基礎狀態回傳候選信封。Arbiter 是唯一寫入者，依序套用被接受的發現。

每個 `sessionId` 只有一條已提交的狀態譜系。多個候選執行可以共用 Session、`baseStateVersion` 與 `baseStateDigest`；它們是平行提案，不是狀態分叉。

如果仲裁必須保留兩個以上互不相容的正式後繼狀態，應以 `parentSessionId` 與 `forkedFromStateVersion` 建立子 Session。同一 Session 絕不能有兩個已提交後繼狀態。

使用舊狀態版本或不同 Base Digest 的信封已過期，合併前必須拒絕或重新執行。

## 仲裁紀錄

仲裁紀錄引用候選 `runId`，並為每個候選指定：

- `accepted`、`rejected` 或 `partial`；
- 精簡且以證據為基礎的理由；
- 當結果為 `partial` 時，以 JSON Pointer 表示的 `acceptedPaths`。

Partial Path 必須以不可變候選輸出為基準，且必須存在、不得重疊，並準確指出接受的值。

紀錄也保存分歧分類、證據引用、Never Rule 違反、Rubric 發現、仲裁者身分與類型、人類核准，以及結果狀態的版本與 Digest。L3 仲裁必須取得明確的人類核准。

## State Chain 與 Record Chain

每次仲裁轉換必須滿足：

```text
resultStateVersion = baseStateVersion + 1
next.baseStateDigest = previous.resultStateDigest
next.previousRecordDigest = previous.recordDigest
```

Session 的第一筆紀錄，其 `previousRecordDigest` 為 `null`。計算 `recordDigest` 時：

1. 複製完整仲裁紀錄。
2. 完全移除 `recordDigest` 屬性。
3. 依 RFC 8785 正規化剩餘物件。
4. 對正規化後的 UTF-8 Bytes 計算 SHA-256。
5. 以 `sha256:` 前綴加小寫結果保存。

Digest Chain 只能相對於可信任錨點提供連續性與竄改跡象；本身不能提供身分、真實性或不可否認性。受保護 Git Branch 與經驗證的 Signed Release Tag 可作為已提交紀錄的錨點，但仍受 Repository 與簽署金鑰治理限制。Runtime 紀錄在 Commit 或被 Host 以其他方式保護前，仍未被錨定。

## 分歧診斷

修改 Skill 契約前，應依序診斷可重現的分歧：

1. 比較 Framework、Skill 與 Source Commit Identity。
2. 比較 Instruction、Input、State 與 Request Digest。
3. 拒絕過期的 Base State 與不合 Schema 的輸出。
4. 檢查 Adapter Mapping 與 Fail-closed Parsing。
5. 重複受控執行，估計抽樣隨機性。
6. 分類剩餘分歧。

分類包括 Input、State、Instruction 或 Version Mismatch；Adapter 或 Schema Nonconformance；Stochastic Variance；Model Nonconformance；Contract Ambiguity；以及 Unresolved Divergence。

不同分類應進入不同改進路徑：

- Adapter Nonconformance 轉成 Adapter 契約測試；
- Schema Nonconformance 轉成 Parser 或 Validation 測試；
- Model Variance 回饋角色與 Provider 組態；
- 經確認的 Contract Ambiguity 轉成 Skill 或協作迴歸案例。

分歧不會自動證明 Skill 契約含糊。

## 合成 Fixtures

Repository Fixtures 必須完全合成，並宣告：

```json
{
  "synthetic": true,
  "containsRealUserData": false
}
```

Fixture 內容或 Digest 都不得源自真實使用者對話、私人狀態、憑證或敏感來源。Schema 驗證只能確認聲明，貢獻審查仍須確認資料來源。

## Draft Schema 生命週期

Draft Schema 使用版本化 Canonical `$id`、`x-thinkingos-lifecycle: draft` 與 `x-thinkingos-stability: experimental`。Draft Identifier 可在正式發布前改變，不得視為穩定相依項目。

完成受控 Conformance 與審查後，Released Schema 取得穩定且遵循語意化版本的 `$id`。無版本 URL 可以解析到最新相容 Released Version，但長期保存紀錄必須保留驗證時使用的精確版本化 Identifier。

## Conformance

Contract Conformance 使用合成正向、反向 Fixtures 與跨欄位測試。正式發布前，Mapping 至少要通過一個具有 Structured Output 能力的 Provider API Adapter 及 MCP Adapter。受控 Live Interoperability 是 Release Gate；之後的生產經驗用於改進，但不得把私人對話放入 Repository。

Reference Coordinator 必須維持非規範性、無狀態，並服從本契約。
