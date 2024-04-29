const downloadLinks = document.querySelectorAll("[data-download]");

downloadLinks.forEach(button => {
    const id = button.dataset.download;
    const content = document.getElementById(id);
    const a = document.createElement("a");

    // Set the href to a valid URL, e.g., to a data URL or a server endpoint
    // Example: a.href = "https://example.com/download";
    a.href = content.src ;

    // Optionally, set a filename for the downloaded file
    // Example: a.download = "myfile.txt";
    a.download = "";

    a.style.display = 'none';

    button.addEventListener("click", () => {
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
});
