let primaryChartInstance = null;
let secondaryChartInstance = null;
Chart.register(ChartDataLabels);
Chart.defaults.plugins.datalabels = false;

const CHART_COLORS = {
    primary: "#4C9AFF",
    primaryFill: "rgba(76, 154, 255, 0.28)",
    accent: "#FF6384",
    accentSoft: "rgba(255, 99, 132, 0.22)",
    text: "#cfd8e3",
    mutedText: "#9fb0c8",
    grid: "rgba(255, 255, 255, 0.08)",
    panelStroke: "rgba(255, 255, 255, 0.14)"
};

function getCommonTitleOptions(viz) {
    if (!viz.meta) return { display: false };
    return {
        display: true,
        text: viz.meta,
        color: CHART_COLORS.text,
        padding: {
            top: 6,
            bottom: 14
        },
        font: {
            size: 13,
            weight: "500"
        }
    };
}

function getCommonCartesianOptions(viz) {
    return {
        responsive: true,
        maintainAspectRatio: true,
        layout: {
            padding: 8
        },
        plugins: {
            datalabels: false,
            legend: { display: false },
            title: getCommonTitleOptions(viz)
        },
        scales: {
            x: {
                ticks: { color: CHART_COLORS.mutedText, maxRotation: 0 },
                grid: { color: CHART_COLORS.grid, drawBorder: false },
                border: { color: CHART_COLORS.panelStroke }
            },
            y: {
                ticks: { color: CHART_COLORS.mutedText },
                grid: { color: CHART_COLORS.grid, drawBorder: false },
                border: { color: CHART_COLORS.panelStroke }
            }
        }
    };
}

function hidePrimaryXAxisLabels(options, target) {
    if (target !== "primary") return options;

    return {
        ...options,
        scales: {
            ...options.scales,
            x: {
                ...options.scales?.x,
                ticks: {
                    ...options.scales?.x?.ticks,
                    display: false
                }
            }
        }
    };
}

function getChartDensitySettings(itemCount) {
    const isLowDensity = itemCount > 0 && itemCount <= 14;
    return {
        isLowDensity,
        showXAxisLabels: isLowDensity
    };
}

function getLinearTrend(values) {
    const n = values.length;
    if (n < 2) return values.slice();

    let sumX = 0;
    let sumY = 0;
    let sumXY = 0;
    let sumXX = 0;

    for (let i = 0; i < n; i++) {
        const x = i;
        const y = Number(values[i]) || 0;
        sumX += x;
        sumY += y;
        sumXY += x * y;
        sumXX += x * x;
    }

    const denominator = (n * sumXX) - (sumX * sumX);
    const slope = denominator === 0 ? 0 : ((n * sumXY) - (sumX * sumY)) / denominator;
    const intercept = (sumY - (slope * sumX)) / n;

    return values.map((_, i) => (slope * i) + intercept);
}

function getAdaptiveBarDataLabels(itemCount) {
    return { display: false };
}

function formatTwoDecimals(value) {
    const num = Number(value);
    if (!Number.isFinite(num)) return value;
    return num.toFixed(2);
}

function normalizeChartOptionsForTarget(options, target, vizType) {
    if (target === "secondary" && vizType !== "pie") {
        return {
            ...options,
            maintainAspectRatio: false
        };
    }
    return options;
}

function hasNativeBoxplotSupport() {
    try {
        if (!Chart || !Chart.registry || !Chart.registry.controllers) return false;
        return Boolean(Chart.registry.controllers.get("boxplot"));
    } catch (error) {
        return false;
    }
}

