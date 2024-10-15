document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("urlForm");

    form.addEventListener("submit", function(event) {
        event.preventDefault();  // Prevents the form from submitting in the traditional way

        const url = document.getElementById("urlInput").value;
        console.log("URL Entered: ", url);

        // Here you could make an AJAX request or send the URL to the backend for phishing detection.
    });
});
