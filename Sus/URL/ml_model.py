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

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved model and vectorizer using relative paths
model_path = os.path.join(current_dir, 'xgboost_phishing_model.json')
vectorizer_path = os.path.join(current_dir, 'vectorizer.pkl')

try:
    # Load model
    model = xgb.Booster()  # Initialize booster
    model.load_model(model_path)  # Load model
    
    # Load vectorizer
    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = dill.load(vectorizer_file)
except Exception as e:
    print(f"Error loading model or vectorizer: {e}")

def predict_url(url):
    """Preprocess the input URL, tokenize it, and predict whether it's phishing or not."""
    try:
        # Step 1: Preprocess the URL
        url = url.lower().strip().rstrip('/')
        url = re.sub(r'[^a-zA-Z0-9/:.?=&_-]', '', url)

        # Step 2: Tokenize and vectorize the URL
        X_url_new = vectorizer.transform([url])
        
        # Step 3: Extract additional features
        url_length = len(url)
        num_dots = url.count('.')
        X_additional_new = sp.csr_matrix([[url_length, num_dots]])
        
        # Step 4: Combine features
        X_combined_new = sp.hstack([X_url_new, X_additional_new])
        
        # Step 5: Convert to DMatrix and predict
        dtest = xgb.DMatrix(X_combined_new)
        prediction = model.predict(dtest)
        
        # Step 6: Convert prediction to result
        result = 'Bad' if prediction[0] > 0.5 else 'Good'
        return result
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Error processing URL"