/**
 * This file contains code and logic for Side Bar
 */

const toggleBtn = document.getElementById("toggleSidebar");
const sidebar = document.getElementById("sidebar");

// On page load, check localStorage and set sidebar state
window.addEventListener("DOMContentLoaded", () => {
    const collapsed = localStorage.getItem("sidebar-collapsed");
    if (collapsed === "true") {
        sidebar.classList.add("collapsed");
    } else {
        sidebar.classList.remove("collapsed");
    }
});

if (toggleBtn){
    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        // Save current collapsed state to localStorage
        const isCollapsed = sidebar.classList.contains("collapsed");
        localStorage.setItem("sidebar-collapsed", isCollapsed);
    });
}

function switchSidebarPage(pageName) {

    // Hide dashboard sub-pages ONLY
    document.querySelectorAll(".dash-page").forEach(p => {
        p.classList.add("hidden");
        p.classList.remove("active");
    });

    // Show selected
    const activePage = document.querySelector(`.dash-${pageName}`);
    if (activePage) {
        activePage.classList.remove("hidden");
        activePage.classList.add("active");
    }

    // Sidebar active state
    document.querySelectorAll(".sidebar-item").forEach(item => {
        item.classList.remove("active");
    });

    document.querySelector(`.sidebar-item[data-page="${pageName}"]`)
        ?.classList.add("active");

    window.scrollTo(0, 0);
}

document.querySelectorAll(".sidebar-item").forEach(item => {
    item.addEventListener("click", () => {
        const page = item.dataset.page;
        switchSidebarPage(page);
    });
});

function initCustomSelect(selectId, options, onSelect) {
    const container = document.getElementById(selectId);
    const display = container.querySelector(".select-display");
    const dropdown = container.querySelector(".select-dropdown");
    const search = container.querySelector(".select-search");
    const list = container.querySelector(".options-list");

    let currentOptions = options;

    function renderOptions(items) {
        list.innerHTML = "";
        items.forEach(item => {
            const div = document.createElement("div");
            div.classList.add("option-item");
            div.textContent = item;

            div.addEventListener("click", (e) => {
                e.stopPropagation();  // prevents immediate close conflict

                display.textContent = item;
                dropdown.classList.add("hidden");
                onSelect(item);
            });

            list.appendChild(div);
        });
    }

    renderOptions(options);

    // Toggle dropdown
    display.addEventListener("click", (e) => {
        e.stopPropagation(); 

        dropdown.classList.toggle("hidden");
        search.value = "";
        renderOptions(currentOptions);
    });
    // Search filter
    search.addEventListener("input", () => {
        const value = search.value.toLowerCase();
        const filtered = currentOptions.filter(opt =>
            opt.toLowerCase().includes(value)
        );
        renderOptions(filtered);
    });

    // Close on outside click
    document.addEventListener("click", (e) => {
        if (!container.contains(e.target)) {
            dropdown.classList.add("hidden");
        }
    });
}

function initializeAnalyticsSelectors() {

    // RESET FIRST
    resetCustomSelect("datasetSelect");
    resetCustomSelect("columnSelect");

    // Dataset dropdown
    initCustomSelect(
        "datasetSelect",
        filesStore.map(f => f.file.name),
        (selected) => {

            const index = filesStore.findIndex(f => f.file.name === selected);
            selectedDatasetIndex = index;

            const data = filesStore[index].data;

            const columns =
                data.meta?.columns_list ||
                Object.keys(data.descriptive?.profile || {});
            
            selectedColumn = null;

            resetAnalyticsUI();

            // RESET column before re-init
            resetCustomSelect("columnSelect");

            initCustomSelect(
                "columnSelect",
                columns,
                handleColumnChange
            );
        }
    );
}

function resetCustomSelect(selectId) {
    const container = document.getElementById(selectId);

    container.innerHTML = `
        <div class="select-display">Select ${selectId === "datasetSelect" ? "dataset" : "column"}</div>
        <div class="select-dropdown hidden">
            <input type="text" class="select-search" placeholder="Search...">
            <div class="options-list"></div>
        </div>
    `;
}

