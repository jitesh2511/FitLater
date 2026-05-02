/**
 * This file provides the main JavaScript logic for the FitLater dashboard UI.
 * It manages global state for uploaded files, UI state transitions for various dashboard panels,
 * and DOM references for interactive elements. The code also includes utilities for
 * handling state switching, updating the dashboard view, and integrating API responses.
 */



// ==============================
// Global State Management
// ==============================

// Stores uploaded files and their corresponding API responses
const filesStore = [];

// Tracks currently active file index
let activeFileIndex = null;

// Prevent multiple concurrent uploads
let isUploading = false;

// API
const API_BASE = "http://127.0.0.1:8000";


// ==============================
// State Handling Utilities
// ==============================

/**
 * Switches UI state inside a panel
 */
function setState(panel, newState) {
    const states = panel.querySelectorAll(".state");

    states.forEach(s => s.classList.add("hidden"));

    panel.querySelector(`.state-${newState}`).classList.remove("hidden");
}

// ==============================
// DOM Element References
// ==============================

const uploadBox = document.querySelector('.upload-box');
const advisoryBox = document.querySelector('.advise-box');
const cards = document.querySelectorAll('.card');

// ==============================
// Dashboard State Management
// ==============================

/**
 * Updates overall dashboard state
 * Controls upload box, advisory panel and diagnostic cards
 */
function setDashboardState(state) {

    setState(uploadBox, state);

    // Advisory and diagnostic cards always remain in result state
    setState(advisoryBox, "result");
    cards.forEach(card => setState(card, "result"));
}

/**
 * Initializes dashboard with default values
 */
function initializeDashboard() {

    setState(advisoryBox, "result");
    cards.forEach(card => setState(card, "result"));

    const defaultData = {
        diagnostics: {
            missing: { percentage: 0, columns: 0 },
            outliers: { percentage: 0, columns: 0 },
            distribution: { max_skew: 0 },
            duplicates: { percentage: 0}
        },
        advisory: {
            high: [],
            medium: [],
            low: []
        }
    };

    updateUI(defaultData);
}

// ==============================
// File Upload Logic
// ==============================

/**
 * Handles file upload and API interaction
 */
async function handleFileUpload(file) {

    // Prevent multiple concurrent uploads
    if (isUploading) {
        console.warn("Upload already in progress, ignoring new upload");
        return;
    }
    isUploading = true;

    // Step 1: Set loading state
    setDashboardState("loading");

    try {
        // Step 2: Prepare form data
        const formData = new FormData();
        formData.append("file", file);

        // Step 3: Send request to backend
        const response = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData
        });

        // Check if response is successful
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server returned error:", errorData);
            showError(errorData.detail || "Upload failed");
        }

        const data = await response.json();

        // Validate response structure
        if (!data || !data.diagnostics || !data.advisory || !data.descriptive || !data.col_diagnostics || !data.meta) {
            console.error("Invalid response structure:", data);
            showError("Invalid API response");
        }


        // Enforce max file limit
        if (filesStore.length >= 4) {
            showError("Maximum 4 files allowed");
            setState(uploadBox, "result");
            isUploading = false;
            return;
        }

        // Store file and response
        filesStore.push({
            file: file,
            data: data
        });

        activeFileIndex = filesStore.length - 1;

        initializeAnalyticsSelectors();

        // Switch to result state
        setState(uploadBox, "result");

        // Render UI
        renderFileCards();
        updateUI(data);
        

    } catch (error) {
        console.error("Upload Error:", error);

        showError(error.message || "Upload failed");
    } finally {
        // Always reset the uploading flag
        isUploading = false;
    }

}

// ==============================
// Advisory Rendering
// ==============================

/**
 * Updates advisory panel based on API data
 */
function updateAdvisory(data) {

    function renderList(section, items) {
        const container = document.querySelector(section + " .list");
        const header = document.querySelector(section + " .head");

        container.innerHTML = "";

        const total = items.length;
        const visible = items.slice(0, 5);

        const base = header.dataset.label || header.textContent.split("(")[0].trim();
        header.dataset.label = base;
        header.textContent = `${base} (showing ${visible.length} out of ${total})`;
        
         // No issues case
        if (total === 0) {
            const card = document.createElement("div");

            card.classList.add("advise-card", "no-issue");

            if (section.includes("high")) card.classList.add("high");
            if (section.includes("medium")) card.classList.add("medium");
            if (section.includes("low")) card.classList.add("low");

            card.innerHTML = `
                <p class="rec">✔ No issues detected</p>
                <p class="reason">This category looks good. No action needed.</p>
            `;

            container.appendChild(card);
            return;
        }

        // Render advisory items
        visible.forEach(item => {
            const card = document.createElement("div");

            card.classList.add("advise-card");

            if (section.includes("high")) card.classList.add("high");
            if (section.includes("medium")) card.classList.add("medium");
            if (section.includes("low")) card.classList.add("low");

            card.innerHTML = `
                <p class="rec">• <b>${item.column}</b>: ${item.recommendation}</p>
                <p class="reason">${item.reason}</p>
           
            `;

            container.appendChild(card);
        });
    }

    renderList(".advise.high", data.advisory.high);
    renderList(".advise.medium", data.advisory.medium);
    renderList(".advise.low", data.advisory.low);
}

// ==============================
// Utility Functions
// ==============================