function renderBoxplotFallback(ctx, viz, target = "secondary") {
    const min = Number(viz.min);
    const q1 = Number(viz.q1);
    const median = Number(viz.median);
    const q3 = Number(viz.q3);
    const max = Number(viz.max);

    const fallbackPlugin = {
        id: "manualBoxplot",
        afterDatasetsDraw(chart) {
            const { ctx: drawCtx, scales } = chart;
            const xScale = scales.x;
            const yScale = scales.y;

            if (!xScale || !yScale) return;

            const centerX = xScale.getPixelForValue(0);
            const yMin = yScale.getPixelForValue(min);
            const yQ1 = yScale.getPixelForValue(q1);
            const yMedian = yScale.getPixelForValue(median);
            const yQ3 = yScale.getPixelForValue(q3);
            const yMax = yScale.getPixelForValue(max);

            const boxWidth = 58;
            const capWidth = 26;

            drawCtx.save();

            drawCtx.strokeStyle = "#4C9AFF";
            drawCtx.lineWidth = 2;

            drawCtx.beginPath();
            drawCtx.moveTo(centerX, yMin);
            drawCtx.lineTo(centerX, yMax);
            drawCtx.stroke();

            drawCtx.beginPath();
            drawCtx.moveTo(centerX - capWidth / 2, yMin);
            drawCtx.lineTo(centerX + capWidth / 2, yMin);
            drawCtx.moveTo(centerX - capWidth / 2, yMax);
            drawCtx.lineTo(centerX + capWidth / 2, yMax);
            drawCtx.stroke();

            drawCtx.fillStyle = "rgba(76, 154, 255, 0.22)";
            drawCtx.strokeStyle = "#4C9AFF";
            drawCtx.fillRect(centerX - boxWidth / 2, yQ3, boxWidth, yQ1 - yQ3);
            drawCtx.strokeRect(centerX - boxWidth / 2, yQ3, boxWidth, yQ1 - yQ3);

            drawCtx.strokeStyle = "#FF6384";
            drawCtx.lineWidth = 2.5;
            drawCtx.beginPath();
            drawCtx.moveTo(centerX - boxWidth / 2, yMedian);
            drawCtx.lineTo(centerX + boxWidth / 2, yMedian);
            drawCtx.stroke();

            drawCtx.restore();
        }
    };

    const fallbackOptions = normalizeChartOptionsForTarget({
        plugins: {
            datalabels: false,
            legend: { display: false },
            title: viz.meta
                ? { display: true, text: viz.meta }
                : { display: false }
        },
        scales: {
            x: {
                ticks: { color: CHART_COLORS.text },
                grid: { display: false }
            },
            y: {
                beginAtZero: false,
                min: min,
                max: max,
                ticks: {
                    color: CHART_COLORS.text,
                    callback(value) {
                        return formatTwoDecimals(value);
                    }
                },
                grid: { color: CHART_COLORS.grid }
            }
        }
    }, target, "boxplot");

    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Distribution"],
            datasets: [{
                data: [0],
                backgroundColor: "rgba(0,0,0,0)",
                borderWidth: 0
            }]
        },
        options: fallbackOptions,
        plugins: [fallbackPlugin]
    });
}

