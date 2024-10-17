// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
    const urlForm = document.getElementById('urlForm');
    const outputBox = document.getElementById('outputBox');
    
    // Handle form submission
    urlForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the URL input value
        const urlInput = document.getElementById('urlInput').value;

        // Show loading message while fetching results
        outputBox.innerHTML = 'Checking... Please wait.';

        // Create a FormData object to send the URL via AJAX
        const formData = new FormData();
        formData.append('url', urlInput);

        // Send the data to the server using Fetch API
        fetch(urlForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
            },
        })
        .then(response => response.json()) // Parse JSON response
        .then(data => {
            // Update the output box with the result
            outputBox.innerHTML = data.result || 'An error occurred. Please try again.';
        })
        .catch(error => {
            console.error('Error:', error);
            outputBox.innerHTML = 'An error occurred. Please try again.';
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Check if this cookie string begins with the name we want
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
