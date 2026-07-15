"use strict";

const byId = (id) => document.getElementById(id);

function appendTextList(id, values, render) {
  const list = byId(id);
  list.replaceChildren();
  if (!values.length) {
    const item = document.createElement("li");
    item.textContent = "None recorded／目前無紀錄";
    list.append(item);
    return;
  }
  values.forEach((value) => {
    const item = document.createElement("li");
    const result = render ? render(value) : { text: value };
    item.append(document.createTextNode(result.text));
    if (result.tag) {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = result.tag;
      item.append(tag);
    }
    list.append(item);
  });
}

function renderReport(data) {
  document.title = `${data.title} · ThinkingOS`;
  byId("summary").textContent = data.summary;
  byId("current-condition").textContent = data.currentCondition;
  byId("goal").textContent = data.goal;
  byId("confidence").textContent = data.confidence;
  byId("generated-at").textContent = data.generatedAt ? new Date(data.generatedAt).toLocaleString() : "Not recorded／未記錄";
  byId("next-step").textContent = data.nextStep || "No downstream transition／不進入下游技能";

  const status = byId("status");
  status.textContent = data.status;
  status.parentElement.dataset.value = data.status;

  appendTextList("obstacles", data.obstacles, (value) => ({ text: value.statement, tag: value.basis }));
  appendTextList("constraints", data.constraints, (value) => ({ text: value.statement, tag: `${value.classification} · ${value.basis}` }));
  appendTextList("success-criteria", data.successCriteria);
  appendTextList("scope-exclusions", data.scopeExclusions || []);
  appendTextList("assumptions", data.assumptions);
  appendTextList("missing-information", data.missingInformation);

  const labels = { goal: "Goal／目標", obstacle: "Obstacle／障礙", constraint: "Constraint／限制", logic: "Logic／邏輯", overall: "Overall／整體" };
  const scoreList = byId("score-list");
  scoreList.replaceChildren();
  Object.entries(data.scores || {}).forEach(([name, value]) => {
    const card = document.createElement("div");
    card.className = "score";
    const label = document.createElement("span");
    label.textContent = labels[name] || name;
    const score = document.createElement("strong");
    score.textContent = `${value}/4`;
    card.append(label, score);
    scoreList.append(card);
  });
}

fetch("report.json", { cache: "no-store" })
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(renderReport)
  .catch((error) => {
    const notice = byId("load-error");
    notice.hidden = false;
    notice.textContent = `Unable to load report.json／無法載入報告資料：${error.message}`;
    byId("status").textContent = "Unavailable";
  });

