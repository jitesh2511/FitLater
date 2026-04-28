let primaryChartInstance = null;
let secondaryChartInstance = null;
Chart.register(ChartDataLabels);
Chart.defaults.plugins.datalabels = false;

function renderChartByType(ctx, viz, target) {

    const legendContainer = document.getElementById("customLegend");
    if (legendContainer) {
        legendContainer.innerHTML = "";   // 🔥 clears old legend
    }
    const msg = document.getElementById("secondaryMessage");
    msg.classList.add("hidden");

    document.getElementById("secondaryChart").style.display = "block";

    let instanceRef = target === "primary"
        ? "primaryChartInstance"
        : "secondaryChartInstance";

    let chart;

    if (viz.type === "histogram") {

        let chartConfig;

        if (isDiscreteNumeric(viz)) {

            const countsMap = {};

            viz.bins.slice(0, -1).forEach((binStart, i) => {
                const count = viz.counts[i];
                if (count > 0) {
                    const label = Math.round(binStart);
                    countsMap[label] = (countsMap[label] || 0) + count;
                }
            });

            chartConfig = {
                type: "bar",
                data: {
                    labels: Object.keys(countsMap),
                    datasets: [{ data: Object.values(countsMap) }]
                }
            };

        } else {

            const labels = viz.bins.slice(0, -1).map((_, i) => {
                const start = viz.bins[i];
                const end = viz.bins[i + 1];
                return `${Math.round(start)}–${Math.round(end)}`;
            });

            chartConfig = {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{ data: viz.counts }]
                }
            };
        }

        chart = new Chart(ctx, {
            ...chartConfig,
            options: {
                plugins: {
                    datalabels: false,
                    legend: { display: false },
                    title: viz.meta
                        ? { display: true, text: viz.meta }
                        : { display: false }
                }
            }
        });
    } else if (viz.type === "bar") {

        const labels = Object.keys(viz.data || {});
        const data = Object.values(viz.data || {});

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{ data: data }]
            },
            options: {
                plugins: {
                    datalabels: false,
                    legend: { display: false },
                    title: viz.meta
                        ? { display: true, text: viz.meta }
                        : { display: false }
                }
            }
        });

    } else if (viz.type === "pie") {

        const labels = Object.keys(viz.data || {});
        const data = Object.values(viz.data || {});

        const colors = [
            "#4C9AFF",
            "#FF6384",
            "#FF9F40",
            "#FFCD56",
            "#4BC0C0",
            "#9966FF",
            "#36A2EB"
        ];

        chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    borderWidth: 2,
                    borderColor: "#0f1115",
                    hoverOffset: 8,
                    backgroundColor: colors.slice(0, data.length),

                    datalabels: {
                        color: "#fff",
                        font: {
                            weight: "bold",
                            size: 12
                        },
                        formatter: function (value, context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = (value / total) * 100;
                            return Math.round(percentage) + "%";   
                        }
                    }
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                layout: {
                    padding: 10
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    datalabels: {
                        anchor: "center",
                        align: "center",
                        clamp: true   
                    },
                    title: viz.meta
                        ? {
                            display: true,
                            text: viz.meta,
                            color: "#aaa",
                            padding: {
                                top: 0,
                                bottom: 10   
                            },
                            font: {
                                size: 13,
                                weight: "400"
                            }
                        }
                        : { display: false }
                }
            }
        });
        renderCustomLegend(labels, data, colors);
    } else if (viz.type === "line") {

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: viz.labels,
                datasets: [{
                    data: viz.values,
                    fill: false
                }]
            },
            options: {
                plugins: {
                    datalabels: false,
                    title: viz.meta
                        ? { display: true, text: viz.meta }
                        : { display: false }
                }
            }
        });

    } else if (viz.type === "boxplot") {

        if (target === "primary") {
            showChartMessage("Boxplot coming soon");
        } else {
            showSecondaryMessage("Boxplot coming soon");
        }
        return;
    } else {
        if (target === "primary") {
            showChartMessage("Unsupported chart type");
        } else {
            showSecondaryMessage("Unsupported chart type");
        }
        return;
    }

    if (target === "primary") {
        primaryChartInstance = chart;
    } else {
        secondaryChartInstance = chart;
    }
}

