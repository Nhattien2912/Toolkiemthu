function buildHistoryChart() {
  const canvas = document.getElementById("historyChart");
  if (!canvas || typeof Chart === "undefined") {
    return;
  }

  const labels = JSON.parse(canvas.dataset.labels || "[]");
  const values = JSON.parse(canvas.dataset.values || "[]");
  const colors = JSON.parse(canvas.dataset.colors || "[]");

  if (!labels.length) {
    return;
  }

  new Chart(canvas, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Pass rate (%)",
        data: values,
        backgroundColor: colors,
        borderRadius: 10,
        borderSkipped: false
      }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label(context) {
              return `${context.parsed.y.toFixed(1)}%`;
            }
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#9da7b3" },
          grid: { display: false }
        },
        y: {
          min: 0,
          max: 100,
          ticks: {
            color: "#9da7b3",
            callback(value) {
              return `${value}%`;
            }
          },
          grid: { color: "rgba(255,255,255,0.08)" }
        }
      }
    }
  });
}

function buildModuleTrendChart() {
  const canvas = document.getElementById("moduleTrendChart");
  if (!canvas || typeof Chart === "undefined") {
    return;
  }

  const labels = JSON.parse(canvas.dataset.labels || "[]");
  const datasets = JSON.parse(canvas.dataset.datasets || "[]");
  if (!labels.length || !datasets.length) {
    return;
  }

  new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: datasets.map((dataset) => ({
        ...dataset,
        tension: 0.25,
        borderWidth: 2,
        fill: false,
        spanGaps: true,
        pointRadius: 3
      }))
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: "#c8d7e1" }
        },
        tooltip: {
          callbacks: {
            label(context) {
              const value = context.parsed.y;
              return value == null
                ? `${context.dataset.label}: no data`
                : `${context.dataset.label}: ${value.toFixed(1)}%`;
            }
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#9da7b3" },
          grid: { color: "rgba(255,255,255,0.04)" }
        },
        y: {
          min: 0,
          max: 100,
          ticks: {
            color: "#9da7b3",
            callback(value) {
              return `${value}%`;
            }
          },
          grid: { color: "rgba(255,255,255,0.08)" }
        }
      }
    }
  });
}

function shortenTestId(testId) {
  if (!testId) {
    return "-";
  }
  return testId
    .replace(/^tests[\\/]/i, "")
    .replace(/^\.?[\\/]/, "")
    .replace(/\s+/g, " ");
}

