/**
 * 
 * Provides logic for the collapsible sidebar UI in the FitLater dashboard.
 * - Handles sidebar expand/collapse functionality and persists its state via localStorage
 * - Manages sidebar navigation and page switching for dashboard sub-pages
 * - Controls active state styling for sidebar navigation items
 * 
 * This script ensures consistent sidebar interactions, remembering user preferences
 * across sessions and enabling dynamic UI updates based on selected navigation items.
 */


const toggleBtn = document.getElementById("toggleSidebar");
const sidebar = document.getElementById("sidebar");

// On page load, check localStorage and set sidebar state
window.addEventListener("DOMContentLoaded", () => {
    const collapsed = localStorage.getItem("sidebar-collapsed");

    // If user has a preference → use it
    if (collapsed !== null) {
        if (collapsed === "false") {
            sidebar.classList.remove("collapsed");
        } else {
            sidebar.classList.add("collapsed");
        }
    }

    // If no preference → DO NOTHING (stay collapsed by default)
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
