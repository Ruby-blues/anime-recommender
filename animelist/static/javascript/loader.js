// Function to show loader
function showLoader() {
    const loader = document.querySelector(".loader");
    loader.classList.remove("loader--hidden");
}

window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");
    loader.classList.add("loader--hidden");
    loader.addEventListener("transitionend", () => {
        document.body.removeChild(loader);
    });
});

// Show loader beforeunload
window.addEventListener("beforeunload", showLoader);