function createExecutionTracker() {
  const refs = {
    phase: document.getElementById("execution-phase"),
    total: document.getElementById("execution-total"),
    completed: document.getElementById("execution-completed"),
    passed: document.getElementById("execution-passed"),
    failed: document.getElementById("execution-failed"),
    skipped: document.getElementById("execution-skipped"),
    current: document.getElementById("execution-current"),
    step: document.getElementById("execution-step"),
    last: document.getElementById("execution-last"),
    activity: document.getElementById("execution-activity"),
    progressFill: document.getElementById("execution-progress-fill"),
    progressCopy: document.getElementById("execution-progress-copy")
  };

  const enabled = Object.values(refs).some(Boolean);
  if (!enabled) {
    return {
      processChunk() {},
      resetForSuite() {},
      setPhase() {},
      syncFromText() {},
      hasMeaningfulProgress() { return false; }
    };
  }

  const state = {
    collected: null,
    completed: 0,
    passed: 0,
    failed: 0,
    skipped: 0,
    currentTest: "-",
    lastStep: "-",
    lastLine: "-",
    phase: "Idle",
    activity: [],
    completedTests: new Set()
  };

  function setText(element, value) {
    if (element) {
      element.textContent = value;
    }
  }

  function pushActivity(entry) {
    if (!entry) {
      return;
    }
    if (state.activity[0] !== entry) {
      state.activity.unshift(entry);
      state.activity = state.activity.slice(0, 5);
    }
  }

  function renderActivity() {
    if (!refs.activity) {
      return;
    }
    refs.activity.innerHTML = "";
    const items = state.activity.length ? state.activity : ["Chua co su kien noi bat."];
    items.forEach((entry) => {
      const item = document.createElement("li");
      item.textContent = entry;
      refs.activity.appendChild(item);
    });
  }

  function render() {
    const total = state.collected;
    const completed = state.completed;
    const percent = total ? Math.min(100, Math.round((completed / total) * 100)) : 0;

    setText(refs.phase, state.phase);
    setText(refs.total, total == null ? "-" : String(total));
    setText(refs.completed, String(completed));
    setText(refs.passed, String(state.passed));
    setText(refs.failed, String(state.failed));
    setText(refs.skipped, String(state.skipped));
    setText(refs.current, shortenTestId(state.currentTest));
    setText(refs.step, state.lastStep || "-");
    setText(refs.last, state.lastLine || "-");

    if (refs.progressFill) {
      refs.progressFill.style.width = `${percent}%`;
    }

    if (refs.progressCopy) {
      if (total == null) {
        refs.progressCopy.textContent = "Dang cho thong tin collected tu pytest...";
      } else {
        refs.progressCopy.textContent = `${completed}/${total} case da hoan thanh (${percent}%). Passed ${state.passed}, failed ${state.failed}, skipped ${state.skipped}.`;
      }
    }

    renderActivity();
  }

  function setPhase(nextPhase) {
    if (!nextPhase) {
      return;
    }
    state.phase = nextPhase;
    render();
  }

  function hasMeaningfulProgress() {
    return state.collected != null || state.completed > 0 || state.lastLine !== "-";
  }

  function resetForSuite(suiteData) {
    state.collected = null;
    state.completed = 0;
    state.passed = 0;
    state.failed = 0;
    state.skipped = 0;
    state.currentTest = suiteData?.label || "-";
    state.lastStep = "Dang khoi tao suite tu dashboard.";
    state.lastLine = suiteData?.command || "Dang chuan bi chay pytest...";
    state.phase = "Queued";
    state.activity = [];
    state.completedTests.clear();
    pushActivity(`Queued: ${suiteData?.label || "pytest suite"}`);
    render();
  }

  function markResult(testId, status) {
    const normalizedStatus = status.toUpperCase();
    const key = `${testId}::${normalizedStatus}`;
    if (state.completedTests.has(key)) {
      return;
    }

    state.completedTests.add(key);
    if (normalizedStatus === "PASSED") {
      state.passed += 1;
    } else if (normalizedStatus === "FAILED" || normalizedStatus === "ERROR") {
      state.failed += 1;
    } else if (normalizedStatus === "SKIPPED") {
      state.skipped += 1;
    }
    state.completed = state.passed + state.failed + state.skipped;
  }

  function processLine(rawLine) {
    const trimmed = rawLine.replace(/\r/g, "").trim();
    if (!trimmed) {
      return;
    }

    state.lastLine = trimmed;

    if (/^=+ test session starts/i.test(trimmed)) {
      state.phase = "Starting";
      pushActivity("Pytest session started");
    }

    if (/^collecting\b/i.test(trimmed)) {
      state.phase = "Collecting";
    }

    const collectedMatch = trimmed.match(/\bcollected\s+(\d+)\s+items?\b/i);
    if (collectedMatch) {
      state.collected = Number.parseInt(collectedMatch[1], 10);
      state.phase = "Running";
      pushActivity(`Collected ${state.collected} test cases`);
      render();
      return;
    }

    const stepMatch = trimmed.match(/\[STEP [^\]]+\]\s*(.+)$/);
    if (stepMatch) {
      state.lastStep = stepMatch[1];
      if (state.phase !== "Paused") {
        state.phase = "Running";
      }
      pushActivity(`Step: ${state.lastStep}`);
    }

    const inlineResultMatch = trimmed.match(/((?:[A-Za-z]:)?\S+?\.py::\S+)\s+(PASSED|FAILED|SKIPPED|ERROR)\b/i);
    if (inlineResultMatch) {
      state.currentTest = inlineResultMatch[1];
      state.lastStep = `${shortenTestId(inlineResultMatch[1])} -> ${inlineResultMatch[2].toUpperCase()}`;
      markResult(inlineResultMatch[1], inlineResultMatch[2]);
      pushActivity(`${inlineResultMatch[2].toUpperCase()}: ${shortenTestId(inlineResultMatch[1])}`);
      render();
      return;
    }

    const standaloneResultMatch = trimmed.match(/^(PASSED|FAILED|SKIPPED|ERROR)$/i);
    if (standaloneResultMatch && state.currentTest && state.currentTest !== "-") {
      state.lastStep = `${shortenTestId(state.currentTest)} -> ${standaloneResultMatch[1].toUpperCase()}`;
      markResult(state.currentTest, standaloneResultMatch[1]);
      pushActivity(`${standaloneResultMatch[1].toUpperCase()}: ${shortenTestId(state.currentTest)}`);
      render();
      return;
    }

    const testIdMatch = trimmed.match(/((?:[A-Za-z]:)?\S+?\.py::\S+)/);
    if (testIdMatch && !/short test summary info/i.test(trimmed) && !/^=+/.test(trimmed)) {
      const nextTest = testIdMatch[1];
      if (state.currentTest !== nextTest) {
        state.currentTest = nextTest;
        if (state.phase !== "Paused") {
          state.phase = "Running";
        }
        pushActivity(`Running: ${shortenTestId(nextTest)}`);
      }
      render();
      return;
    }

    if (/^\[dashboard\].*paused/i.test(trimmed)) {
      state.phase = "Paused";
      pushActivity("Suite paused from dashboard");
      render();
      return;
    }

    if (/^\[dashboard\].*(resume|resum)/i.test(trimmed)) {
      state.phase = "Running";
      pushActivity("Suite resumed from dashboard");
      render();
      return;
    }

    const exitCodeMatch = trimmed.match(/\[dashboard\] Pytest finished with exit code\s+(-?\d+)/i);
    if (exitCodeMatch) {
      state.phase = Number.parseInt(exitCodeMatch[1], 10) === 0 ? "Completed" : "Completed with failures";
      pushActivity(`Finished with exit code ${exitCodeMatch[1]}`);
      render();
      return;
    }

    if (/Log stream disconnected/i.test(trimmed)) {
      state.phase = "Disconnected";
      pushActivity("Log stream disconnected");
      render();
      return;
    }

    if (/No active pytest run/i.test(trimmed)) {
      pushActivity(trimmed);
      render();
      return;
    }

    if (trimmed.includes(" in ") && /\b(passed|failed|skipped|error)\b/i.test(trimmed)) {
      pushActivity(trimmed);
    }

    render();
  }

  function processChunk(chunk) {
    chunk.split("\n").forEach(processLine);
  }

  function syncFromText(text) {
    const snapshot = text.trim();
    if (!snapshot || /Click "Run Suite" to start pytest/i.test(snapshot) || /Quick-run log/i.test(snapshot)) {
      render();
      return;
    }
    processChunk(snapshot);
  }

  render();

  return {
    processChunk,
    resetForSuite,
    setPhase,
    syncFromText,
    hasMeaningfulProgress
  };
}