function isDiscreteNumeric(viz) {
    if (viz.type !== "histogram") return false;

    const uniqueBins = viz.bins.length;
    const nonZeroCounts = viz.counts.filter(c => c > 0).length;

    // If very few bins actually have data → discrete
    return nonZeroCounts <= 10;
}

function renderPrimaryChart(colData) {
    console.log(colData.visualizations);

    const ctx = document.getElementById("primaryChart").getContext("2d");

    if (primaryChartInstance) {
        primaryChartInstance.destroy();
        primaryChartInstance = null;
    }

    const viz = colData.visualizations?.primary;

    if (!viz) {
        showChartMessage("No data available");
        return;
    }

    renderChartByType(ctx, viz, "primary");
}

function renderSecondaryChart(colData) {

    const ctx = document.getElementById("secondaryChart").getContext("2d");

    if (secondaryChartInstance) {
        secondaryChartInstance.destroy();
        secondaryChartInstance = null;
    }

    const viz = colData.visualizations?.secondary;

    if (!viz) {
        showSecondaryMessage("No secondary chart available");
        return;
    }

    renderChartByType(ctx, viz, "secondary");
}

function renderHistogram(ctx, values) {

    if (!values || values.length === 0) return;

    const bins = 10;

    const min = Math.min(...values);
    const max = Math.max(...values);

    const binWidth = (max - min) / bins || 1;

    const counts = new Array(bins).fill(0);

    values.forEach(v => {
        let index = Math.floor((v - min) / binWidth);

       
        if (index >= bins) index = bins - 1;

        counts[index]++;
    });

    const labels = viz.bins.slice(0, -1).map((b, i) => {
        const start = viz.bins[i];
        const end = viz.bins[i + 1];

        return `${Math.round(start)}–${Math.round(end)}`;
    });

    primaryChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                data: counts
            }]
        },
        options: {
            plugins: { legend: { display: false } }
        }
    });
}

function isCategoricalNumeric(values) {
    const unique = [...new Set(values)];
    return unique.length <= 10; // threshold
}

function renderBarChart(ctx, topValues) {

    const labels = Object.keys(topValues);
    const data = Object.values(topValues);

    primaryChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Count",
                data: data
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function getTopCategories(values, topN = 10) {

    const counts = {};

    values.forEach(v => {
        counts[v] = (counts[v] || 0) + 1;
    });

    // Convert to array and sort
    const sorted = Object.entries(counts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, topN);

    return Object.fromEntries(sorted);
}

function showChartMessage(message) {

    if (primaryChartInstance) {
        primaryChartInstance.destroy();
        primaryChartInstance = null;
    }

    const ctx = document.getElementById("primaryChart").getContext("2d");

    primaryChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [],
            datasets: []
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: message
                }
            }
        }
    });
}

function showSecondaryMessage(message) {
    const msg = document.getElementById("secondaryMessage");

    msg.textContent = message;
    msg.classList.remove("hidden");

    // hide canvas
    document.getElementById("secondaryChart").style.display = "none";
}

function renderCustomLegend(labels, data, colors) {

    const container = document.getElementById("customLegend");
    container.innerHTML = "";

    labels.forEach((label, i) => {
        const item = document.createElement("div");
        item.style.display = "flex";
        item.style.alignItems = "center";
        item.style.gap = "10px";

        const box = document.createElement("div");
        box.style.width = "14px";
        box.style.height = "14px";
        box.style.backgroundColor = colors[i];
        box.style.borderRadius = "3px";

        const text = document.createElement("span");
        text.textContent = label;
        text.style.color = "#ccc";
        text.style.fontSize = "13px";

        item.appendChild(box);
        item.appendChild(text);
        container.appendChild(item);
    });
}