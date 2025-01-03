import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
import dill
import scipy.sparse as sp
import xgboost as xgb

# Define the custom tokenizer function
def custom_tokenizer(url):
    return url.split('/')

# Load the saved model and vectorizer
with open(r'C:\Coding\Phishing-Website\Sus\URL\xgboost_phishing_model.pkl', 'rb') as model_file:
    model = dill.load(model_file)

with open(r'C:\Coding\Phishing-Website\Sus\URL\vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = dill.load(vectorizer_file)

# Function to preprocess and predict URL
def predict_url(url):
    """Preprocess the input URL, tokenize it, and predict whether it's phishing or not."""
    
    # Step 1: Preprocess the URL
    url = url.lower().strip().rstrip('/')
    url = re.sub(r'[^a-zA-Z0-9/:.?=&_-]', '', url)  # Remove unwanted characters

    # Step 2: Tokenize and vectorize the URL using the pre-trained vectorizer
    try:
        X_url_new = vectorizer.transform([url])  # Assuming 'vectorizer' is pre-loaded
    except Exception as e:
        print(f"Error during vectorization: {e}")
        return "An error occurred during URL processing."

    # Step 3: Extract additional features (URL length and number of dots)
    url_length = len(url)
    num_dots = url.count('.')
    X_additional_new = sp.csr_matrix([[url_length, num_dots]])  # Create a sparse matrix for the additional features

    # Step 4: Combine URL features with additional features
    X_combined_new = sp.hstack([X_url_new, X_additional_new])  # Stack the tokenized URL features with additional features

    # Step 5: Make predictions using the loaded model
    try:
        prediction = model.predict(X_combined_new)  # Assuming 'model' is pre-loaded
        result = 'Bad' if prediction[0] == 1 else 'Good'
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "An error occurred during prediction."

    return result