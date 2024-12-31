from django.shortcuts import render, redirect
from .ml_model import predict_url
from django.utils.timezone import now

def index(request):
    """Renders the index page."""
    timestamp = now().timestamp()  # Get a unique timestamp
    return render(request, 'URL/index.html', {'timestamp': timestamp, 'result': None})

def check_url(request):
    """Handles URL checking and displays the result."""
    result = None
    if request.method == "POST":
        url = request.POST.get('url', '').strip()
        if url:
            result = predict_url(url)  # Call your prediction function
        else:
            result = "Invalid URL. Please try again."

    return render(request, 'URL/index.html', {'result': result})
