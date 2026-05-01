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
