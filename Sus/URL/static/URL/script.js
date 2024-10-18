// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
    const urlForm = document.getElementById('urlForm');
    const outputBox = document.getElementById('outputBox');

    // Handle form submission
    urlForm.addEventListener('submit', function(event) {
        // Show a loading message while waiting for the server to respond
        outputBox.innerHTML = 'Checking... Please wait.';
    });
});
