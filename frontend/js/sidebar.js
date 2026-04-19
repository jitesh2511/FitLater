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