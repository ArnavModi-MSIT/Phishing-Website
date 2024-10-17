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
with open(r'C:\Coding\Phishing\1\xgboost_phishing_model.pkl', 'rb') as model_file:
    model = dill.load(model_file)

with open(r'C:\Coding\Phishing\1\vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = dill.load(vectorizer_file)

# Function to preprocess and predict URL
def predict_url(url):
    # Preprocess URL
    url = url.lower().strip().rstrip('/')
    url = re.sub(r'[^a-zA-Z0-9/:.?=&_-]', '', url)

    # Tokenize and vectorize the URL
    X_url_new = vectorizer.transform([url])
    url_length = len(url)
    num_dots = url.count('.')
    X_additional_new = sp.csr_matrix([[url_length, num_dots]])

    # Combine URL features with additional features
    X_combined_new = sp.hstack([X_url_new, X_additional_new])

    # Make predictions
    prediction = model.predict(X_combined_new)

    return 'Bad' if prediction[0] == 1 else 'Good'