function getSmoothColor(value, min = 0, max = 100) {
    // Normalize value between 0 and 1
    let ratio = (value - min) / (max - min);
    ratio = Math.max(0, Math.min(1, ratio));

    // Gradient: Green → Yellow → Red
    let r, g, b = 0;

    if (ratio < 0.5) {
        // Green → Yellow
        r = Math.round(255 * (ratio * 2));
        g = 200;
    } else {
        // Yellow → Red
        r = 255;
        g = Math.round(200 * (1 - (ratio - 0.5) * 2));
    }

    return `rgb(${r}, ${g}, ${b})`;
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function showError(message) {
    console.error("UI Error:", message);

    const errorMsg = uploadBox.querySelector(".state-error .error-msg");

    if (!errorMsg) {
        console.warn("Error element not found");
        return;
    }

    errorMsg.textContent = message;

    // 🔥 IMPORTANT: switch to error state
    setState(uploadBox, "error");
}

// ==============================
// UI Update Logic
// ==============================

function updateUI(data) {

    // Missing
    const missingValue = data?.diagnostics?.missing?.percentage ?? 0;
    const missingEl = document.querySelector(".missing .state-result .card-value");
    const missingText = document.querySelector(".missing .state-result .card-sub");
    missingEl.textContent = missingValue + "%";
    missingEl.style.color = getSmoothColor(missingValue);
    missingText.textContent = data.diagnostics.missing.columns + " columns affected";
    missingText.style.color = missingEl.style.color;

    // Skew
    const skewValue = data?.diagnostics?.distribution?.max_skew ?? 0.0;
    const skewEl = document.querySelector(".distribution .state-result .card-value");
    const skewText = document.querySelector(".distribution .state-result .card-sub");
    skewEl.textContent = skewValue;
    skewEl.style.color = getSmoothColor(skewValue, 0, 2.5);
    skewText.style.color = skewEl.style.color;

    // Outliers
    const outlierValue = data?.diagnostics?.outliers?.percentage ?? 0;
    const outlierEl = document.querySelector(".outliers .state-result .card-value");
    const outlierText = document.querySelector(".outliers .state-result .card-sub");
    outlierEl.textContent = outlierValue + "%";
    outlierEl.style.color = getSmoothColor(outlierValue);
    outlierText.textContent = data.diagnostics.outliers.columns + " columns affected";
    outlierText.style.color = outlierEl.style.color;

    // Duplicates
    const duplicatesValue = data?.diagnostics?.duplicates?.percentage ?? 0;
    const duplicatesEl = document.querySelector(".duplicates .state-result .card-value");
    const duplicatesText = document.querySelector(".duplicates .state-result .card-sub");
    duplicatesEl.textContent = duplicatesValue + "%";
    duplicatesEl.style.color = getSmoothColor(duplicatesValue);
    duplicatesText.textContent = "Duplicate values detected";
    duplicatesText.style.color = duplicatesEl.style.color


    // Advisory
    updateAdvisory(data);
    // Report Page
    if (typeof renderReport === "function") {
        renderReport(data);
    }
}

// ==============================
// File Input & Drag-Drop Events
// ==============================

const fileInput = document.getElementById('fileInput');
const uploadTrigger = document.getElementById('uploadTrigger');

uploadTrigger.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    // Prevent multiple uploads
    if (isUploading) {
        console.warn("Upload already in progress, ignoring change event");
        return;
    }
    
    const file = fileInput.files[0];

    handleFileUpload(file);
    
    // Clear the input value so the same file can be selected again
    fileInput.value = '';
});

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();

    // Prevent multiple uploads
    if (isUploading) {
        console.warn("Upload already in progress, ignoring drop event");
        return;
    }

    const file = e.dataTransfer.files[0];

    handleFileUpload(file);
    
    // Clear the file input value
    fileInput.value = '';
});

document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});

// ==============================
// File Cards Rendering
// ==============================

function renderFileCards(){

    const container = document.querySelector(".file-list");
    container.innerHTML = "";

    filesStore.forEach((item, index) => {

        const isActive = index === activeFileIndex;

        const card = document.createElement("div");
        card.classList.add("file-card");
        if (isActive) card.classList.add("active");

        card.innerHTML = `
            <div class="file-info">
                <span class="file-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-chart-column-increasing-icon lucide-file-chart-column-increasing"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M8 18v-2"/><path d="M12 18v-4"/><path d="M16 18v-6"/></svg></span>
                <div class="file-meta">
                    <span class="file-name">${item.file.name}</span>
                    <span class="file-size">
                        ${formatFileSize(item.file.size)} • 
                        ${item.data.meta.rows} × ${item.data.meta.columns}
                    </span>
                </div>
            </div>
            <button class="remove-file" data-index="${index}">✖</button>
        `;

        card.addEventListener("click", () => {
            activeFileIndex = index;
            renderFileCards();
            updateUI(item.data);
        });

        container.appendChild(card);
    });

    const uploadMoreBtn = document.getElementById("uploadMoreBtn");

    if (!uploadMoreBtn) return;

    uploadMoreBtn.onclick = () => fileInput.click();

    uploadMoreBtn.style.display = filesStore.length >= 4 ? "none" : "block";
}

// ==============================
// File Removal Logic
// ==============================

document.addEventListener("click", (e) => {

    const btn = e.target.closest(".remove-file");
    if (btn) {
        
        e.stopPropagation();

        const index = Number(btn.dataset.index);

        filesStore.splice(index, 1);

        if (filesStore.length === 0) {
            activeFileIndex = null;
            setState(uploadBox, "empty");
            initializeDashboard();
            return;
        }

        activeFileIndex = Math.max(0, index - 1);

        setState(uploadBox, "result");
        renderFileCards();
        updateUI(filesStore[activeFileIndex].data);
    }
});

// ==============================
// Settings Handlers
// ==============================

document.getElementById("resetDataBtn")?.addEventListener("click", () => {
    filesStore.length = 0;
    activeFileIndex = null;

    setState(uploadBox, "empty");
    initializeDashboard();

    alert("All data reset");
});