function renderChartByType(ctx, viz, target) {

    const legendContainer = document.getElementById("customLegend");
    const chartWrapper = document.querySelector(".chart-wrapper");
    if (legendContainer) {
        legendContainer.innerHTML = "";
        legendContainer.style.display = viz.type === "pie" ? "flex" : "none";
    }
    if (chartWrapper && target === "secondary") {
        chartWrapper.classList.toggle("secondary-pie-layout", viz.type === "pie");
        chartWrapper.classList.toggle("secondary-single-layout", viz.type !== "pie");
    }
    const msg = document.getElementById("secondaryMessage");
    if (msg && target === "secondary") {
        msg.classList.add("hidden");
    }

    const secondaryCanvas = document.getElementById("secondaryChart");
    if (secondaryCanvas && target === "secondary") {
        secondaryCanvas.style.display = "block";
    }

    let instanceRef = target === "primary"
        ? "primaryChartInstance"
        : "secondaryChartInstance";

    let chart;

    if (viz.type === "histogram") {
        const bins = Array.isArray(viz.bins) ? viz.bins : [];
        const counts = Array.isArray(viz.counts) ? viz.counts : [];
        const bucketCount = Math.min(Math.max(bins.length - 1, 0), counts.length);
        const density = getChartDensitySettings(bucketCount);
        const labels = Array.from({ length: bucketCount }, (_, i) => {
            if (!density.showXAxisLabels) return `${i + 1}`;

            const start = bins[i];
            const end = bins[i + 1];
            if (typeof start === "number" && typeof end === "number") {
                return `${start.toFixed(2)}-${end.toFixed(2)}`;
            }
            return `Bucket ${i + 1}`;
        });
        const borderRadius = bucketCount > 40 ? 2 : bucketCount > 20 ? 4 : 8;
        const dataLabelOptions = getAdaptiveBarDataLabels(bucketCount);

        let histogramOptions = {
            ...getCommonCartesianOptions(viz),
            aspectRatio: 2.35,
            scales: {
                ...getCommonCartesianOptions(viz).scales,
                x: {
                    ...getCommonCartesianOptions(viz).scales.x,
                    ticks: {
                        ...getCommonCartesianOptions(viz).scales.x.ticks,
                        display: density.showXAxisLabels,
                        autoSkip: !density.showXAxisLabels,
                        maxTicksLimit: density.showXAxisLabels ? 14 : 10
                    },
                    grid: { display: false }
                }
            },
            plugins: {
                ...getCommonCartesianOptions(viz).plugins,
                datalabels: dataLabelOptions,
                tooltip: {
                    callbacks: {
                        title(items) {
                            const idx = items?.[0]?.dataIndex ?? 0;
                            const start = bins[idx];
                            const end = bins[idx + 1];
                            if (typeof start === "number" && typeof end === "number") {
                                return `Range: ${start.toFixed(3)} to ${end.toFixed(3)}`;
                            }
                            return `Bucket ${idx + 1}`;
                        },
                        label(context) {
                            return `Count: ${context.raw}`;
                        }
                    }
                }
            }
        };

        histogramOptions = normalizeChartOptionsForTarget(histogramOptions, target, "histogram");

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    data: counts.slice(0, bucketCount),
                    backgroundColor: CHART_COLORS.primaryFill,
                    borderColor: CHART_COLORS.primary,
                    borderWidth: 1.1,
                    borderRadius,
                    borderSkipped: false,
                    barPercentage: 1.0,
                    categoryPercentage: 1.0,
                    maxBarThickness: 24,
                    datalabels: dataLabelOptions
                }]
            },
            options: histogramOptions
        });
    } else if (viz.type === "bar") {

        const labels = Array.isArray(viz.labels)
            ? viz.labels
            : Object.keys(viz.data || {});
        const data = Array.isArray(viz.values)
            ? viz.values
            : Object.values(viz.data || {});

        const categoryCount = labels.length;
        const density = getChartDensitySettings(categoryCount);
        const xTickStep = categoryCount > 30 ? Math.ceil(categoryCount / 10) : 1;

        const trendValues = target === "secondary" ? getLinearTrend(data) : [];
        const yMaxBase = Math.max(...data, ...(trendValues.length ? trendValues : [0]), 0);
        const ySuggestedMax = target === "secondary" ? yMaxBase * 1.15 : undefined;

        let barOptions = {
            ...getCommonCartesianOptions(viz),
            plugins: {
                ...getCommonCartesianOptions(viz).plugins,
                datalabels: getAdaptiveBarDataLabels(categoryCount)
            },
            scales: {
                ...getCommonCartesianOptions(viz).scales,
                x: {
                    ...getCommonCartesianOptions(viz).scales.x,
                    ticks: {
                        ...getCommonCartesianOptions(viz).scales.x.ticks,
                        display: density.showXAxisLabels,
                        autoSkip: !density.showXAxisLabels || categoryCount > 16,
                        maxTicksLimit: density.showXAxisLabels ? 14 : 10,
                        callback(value, index) {
                            if (!density.showXAxisLabels) return "";
                            if (xTickStep > 1 && (index % xTickStep !== 0)) return "";
                            return this.getLabelForValue(value);
                        }
                    }
                },
                y: {
                    ...getCommonCartesianOptions(viz).scales.y,
                    suggestedMax: ySuggestedMax
                }
            }
        };

        const datasets = [{
            data: data,
            backgroundColor: CHART_COLORS.primaryFill,
            borderColor: CHART_COLORS.primary,
            borderWidth: 1.5,
            borderRadius: 8,
            borderSkipped: false
        }];

        if (target === "secondary" && trendValues.length) {
            datasets.push({
                type: "line",
                label: "Trend",
                data: trendValues,
                borderColor: CHART_COLORS.accent,
                borderWidth: 2.2,
                pointRadius: 0,
                pointHoverRadius: 0,
                tension: 0.25,
                fill: false,
                datalabels: { display: false }
            });
        }

        barOptions = normalizeChartOptionsForTarget(barOptions, target, "bar");

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets
            },
            options: barOptions
        });

    } else if (viz.type === "pie") {

        const labels = Object.keys(viz.data || {});
        const data = Object.values(viz.data || {});

        const colors = [
            "#63A8FF",
            "#8D7CFF",
            "#42D6C6",
            "#FF9D66",
            "#FF6E9F",
            "#8BD450",
            "#FFCC66"
        ];

        chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    borderWidth: 2.5,
                    borderColor: "#10131a",
                    hoverOffset: 12,
                    spacing: 2,
                    backgroundColor: colors.slice(0, data.length),

                    datalabels: {
                        color: "#fff",
                        font: {
                            weight: "600",
                            size: 11
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
                    padding: 12
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
                        ? getCommonTitleOptions(viz)
                        : { display: false }
                }
            }
        });
        renderCustomLegend(labels, data, colors);
    } else if (viz.type === "line") {

        const pointCount = Array.isArray(viz.values) ? viz.values.length : 0;
        const showPoints = pointCount <= 80;

        let lineOptions = {
            ...getCommonCartesianOptions(viz),
            scales: {
                ...getCommonCartesianOptions(viz).scales,
                x: {
                    ...getCommonCartesianOptions(viz).scales.x,
                    ticks: {
                        ...getCommonCartesianOptions(viz).scales.x.ticks,
                        autoSkip: true,
                        maxTicksLimit: 10
                    }
                }
            }
        };
        lineOptions = hidePrimaryXAxisLabels(lineOptions, target);

        lineOptions = normalizeChartOptionsForTarget(lineOptions, target, "line");

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: viz.labels,
                datasets: [{
                    data: viz.values,
                    fill: true,
                    backgroundColor: "rgba(76, 154, 255, 0.15)",
                    borderColor: CHART_COLORS.primary,
                    pointBackgroundColor: CHART_COLORS.primary,
                    pointBorderColor: "#10131a",
                    pointBorderWidth: showPoints ? 1.5 : 0,
                    pointHoverRadius: showPoints ? 5 : 0,
                    pointRadius: showPoints ? 3 : 0,
                    borderWidth: 2.5,
                    tension: 0.25
                }]
            },
            options: lineOptions
        });

    } else if (viz.type === "boxplot") {

        const d = viz;
        const supportsBoxplot = hasNativeBoxplotSupport();

        if (supportsBoxplot) {
            let boxplotOptions = {
                ...getCommonCartesianOptions(viz),
                plugins: {
                    ...getCommonCartesianOptions(viz).plugins,
                    tooltip: {
                        callbacks: {
                            title() {
                                return "Distribution Summary";
                            },
                            label() {
                                const iqr = Number(d.q3) - Number(d.q1);
                                return [
                                    `Min: ${formatTwoDecimals(d.min)}`,
                                    `Q1: ${formatTwoDecimals(d.q1)}`,
                                    `Median: ${formatTwoDecimals(d.median)}`,
                                    `Q3: ${formatTwoDecimals(d.q3)}`,
                                    `Max: ${formatTwoDecimals(d.max)}`,
                                    `IQR: ${formatTwoDecimals(iqr)}`
                                ];
                            }
                        }
                    }
                }
            };
            boxplotOptions = normalizeChartOptionsForTarget(boxplotOptions, target, "boxplot");

            chart = new Chart(ctx, {
                type: "boxplot",
                data: {
                    labels: ["Distribution"],
                    datasets: [{
                        label: viz.meta || "Boxplot",
                        data: [[d.min, d.q1, d.median, d.q3, d.max]],
                        backgroundColor: "rgba(76, 154, 255, 0.22)",
                        borderColor: CHART_COLORS.primary,
                        medianColor: CHART_COLORS.accent,
                        itemRadius: 8,
                        outlierRadius: 3,
                        lowerBackgroundColor: CHART_COLORS.primaryFill,
                        upperBackgroundColor: CHART_COLORS.accentSoft
                    }]
                },
                options: boxplotOptions
            });
        } else {
            chart = renderBoxplotFallback(ctx, viz, target);
        }

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

    const ctx = document.getElementById("primaryChart").getContext("2d");

    const existingChart = Chart.getChart(ctx.canvas);

    if (existingChart) {
        existingChart.destroy();
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

    const existingChart = Chart.getChart(ctx.canvas);

    if (existingChart) {
        existingChart.destroy();
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