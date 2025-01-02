from django.shortcuts import render, redirect
from .ml_model import predict_url
from django.utils.timezone import now
from pymongo import MongoClient
from urllib.parse import urlparse

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['phishing_database']
phishing_urls = db['phishing_urls']

def normalize_url(url):
    """Normalize URL by removing unnecessary parts like 'www'."""
    parsed_url = urlparse(url.lower())
    return parsed_url.netloc + parsed_url.path

def index(request):
    """Renders the index page."""
    timestamp = now().timestamp()
    return render(request, 'URL/index.html', {'timestamp': timestamp, 'result': None})

def check_url(request):
    """Handles URL checking and displays the result."""
    result = None
    url = None
    if request.method == "POST":
        url = request.POST.get('url', '').strip()
        if url:
            # Normalize the URL for consistent checking
            normalized_url = normalize_url(url)

            # Check the database for the URL
            existing_entry = phishing_urls.find_one({'url': normalized_url})
            if existing_entry:
                # Ensure that 'label' field exists in the existing entry
                result = existing_entry.get('label', None)
                if result is None:
                    # If label does not exist, predict it and update the database
                    prediction = predict_url(url)
                    result = "bad" if prediction == "bad" else "good"
                    phishing_urls.update_one(
                        {'url': normalized_url},
                        {'$set': {'label': result}}
                    )
            else:
                # If URL is not found, predict and store it in the database
                prediction = predict_url(url)
                result = "bad" if prediction == "bad" else "good"
                phishing_urls.insert_one({'url': normalized_url, 'label': result})
        else:
            result = "Invalid URL. Please try again."

    return render(request, 'URL/index.html', {'result': result, 'url': url})

def feedback(request):
    """Handles user feedback and stores it in MongoDB."""
    if request.method == "POST":
        url = request.POST.get('url')
        result = request.POST.get('result')
        feedback = request.POST.get('feedback')

        # Normalize the URL for consistent checking
        normalized_url = normalize_url(url)

        # Ensure the URL exists in the collection before updating
        existing_entry = phishing_urls.find_one({'url': normalized_url})

        if existing_entry:
            # Check if feedback already exists for this URL
            if 'feedback' in existing_entry:
                # If feedback already exists, don't save again
                print("Feedback already stored for this URL.")
            else:
                # Apply logic to set the label based on feedback
                if result == "bad" and feedback == "no":
                    label = "good"  # Set label to good if result is bad and feedback is no
                elif result == "bad" and feedback == "yes":
                    label = "bad"
                elif result == "good" and feedback == "no":
                    label = "bad"
                else:  # result == "good" and feedback == "yes"
                    label = "good"

                # Update the record with the new label and feedback field
                phishing_urls.update_one(
                    {'url': normalized_url},
                    {'$set': {'label': label, 'feedback': feedback}}
                )
                print(f"Updated URL {url} with new label: {label} and feedback: {feedback}.")
        else:
            # URL not found in the collection, handle appropriately
            print("URL not found in collection.")
    
    return redirect('/')
