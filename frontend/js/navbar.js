/**
 * This file contains the JavaScript code and logic for proper
 * functioning of the Navigation Bar. It includes functions 
 * which helps switching pages in a smooth and efficient manner.
*/


// Implementing page switching
const pages = {
    dashboard: document.getElementById("dashboard-page"),
    overview: document.getElementById("overview-page"),
    about: document.getElementById("about-page"),
    contact: document.getElementById("contact-page")
};

function showPage(pageName) {
    Object.values(pages).forEach(p => p.classList.add("hidden"));
    pages[pageName].classList.remove("hidden");
    window.scrollTo(0, 0);
}

const navItems = document.querySelectorAll(".nav-item");

navItems.forEach(item => {
    item.addEventListener("click", () => {

        navItems.forEach(i => i.classList.remove("active"));

        item.classList.add("active");

        const page = item.getAttribute("data-page");
        showPage(page);
        moveSlider(item);
        localStorage.setItem("activePage", page);
    });
});

// Implementing a slide animation for UX
const slider = document.querySelector(".nav-slider");

function moveSlider(element) {
    const rect = element.getBoundingClientRect();
    const parentRect = element.parentElement.getBoundingClientRect();

    slider.style.width = rect.width + "px";
    slider.style.height = rect.height + "px";
    slider.style.left = (rect.left - parentRect.left) + "px";
    slider.style.top = (rect.top - parentRect.top) + "px";
}

// Saving the last page user was on to load same page upon a reload
window.addEventListener("DOMContentLoaded", () => {
    const savedPage = localStorage.getItem("activePage") || "dashboard";

    showPage(savedPage);

    document.querySelectorAll(".nav-item").forEach(item => {
        item.classList.remove("active");

        if (item.getAttribute("data-page") === savedPage) {
            item.classList.add("active");
        }
    });

    const activeItem = document.querySelector(`.nav-item[data-page="${savedPage}"]`);
    if (activeItem) moveSlider(activeItem); 
    initializeDashboard();
});
