const $ = (id) => document.getElementById(id);

async function jsonRequest(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    '"': "&quot;",
  }[character]));
}

function metric(label, value) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

async function decideApproval(approvalId, approved) {
  const reviewer = $("reviewerName").value.trim() || "Demo Reviewer";
  const result = await jsonRequest(`/api/v1/approvals/${encodeURIComponent(approvalId)}/decision`, {
    method: "POST",
    body: JSON.stringify({
      approved,
      decided_by: reviewer,
      execute_synthetic_action: approved,
      comment: approved ? "Approved through public synthetic demo." : "Rejected through public synthetic demo.",
    }),
  });

  const approval = result.approval;
  const execution = result.execution;
  $("approval").innerHTML = `
    <strong>Decision recorded: ${escapeHtml(approval.status)}</strong><br>
    <span>Reviewer: ${escapeHtml(approval.decided_by)}</span><br>
    <small>${execution ? `Synthetic execution success: ${escapeHtml(execution.success)}` : "No write executed."}</small>`;
}

function render(result) {
  $("decision").textContent = result.policy.decision;
  $("decision").className = `badge ${result.policy.decision}`;
  $("answer").textContent = result.answer;

  $("citations").innerHTML = result.citations.length
    ? result.citations.map((item) => `
      <div class="card">
        <strong>${escapeHtml(item.document_id)} — ${escapeHtml(item.title)}</strong>
        <small>${escapeHtml(item.source)} · retrieval score ${escapeHtml(item.score.toFixed(3))}</small>
        <div>${escapeHtml(item.excerpt)}</div>
      </div>`).join("")
    : '<span class="muted">No citations returned for this decision.</span>';

  const evaluation = result.evaluation;
  $("evaluation").innerHTML = [
    metric("Groundedness", evaluation.groundedness.toFixed(2)),
    metric("Citation coverage", evaluation.citation_coverage.toFixed(2)),
    metric("Policy consistency", evaluation.policy_consistency.toFixed(2)),
    metric("Release gate", evaluation.passed_release_gate ? "PASS" : "REVIEW"),
  ].join("");

  $("trace").innerHTML = result.trace.map((step) => `
    <div class="trace-step">
      <strong>${escapeHtml(step.stage)}</strong>
      <span>${escapeHtml(step.latency_ms.toFixed(3))} ms</span>
      <code>${escapeHtml(JSON.stringify(step.detail))}</code>
    </div>`).join("");

  if (result.approval_id) {
    const approvalId = result.approval_id;
    const approvalBox = $("approval");
    approvalBox.classList.remove("hidden");
    approvalBox.innerHTML = `
      <strong>Human approval required</strong><br>
      <code>${escapeHtml(approvalId)}</code>
      <p>The proposed write has not executed.</p>
      <label for="reviewerName">Named reviewer</label>
      <input id="reviewerName" value="Demo Reviewer" maxlength="100">
      <div class="approval-actions">
        <button id="approveAction">Approve synthetic write</button>
        <button id="rejectAction" class="danger">Reject</button>
      </div>
      <small>Live Salesforce writes remain disabled by default.</small>`;
    $("approveAction").addEventListener("click", () => decideApproval(approvalId, true));
    $("rejectAction").addEventListener("click", () => decideApproval(approvalId, false));
  } else {
    $("approval").classList.add("hidden");
  }
}

$("run").addEventListener("click", async () => {
  $("run").disabled = true;
  $("answer").textContent = "Running retrieval, policy, response, and evaluation stages…";
  try {
    const result = await jsonRequest("/api/v1/assist", {
      method: "POST",
      body: JSON.stringify({
        query: $("query").value,
        case_id: $("caseId").value || null,
        requested_action: $("action").value,
        user_role: "agent",
      }),
    });
    render(result);
  } catch (error) {
    $("answer").textContent = `Error: ${error.message}`;
  } finally {
    $("run").disabled = false;
  }
});

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => {
    $("query").value = button.dataset.example;
    $("action").value = button.dataset.action;
  });
});

async function runEvaluation(endpoint, label) {
  $("benchmarkOutput").classList.remove("hidden");
  $("benchmarkOutput").textContent = `Running ${label}…`;
  try {
    const result = await jsonRequest(endpoint, { method: "POST" });
    $("benchmarkOutput").textContent = JSON.stringify(result.metrics, null, 2);
  } catch (error) {
    $("benchmarkOutput").textContent = error.message;
  }
}

$("benchmark").addEventListener("click", () => {
  runEvaluation("/api/v1/evaluations/benchmark", "synthetic benchmark");
});

$("redTeam").addEventListener("click", () => {
  runEvaluation("/api/v1/evaluations/red-team", "red-team suite");
});

jsonRequest("/api/v1/health")
  .then((health) => {
    $("status").textContent = `${health.status.toUpperCase()} · ${health.model_provider} · ${health.integrations.salesforce_mode}`;
  })
  .catch(() => { $("status").textContent = "Runtime unavailable"; });
