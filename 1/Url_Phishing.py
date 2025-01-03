import pandas as pd
import re
import time
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import dill
import scipy.sparse as sp
import os

# Start time for the entire process
start_time = time.time()

# Load the dataset
load_start = time.time()
df = pd.read_csv(r"1/phishing_site_urls.csv")
print(f"Dataset loaded in {time.time() - load_start:.2f} seconds")

# Remove duplicates and handle missing values
preprocess_start = time.time()
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
print(f"Preprocessing done in {time.time() - preprocess_start:.2f} seconds")

# Replace lambda with a named function for tokenization
def custom_tokenizer(url):
    return url.split('/')

# Tokenize and vectorize URLs
tokenization_start = time.time()
vectorizer = CountVectorizer(tokenizer=custom_tokenizer, token_pattern=None)
X_url = vectorizer.fit_transform(df['URL'])
print(f"Tokenization and vectorization done in {time.time() - tokenization_start:.2f} seconds")

# Combine URL features with additional features
X_additional = df[['url_length', 'num_dots']].values
X_combined = sp.hstack([X_url, X_additional])

# Define target variable
y = df['Label']

# Sample data before splitting
sampling_start = time.time()
df_sampled = df.sample(frac=1, random_state=42)
print(f"Sampling done in {time.time() - sampling_start:.2f} seconds")

# Split the data into training and test sets
split_start = time.time()
X = sp.hstack([vectorizer.transform(df_sampled['URL']), df_sampled[['url_length', 'num_dots']].values])
y = df_sampled['Label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data split into train and test sets in {time.time() - split_start:.2f} seconds")

# Convert to DMatrix format
train_start = time.time()
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Set parameters
params = {
    'max_depth': 5,
    'objective': 'binary:logistic',
    'eval_metric': 'logloss'
}

# Train model
model = xgb.train(
    params,
    dtrain,
    num_boost_round=100,
    evals=[(dtrain, 'train'), (dtest, 'test')],
    verbose_eval=True
)
print(f"Model training done in {time.time() - train_start:.2f} seconds")
prediction_start = time.time()
y_pred = model.predict(dtest)
y_pred_binary = [1 if p > 0.5 else 0 for p in y_pred]
print(f"Predictions made in {time.time() - prediction_start:.2f} seconds")

# Evaluate the model
print("ROC AUC Score:", roc_auc_score(y_test, y_pred))
print(classification_report(y_test, y_pred_binary))

# Create output directory if it doesn't exist
output_dir = "1"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the model in XGBoost's native format
save_model_start = time.time()
model.save_model(os.path.join(output_dir, 'xgboost_phishing_model.json'))
print(f"Model saved in {time.time() - save_model_start:.2f} seconds")

# Save the vectorizer using dill
save_vectorizer_start = time.time()
with open(os.path.join(output_dir, 'vectorizer.pkl'), 'wb') as vectorizer_file:
    dill.dump(vectorizer, vectorizer_file)
print(f"Vectorizer saved in {time.time() - save_vectorizer_start:.2f} seconds")

# Total time for the process
print(f"Total time taken: {time.time() - start_time:.2f} seconds")