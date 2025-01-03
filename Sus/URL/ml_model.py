import pandas as pd
import re
import os
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
import dill
import scipy.sparse as sp
import xgboost as xgb

# Define the custom tokenizer function
def custom_tokenizer(url):
    return url.split('/')

# Get the current directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(current_dir, 'xgboost_phishing_model.json')
vectorizer_path = os.path.join(current_dir, 'vectorizer.pkl')

model = xgb.XGBClassifier()
model.load_model(model_path)

# Load model
with open(model_path, 'rb') as model_file:
    model = dill.load(model_file)

# Load vectorizer
with open(vectorizer_path, 'rb') as vectorizer_file:
    vectorizer = dill.load(vectorizer_file)

# Function to preprocess and predict URL
def predict_url(url):
    """Preprocess the input URL, tokenize it, and predict whether it's phishing or not."""
   
    # Step 1: Preprocess the URL
    url = url.lower().strip().rstrip('/')
    url = re.sub(r'[^a-zA-Z0-9/:.?=&_-]', '', url)  # Remove unwanted characters

    # Step 2: Tokenize and vectorize the URL using the pre-trained vectorizer
    try:
        X_url_new = vectorizer.transform([url])
    except Exception as e:
        print(f"Error during vectorization: {e}")
        return "An error occurred during URL processing."

    # Step 3: Extract additional features (URL length and number of dots)
    url_length = len(url)
    num_dots = url.count('.')
    X_additional_new = sp.csr_matrix([[url_length, num_dots]])

    # Step 4: Combine URL features with additional features
    X_combined_new = sp.hstack([X_url_new, X_additional_new])

    # Step 5: Make predictions using the loaded model
    try:
        prediction = model.predict(X_combined_new)
        result = 'Bad' if prediction[0] == 1 else 'Good'
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "An error occurred during prediction."

    return result