from django.shortcuts import render, redirect
from .ml_model import predict_url
from django.utils.timezone import now
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['phishing_database']
feedback_collection = db['feedback']

def index(request):
    """Renders the index page."""
    timestamp = now().timestamp()  # Get a unique timestamp
    return render(request, 'URL/index.html', {'timestamp': timestamp, 'result': None})

def check_url(request):
    """Handles URL checking and displays the result."""
    result = None
    url = None
    if request.method == "POST":
        url = request.POST.get('url', '').strip()
        if url:
            result = predict_url(url)  # Call your prediction function
        else:
            result = "Invalid URL. Please try again."

    return render(request, 'URL/index.html', {'result': result, 'url': url})

def feedback(request):
    """Handles user feedback and stores it in MongoDB."""
    if request.method == "POST":
        url = request.POST.get('url')
        result = request.POST.get('result')
        feedback = request.POST.get('feedback')
        feedback_data = {
            'url': url,
            'result': result,
            'feedback': feedback,
            'timestamp': now()
        }
        feedback_collection.insert_one(feedback_data)
    return redirect('/')
