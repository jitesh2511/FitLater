/* =========================
   REPORT CONTROLLER
========================= */

function renderReport(response) {
    if (!response) return;

    renderSummary(buildSummary(response));
    renderDiagnostics(response.col_diagnostics);
    renderAdvisory(response.advisory);
}


/* =========================
   SUMMARY
========================= */

function buildSummary(res) {
    return {
        rows: res.meta?.rows || 0,
        columns: res.meta?.columns || 0,
        missing: res.diagnostics?.missing?.columns || 0,
        outliers: res.diagnostics?.outliers?.columns || 0,
        duplicates: res.diagnostics?.duplicates?.percentage || 0
    };
}

function renderSummary(summary) {
    setCard("rows", summary.rows);
    setCard("columns", summary.columns);
    setCard("missing", summary.missing);
    setCard("duplicates", summary.duplicates);
    setCard("outliers", summary.outliers);
}

function setCard(type, value) {
    const card = document.querySelector(`.report-card.${type}`);
    if (!card) return;

    toggleState(card, "result");

    const valueEl = card.querySelector(".card-value");
    if (valueEl) valueEl.textContent = value;
}


/* =========================
   DIAGNOSTICS
========================= */

function groupDiagnostics(issues) {
    const grouped = {
        missing: [],
        outliers: [],
        type_issues: [],
        distribution: [],
        duplicates: []
    };

    issues.forEach(issue => {
        if (!issue.meta?.has_issue) return;

        switch (issue.type) {
            case "missing_values":
                grouped.missing.push(issue);
                break;
            case "outliers":
                grouped.outliers.push(issue);
                break;
            case "type_issue":
                grouped.type_issues.push(issue);
                break;
            case "distribution":
                grouped.distribution.push(issue);
                break;
            case "duplicates":
                grouped.duplicates.push(issue);
                break;
        }
    });

    return grouped;
}

function renderDiagnostics(colDiagnostics) {
    const wrapper = document.querySelector(".diagnostics-section");

    if (!Array.isArray(colDiagnostics) || colDiagnostics.length === 0) {
        toggleState(wrapper, "empty");
        return;
    }

    toggleState(wrapper, "result");

    const grouped = groupDiagnostics(colDiagnostics);

    renderDiagList("report-missing-list", grouped.missing);
    renderDiagList("report-outliers-list", grouped.outliers);
    renderDiagList("report-types-list", grouped.type_issues);
}

function renderDiagList(id, items) {
    const container = document.getElementById(id);
    if (!container) return;

    container.innerHTML = "";

    if (!Array.isArray(items) || items.length === 0) {
        container.appendChild(createDiagItem("No issues found"));
        return;
    }

    items.forEach(item => {
        const text = formatDiagItem(item);
        container.appendChild(createDiagItem(text));
    });
}

function createDiagItem(text) {
    const el = document.createElement("div");
    el.className = "diag-item";
    el.textContent = text;
    return el;
}

function formatDiagItem(issue) {
    const col = issue.column;
    const details = issue.data?.details || {};
    const type = issue.type;

    if (type === "missing_values") {
        return `${col} → ${details.missing_count} missing (${details.missing_pct}%)`;
    }

    if (type === "outliers") {
        return `${col} → ${details.outlier_count || 0} outliers`;
    }

    if (type === "type_issue") {
        return `${col} → Type mismatch (${issue.data.current_type})`;
    }

    if (type === "distribution") {
        return `${col} → Skew detected (${details.skew || "N/A"})`;
    }

    return `${col} → Issue detected`;
}


/* =========================
   ADVISORY
========================= */

function renderAdvisory(advisory) {
    const wrapper = document.querySelector(".advisory-section");

    if (!advisory) {
        toggleState(wrapper, "empty");
        return;
    }

    toggleState(wrapper, "result");

    renderAdviceList("report-adv-high", advisory.high);
    renderAdviceList("report-adv-medium", advisory.medium);
    renderAdviceList("report-adv-low", advisory.low);
}

function renderAdviceList(id, list) {
    const container = document.getElementById(id);
    if (!container) return;

    container.innerHTML = "";

    if (!list || list.length === 0) {
        container.appendChild(createAdviceItem("No recommendations"));
        return;
    }

    list.forEach(item => {
        container.appendChild(createAdviceItem(formatAdvice(item)));
    });
}

function createAdviceItem(text) {
    const el = document.createElement("div");
    el.className = "advice-item";
    el.textContent = text;
    return el;
}

function formatAdvice(item) {
    if (!item) return "";

    return `${item.column || "General"} → ${item.recommendation || ""}`;
}


/* =========================
   STATE HANDLER
========================= */

function toggleState(parent, state) {
    const states = parent.querySelectorAll(".state");

    states.forEach(s => s.classList.add("hidden"));

    const target = parent.querySelector(`.state-${state}`);
    if (target) target.classList.remove("hidden");
}