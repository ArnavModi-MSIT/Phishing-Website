import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import pickle
import scipy.sparse as sp

# Load the dataset
df = pd.read_csv("phishing_site_urls.csv")

# Remove duplicates and handle missing values
df = df.drop_duplicates(subset='URL')
df = df.dropna(subset=['URL'])

# Normalize URLs
df['URL'] = df['URL'].str.lower().str.strip().str.rstrip('/')
df['URL'] = df['URL'].apply(lambda x: re.sub(r'[^a-zA-Z0-9/:.?=&_-]', '', x))

# Extract URL components
df['domain'] = df['URL'].apply(lambda x: urlparse(x).netloc)
df['path'] = df['URL'].apply(lambda x: urlparse(x).path)
df['query'] = df['URL'].apply(lambda x: urlparse(x).query)

# Remove shortened URLs
shorteners = ['bit.ly', 'goo.gl', 'tinyurl.com']
df = df[~df['domain'].isin(shorteners)]

# Add additional features
df['url_length'] = df['URL'].apply(len)
df['num_dots'] = df['URL'].apply(lambda x: x.count('.'))

# Convert categorical labels to numeric values
label_mapping = {'good': 0, 'bad': 1}
df['Label'] = df['Label'].map(label_mapping)

# Replace lambda with a named function for tokenization
def custom_tokenizer(url):
    return url.split('/')

# Tokenize and vectorize URLs
vectorizer = CountVectorizer(tokenizer=custom_tokenizer, token_pattern=None)
X_url = vectorizer.fit_transform(df['URL'])

# Combine URL features with additional features
X_additional = df[['url_length', 'num_dots']].values
X_combined = sp.hstack([X_url, X_additional])

# Define target variable
y = df['Label']

# Sample data before splitting
df_sampled = df.sample(frac=0.1, random_state=42)

# Split the data into training and test sets
X = sp.hstack([vectorizer.transform(df_sampled['URL']), df_sampled[['url_length', 'num_dots']].values])
y = df_sampled['Label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the XGBoost model
model = xgb.XGBClassifier(max_depth=5, eval_metric='logloss')
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("ROC AUC Score:", roc_auc_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the XGBoost model
with open('xgboost_phishing_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

# Save the vectorizer
with open('vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)
