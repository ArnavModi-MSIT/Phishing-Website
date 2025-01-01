// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
    const urlForm = document.getElementById('urlForm');
    const urlInput = document.getElementById('urlInput');
    const outputBox = document.getElementById('outputBox');

    // Handle form submission
    urlForm.addEventListener('submit', function(event) {
        // Prevent multiple submissions if the input is invalid
        if (!urlInput.checkValidity()) {
            outputBox.innerHTML = '<p style="color: red;">Please enter a valid URL (including http:// or https://).</p>';
            return;
        }

        // Show a loading message while waiting for the server to respond
        outputBox.innerHTML = '<p>🔄 Checking... Please wait.</p>';
    });
});
