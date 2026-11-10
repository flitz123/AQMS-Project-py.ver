const state = { queue: [], stats: {}, current: null };

const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;" })[char]);
const formatTime = (iso) => iso ? new Date(iso).toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" }) : "—";

async function api(path, options = {}) {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.message || "Request failed");
  return data;
}

function toast(message) {
  const node = $("#toast");
  node.textContent = message;
  node.classList.add("show");
  setTimeout(() => node.classList.remove("show"), 2600);
}

async function refresh() {
  try {
    const [queue, stats, report] = await Promise.all([api("/queue"), api("/stats"), api("/reports/daily")]);
    state.queue = queue;
    state.stats = stats;
    render();
    renderReports(report);
  } catch (error) {
    toast(error.message);
  }
}

function render() {
  $("#waitingCount").textContent = state.stats.waiting ?? 0;
  $("#calledCount").textContent = state.stats.called ?? 0;
  $("#servedCount").textContent = state.stats.served ?? 0;
  $("#cancelledCount").textContent = state.stats.cancelled ?? 0;

  const waiting = state.queue.filter((p) => p.status === "WAITING");
  state.current = state.queue.find((p) => p.status === "CALLED") || null;
  if (state.current) {
    $("#nowServing").textContent = state.current.name;
    $("#nowToken").textContent = state.current.token;
    $("#nowService").textContent = state.current.service_type;
    $("#nowStatus").textContent = "Being served";
    $("#serveCurrent").disabled = false;
  } else {
    $("#nowServing").textContent = "No patient called";
    $("#nowToken").textContent = "—";
    $("#nowService").textContent = "—";
    $("#nowStatus").textContent = "Available";
    $("#serveCurrent").disabled = true;
  }

  $("#queuePreview").innerHTML = waiting.slice(0, 5).map((p) => `
    <div class="queue-row"><div class="ticket">${escapeHtml(p.token.replace("T",""))}</div><div><strong>${escapeHtml(p.name)}</strong><span>${escapeHtml(p.service_type)}</span></div><div class="queue-time">${formatTime(p.arrival_time)}</div></div>
  `).join("") || `<div class="queue-row"><div></div><div><strong>No patients waiting</strong><span>The queue is clear</span></div></div>`;
  renderTable(waiting.concat(state.queue.filter((p) => p.status !== "WAITING")));
}

function renderTable(queue) {
  const term = ($("#queueSearch")?.value || "").toLowerCase();
  const filtered = queue.filter((p) => `${p.token} ${p.name} ${p.service_type} ${p.status}`.toLowerCase().includes(term));
  $("#queueTable").innerHTML = filtered.map((p) => {
    const status = p.status.toLowerCase();
    const actions = p.status === "CALLED"
      ? `<button class="icon-button" data-action="served" data-token="${p.token}" title="Mark served">✓</button>`
      : p.status === "WAITING"
        ? `<button class="icon-button" data-action="call" data-token="${p.token}" title="Call patient">→</button><button class="icon-button danger" data-action="cancelled" data-token="${p.token}" title="Cancel">×</button>`
        : "";
    return `<tr><td><strong>${escapeHtml(p.token)}</strong></td><td>${escapeHtml(p.name)}<br><small>${escapeHtml(p.national_id)}</small></td><td>${escapeHtml(p.service_type)}</td><td>${formatTime(p.arrival_time)}</td><td><span class="badge ${status}">${escapeHtml(p.status.replace("_"," "))}</span></td><td><div class="row-actions">${actions}</div></td></tr>`;
  }).join("") || `<tr><td colspan="6">No patients match this search.</td></tr>`;
}

function renderReports(report) {
  $("#dailyTotal").textContent = `${report.patient_served ?? 0} patients served today`;
  $("#dailyProgress").style.width = `${Math.min(100, ((report.patient_served || 0) / Math.max(report.stats?.waiting + report.patient_served || 1, 1)) * 100)}%`;
  $("#reportSummary").innerHTML = [
    ["Total in system", state.stats.total],
    ["Currently waiting", state.stats.waiting],
    ["Currently called", state.stats.called],
    ["Completed visits", state.stats.served],
    ["Cancelled / no-shows", state.stats.cancelled],
  ].map(([label, value]) => `<div class="report-line"><span>${label}</span><strong>${value ?? 0}</strong></div>`).join("");
}

function showView(name) {
  ["overview","queue","reports"].forEach((view) => $(`#${view}View`).classList.toggle("hidden", view !== name));
  document.querySelectorAll(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === name));
}

$("#openRegister").addEventListener("click", () => $("#registerModal").classList.remove("hidden"));
$("#closeRegister").addEventListener("click", () => $("#registerModal").classList.add("hidden"));
$("#registerModal").addEventListener("click", (event) => { if (event.target === $("#registerModal")) $("#registerModal").classList.add("hidden"); });
$("#registerForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form));
  try {
    const patient = await api("/patients", { method:"POST", body:JSON.stringify(payload) });
    $("#registerModal").classList.add("hidden");
    form.reset();
    toast(`${patient.token} created for ${patient.name}`);
    await refresh();
  } catch (error) { $("#formError").textContent = error.message; }
});

$("#callNext").addEventListener("click", async () => {
  try {
    const patient = await api("/queue/call-next", { method:"POST" });
    toast(`Calling ${patient.token} — ${patient.name}`);
    await refresh();
  } catch (error) { toast(error.message); }
});

$("#serveCurrent").addEventListener("click", async () => {
  if (!state.current) return;
  try { await api(`/patients/${state.current.token}/serve`, { method:"POST" }); toast(`${state.current.token} marked served`); await refresh(); }
  catch (error) { toast(error.message); }
});

document.querySelectorAll(".nav-item,[data-view-link]").forEach((button) => button.addEventListener("click", () => showView(button.dataset.view || button.dataset.viewLink)));
$("#queueSearch").addEventListener("input", () => renderTable(state.queue.filter((p) => p.status === "WAITING").concat(state.queue.filter((p) => p.status !== "WAITING"))));
$("#queueTable").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  const { action, token } = button.dataset;
  try {
    if (action === "served") await api(`/patients/${token}/serve`, { method:"POST" });
    else if (action === "call") await api(`/patients/${token}/call`, { method:"POST" });
    else await api(`/patients/${token}/status`, { method:"PATCH", body:JSON.stringify({ status:"CANCELLED" }) });
    await refresh();
    toast(action === "cancelled" ? `${token} cancelled` : `${token} updated`);
  } catch (error) { toast(error.message); }
});

const today = new Date();
$("#today").textContent = today.toLocaleDateString([], { weekday:"long", month:"long", day:"numeric", year:"numeric" });
refresh();
setInterval(refresh, 15000);
