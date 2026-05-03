
/**
 * 
 * This file contains frontend logic for rendering the main Report page
 * in the FitLater dashboard. It provides utility functions to:
 *   - Orchestrate rendering of summary statistics, column diagnostics, and advisory sections
 *   - Build summary information from API responses
 *   - Render report cards with core metrics (rows, columns, missing values, outliers, duplicates)
 *   - Serve as the controller layer for tying together different report components
 * 
 * Used by: main dashboard/report interface to update UI based on backend report data.
 * 
 */


/* =========================
   REPORT CONTROLLER
========================= */

function renderReport(response) {
    if (!response) return;

    renderSummary(buildSummary(response));
    renderReportDiagnostics(response.col_diagnostics);
    renderAdvisory(response.advisory);
}


/* =========================
   SUMMARY
========================= */

function buildSummary(res) {
    return {
        rows: res.meta?.rows || 0,
        columns: res.meta?.columns || 0,
        missing: res.diagnostics?.missing?.percentage || 0,
        outliers: res.diagnostics?.outliers?.percentage || 0,
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
        duplicates: [],
        constant: [],
        imbalance: [],
        correlation: []
    };

    issues.forEach(issue => {
        if (!issue.meta?.has_issue) return;

        switch (issue.type) {
            case "missing":
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
            case "constant":
                grouped.constant.push(issue);
                break;
            case "imbalance":
                grouped.imbalance.push(issue);
                break;
            case "corr":
                grouped.correlation.push(issue);
                break;
        }
    });

    return grouped;
}

function renderReportDiagnostics(colDiagnostics) {
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
    renderDiagList("report-distribution-list", grouped.distribution);
    renderDiagList("report-duplicates-list", grouped.duplicates);
    renderDiagList("report-constant-list", grouped.constant);
    renderDiagList("report-imbalance-list", grouped.imbalance);
    renderDiagList("report-correlation-list", grouped.correlation);
}

function renderDiagList(id, items) {
    const container = document.getElementById(id);
    if (!container) return;

    container.innerHTML = "";

    if (!Array.isArray(items) || items.length === 0) {
        container.appendChild(createDiagItem("No issues found", null));
        return;
    }

    const priorityMap = { "high": 1, "medium": 2, "low": 3 };
    items.sort((a, b) => {
        const pA = priorityMap[a.meta?.severity] || 4;
        const pB = priorityMap[b.meta?.severity] || 4;
        return pA - pB;
    });

    items.forEach(item => {
        const text = formatDiagItem(item);
        const severity = item.meta?.severity;
        container.appendChild(createDiagItem(text, severity));
    });
}

function createDiagItem(text, severity) {
    const el = document.createElement("div");
    el.className = "diag-item";
    if (severity) {
        el.classList.add(severity);
    }
    el.textContent = text;
    return el;
}

function formatDiagItem(issue) {
    const col = issue.column;
    const details = issue.data?.details || {};
    const type = issue.type;

    if (type === "missing") {
        return `${col} → ${details.missing_count} missing (${details.missing_pct}%)`;
    }

    if (type === "outliers") {
        return `${col} → ${details.outlier_pct || 0}% outliers`;
    }

    if (type === "type_issue") {
        return `${col} → Type mismatch (Current Type : ${issue.data.current_type}, Expected Type : ${issue.data.expected_type})`;
    }

    if (type === "distribution") {
        return `${col} → Skew detected (${details.skew || "N/A"})`;
    }

    if (type === "duplicates") {
        return `${col} → ${details.duplicate_pct || 0}% duplicates`;
    }

    if (type === "constant") {
        return `${col} → Constant column`;
    }

    if (type === "imbalance") {
        return `${col} → Imbalanced column`;
    }

    if (type === "corr") {
        const col1 = issue.column?.column_1;
        const col2 = issue.column?.column_2;
        const corr = details.correlation;
    
        return `${col1} ↔ ${col2} : High correlation (${corr})`;
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
        container.appendChild(createAdviceItem({ recommendation: "No recommendations" }));
        return;
    }

    list.forEach(item => {
        container.appendChild(createAdviceItem(item));
    });
}

function createAdviceItem(item) {
    const el = document.createElement("div");
    el.className = "advice-item";
    
    const recText = `${item.column ? item.column + ' : ' : ''}${item.recommendation || ""}`;
    
    const recEl = document.createElement("div");
    recEl.className = "rec";
    recEl.textContent = recText;
    el.appendChild(recEl);
    
    if (item.reason) {
        const reasonEl = document.createElement("div");
        reasonEl.className = "reason";
        reasonEl.textContent = item.reason;
        el.appendChild(reasonEl);
    }
    
    return el;
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