from django.shortcuts import render
from .ml_model import predict_url  # Ensure this imports your prediction function

def index(request):
    """Renders the index page."""
    return render(request, 'URL/index.html', {'result': None})  # Initialize result to None

def check_url(request):
    """Handles URL checking and displays the result."""
    result = ""
    if request.method == "POST":
        if 'url' in request.POST:
            url = request.POST.get('url')
            result = predict_url(url)  # Call your prediction function

    return render(request, 'URL/index.html', {'result': result})

def feedback_view(request):
    """Handles feedback from the user."""
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        # Handle the feedback (e.g., save it to a database or log it)
        # For now, you can just print it to the console
        print(f"User feedback: {feedback}")
    
    return render(request, 'URL/index.html', {'result': None})  # Redirect back to the index page