function handleColumnChange(column) {
    selectedColumn = column;
    const data = filesStore[selectedDatasetIndex].data;

    updateAnalyticsUI(data, column);
}

function updateAnalyticsUI(data, column) {

    const colData = data.descriptive?.profile?.[column];

    if (!colData) return;

    // Summary
    document.getElementById("colName").textContent = column;
    document.getElementById("colType").textContent = colData.type;

    // Numerical
    document.getElementById("colMissing").textContent = formatNumber(colData.missing_pct) + "%";
    document.getElementById("colMean").textContent = formatNumber(colData.mean);
    document.getElementById("colMedian").textContent = formatNumber(colData.median);
    document.getElementById("colStd").textContent = formatNumber(colData.std);
    document.getElementById("colSkew").textContent = formatNumber(colData.skew);

    // Categorical
    document.getElementById("colUnique").textContent = colData.n_unique ?? "-";
    document.getElementById("topValue").textContent = colData.top_value ?? "-";
    document.getElementById("topValueFreq").textContent = colData.top_freq ?? "-";
    
    renderDiagnostics(data, column);
    renderPrimaryChart(colData);
    renderSecondaryChart(colData);
}

function resetAnalyticsUI() {
    document.getElementById("colName").textContent = "-";
    document.getElementById("colType").textContent = "-";

    // Numerical
    document.getElementById("colMissing").textContent = "-";
    document.getElementById("colMean").textContent = "-";
    document.getElementById("colMedian").textContent = "-";
    document.getElementById("colStd").textContent = "-";
    document.getElementById("colSkew").textContent = "-";

    // Categorical
    document.getElementById("colUnique").textContent = "-";
    document.getElementById("topValue").textContent = "-";
    document.getElementById("topValueFreq").textContent = "-";

}

function formatNumber(value) {
    if (value === null || value === undefined) return "-";

    const num = Number(value);
    if (isNaN(num)) return value;

    return num.toFixed(2);
}

function getColumnDiagnostics(data, column) {
    const allIssues = data.col_diagnostics || [];

    return allIssues.filter(issue => issue.column === column);
}

function renderDiagnostics(data, column) {

    const container = document.getElementById("diagList");
    container.innerHTML = "";

    const severityOrder = {
        high: 1,
        medium: 2,
        low: 3
    };

    const issues = getColumnDiagnostics(data, column)
        .filter(issue => issue.meta?.has_issue)
        .sort((a, b) => {
            const s1 = severityOrder[a.meta?.severity || "low"];
            const s2 = severityOrder[b.meta?.severity || "low"];
            return s1 - s2;
        });

    if (!issues.length) {
        container.innerHTML = `<div class="no-issues">No issues detected</div>`;
        return;
    }

    issues.forEach(issue => {

        const severity = issue.meta.severity || "low";

        const div = document.createElement("div");
        div.className = `diag-item diag-${severity}`;

        div.innerHTML = `
            <div class="diag-header">
                <span class="diag-type">${formatIssueTitle(issue.type)}</span>
                <span class="diag-severity">${severity.toUpperCase()}</span>
            </div>
            <div class="diag-desc">
                ${formatIssueDescription(issue)}
            </div>
        `;

        container.appendChild(div);
    });
}

function formatIssueTitle(type) {
    return type.replace(/_/g, " ").toUpperCase();
}

function formatIssueDescription(issue) {

    const d = issue.data;

    if (issue.type === "missing") {
        return `${d.details.missing_pct}% values are missing (${d.details.missing_count} rows)`;
    }

    if (issue.type === "outliers") {
        return `${d.details.outlier_pct}% values are outliers`;
    }

    if (issue.type === "distribution") {
        return `Highly skewed distribution (skew = ${d.details.skew})`;
    }

    if (issue.type === "type_issue") {
        return `${d.expected_type} stored as ${d.current_type}`;
    }

    if (issue.type === "imbalanced") {
        return `Target column is imbalanced with "${d.details.dominating_value}" class dominating`;
    }

    if (issue.type === "constant") {
        return `This column contains constant values`;
    }

    return "Issue detected in column";
}