function attachRunSuiteHandler() {
  const button = document.getElementById("run-suite-button");
  const toggleButton = document.getElementById("toggle-run-button");
  const quickButtons = Array.from(document.querySelectorAll(".quick-run-button"));
  const logPanel = document.getElementById("live-log-panel");
  const statusBadge = document.getElementById("run-status-badge");
  const suiteSelector = document.getElementById("suite-selector");
  const suiteMeta = document.getElementById("selected-suite-meta");
  const suiteCommand = document.getElementById("selected-suite-command");
  const tracker = createExecutionTracker();

  let shouldFollowLog = true;
  let currentPaused = statusBadge ? statusBadge.textContent.trim().toLowerCase() === "paused" : false;

  function isNearBottom(element) {
    if (!element) {
      return true;
    }
    const threshold = 48;
    return element.scrollHeight - element.scrollTop - element.clientHeight <= threshold;
  }

  function appendLogLine(line) {
    if (!logPanel) {
      return;
    }
    const followAfterAppend = shouldFollowLog || isNearBottom(logPanel);
    logPanel.textContent += line;
    tracker.processChunk(line);
    if (followAfterAppend) {
      logPanel.scrollTop = logPanel.scrollHeight;
    }
  }

  function setSuiteCommand(commandText) {
    if (!suiteCommand) {
      return;
    }
    suiteCommand.textContent = commandText || "Suite command preview will appear here.";
  }

  function renderSuiteMetaFromData(data) {
    if (!suiteMeta) {
      return;
    }
    suiteMeta.innerHTML = `
      <span><strong>Suite:</strong> ${data.label || data.id || "-"}</span>
      <span><strong>Method:</strong> ${data.method || "Pytest automation"}</span>
      <span><strong>Browser:</strong> Headless background</span>
      <span>${data.description || "Suite se chay trong nen va cap nhat log truc tiep tren web."}</span>
    `;
    setSuiteCommand(data.command || "");
  }

  function getSelectorSuiteData() {
    if (!suiteSelector) {
      return null;
    }
    const selected = suiteSelector.options[suiteSelector.selectedIndex];
    return {
      id: selected.value,
      label: selected.dataset.label,
      method: selected.dataset.method,
      description: selected.dataset.description,
      command: selected.dataset.command
    };
  }

  function setRunningState(isRunning, paused = false) {
    currentPaused = paused;

    if (statusBadge) {
      statusBadge.textContent = paused ? "Paused" : (isRunning ? "Running" : "Idle");
      statusBadge.classList.toggle("status-running", isRunning && !paused);
      statusBadge.classList.toggle("status-paused", paused);
      statusBadge.classList.toggle("status-idle", !isRunning && !paused);
    }

    if (button) {
      button.disabled = isRunning;
    }
    if (toggleButton) {
      toggleButton.disabled = !isRunning;
      toggleButton.textContent = paused ? "Tiep tuc" : "Tam dung";
    }

    quickButtons.forEach((quickButton) => {
      quickButton.disabled = isRunning;
    });

    if (paused) {
      tracker.setPhase("Paused");
    } else if (isRunning) {
      tracker.setPhase("Running");
    } else if (!tracker.hasMeaningfulProgress()) {
      tracker.setPhase("Idle");
    }
  }

  async function startSuiteRun(suiteData) {
    setRunningState(true, false);
    renderSuiteMetaFromData(suiteData);
    tracker.resetForSuite(suiteData);

    if (logPanel) {
      logPanel.textContent = "";
      shouldFollowLog = true;
      appendLogLine(`[dashboard] Triggering suite: ${suiteData.id}\n`);
    }

    const response = await fetch("/run-suite", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ suite_id: suiteData.id })
    });
    const payload = await response.json();

    if (!response.ok) {
      if (logPanel) {
        appendLogLine(`${payload.message}\n`);
      }
      setRunningState(false, false);
      return;
    }

    if (payload.command_preview) {
      setSuiteCommand(payload.command_preview);
    }

    const source = new EventSource("/stream-log");
    source.addEventListener("log", (event) => {
      const data = JSON.parse(event.data);
      appendLogLine(data.line);
    });

    source.addEventListener("done", (event) => {
      const data = JSON.parse(event.data);
      if (logPanel && data.line && data.line !== "__RUN_COMPLETE__") {
        appendLogLine(data.line);
      }
      source.close();
      window.location.reload();
    });

    source.addEventListener("error", () => {
      source.close();
      if (logPanel) {
        appendLogLine("\n[dashboard] Log stream disconnected.\n");
      }
      setRunningState(false, false);
    });
  }

  async function togglePauseResume() {
    const response = await fetch("/toggle-suite-pause", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });
    const payload = await response.json();

    if (logPanel && payload.message) {
      appendLogLine(`[dashboard] ${payload.message}\n`);
    }

    if (!response.ok) {
      return;
    }

    setRunningState(true, Boolean(payload.paused));
  }

  if (!button && quickButtons.length === 0 && !toggleButton) {
    return;
  }

  if (suiteSelector) {
    suiteSelector.addEventListener("change", () => {
      const suiteData = getSelectorSuiteData();
      if (suiteData) {
        renderSuiteMetaFromData(suiteData);
      }
    });
    const initialSuiteData = getSelectorSuiteData();
    if (initialSuiteData) {
      renderSuiteMetaFromData(initialSuiteData);
    }
  }

  if (logPanel) {
    logPanel.addEventListener("scroll", () => {
      shouldFollowLog = isNearBottom(logPanel);
    });
    tracker.syncFromText(logPanel.textContent || "");
  }

  if (button) {
    button.addEventListener("click", async () => {
      const suiteData = getSelectorSuiteData() || {
        id: "full",
        label: "Full Regression",
        method: "Regression / End-to-End",
        description: "",
        command: ""
      };
      await startSuiteRun(suiteData);
    });
  }

  quickButtons.forEach((quickButton) => {
    quickButton.addEventListener("click", async () => {
      await startSuiteRun({
        id: quickButton.dataset.suiteId,
        label: quickButton.dataset.suiteLabel || quickButton.dataset.suiteId,
        method: quickButton.dataset.suiteMethod,
        description: quickButton.dataset.suiteDescription,
        command: quickButton.dataset.command
      });
    });
  });

  if (toggleButton) {
    toggleButton.addEventListener("click", togglePauseResume);
  }

  setRunningState(
    statusBadge ? statusBadge.textContent.trim().toLowerCase() !== "idle" : false,
    currentPaused
  );
}

document.addEventListener("DOMContentLoaded", () => {
  buildHistoryChart();
  buildModuleTrendChart();
  attachRunSuiteHandler();
});
