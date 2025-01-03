import pandas as pd
import re
import os
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
import dill
import scipy.sparse as sp
import xgboost as xgb

# Define the preprocessing and feature extraction functions
def preprocess_url(url):
    url = url.lower().strip().rstrip('/')
    url = re.sub(r'[^a-zA-Z0-9/:.?=&_-]', '', url)
    return url

def extract_features(url):
    domain = urlparse(url).netloc
    path = urlparse(url).path
    query = urlparse(url).query
    url_length = len(url)
    num_dots = url.count('.')
    return url, domain, path, query, url_length, num_dots

def custom_tokenizer(url):
    return url.split('/')

# Load the saved model and vectorizer
with open('xgboost_phishing_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Get user input for URLs
user_input = input("Enter URLs (separate with commas): ")
new_urls = [url.strip() for url in user_input.split(',')]

# Preprocess and extract features for new URLs
data = {
    'URL': [preprocess_url(url) for url in new_urls]
}
df_new = pd.DataFrame(data)

# Tokenize and vectorize new URLs
X_url_new = vectorizer.transform(df_new['URL'])

# Add additional features
df_new['url_length'] = df_new['URL'].apply(len)
df_new['num_dots'] = df_new['URL'].apply(lambda x: x.count('.'))
X_additional_new = df_new[['url_length', 'num_dots']].values

# Combine URL features with additional features
X_combined_new = sp.hstack([X_url_new, X_additional_new])

# Make predictions
y_pred = model.predict(X_combined_new)

# Display results
for url, prediction in zip(new_urls, y_pred):
    result = 'Bad' if prediction == 1 else 'Good'
    print(f'URL: {url}, Prediction: {result}')
