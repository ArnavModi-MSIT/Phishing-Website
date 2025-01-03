import xgboost as xgb
import os
import dill
import scipy.sparse as sp

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

def load_model():
    try:
        # Load model
        model = xgb.Booster()
        model_path = os.path.join(current_dir, 'xgboost_phishing_model.json')
        model.load_model(model_path)
        
        # Load vectorizer
        vectorizer_path = os.path.join(current_dir, 'vectorizer.pkl')
        with open(vectorizer_path, 'rb') as f:
            vectorizer = dill.load(f)
            
        return model, vectorizer
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

# Load model and vectorizer once when module is imported
MODEL, VECTORIZER = load_model()

def predict_url(url):
    try:
        if MODEL is None or VECTORIZER is None:
            return "Error: Model not loaded"
            
        # Preprocess URL
        url = url.lower().strip().rstrip('/')
        url = re.sub(r'[^a-zA-Z0-9/:.?=&_-]', '', url)
        
        # Create features
        X_url = VECTORIZER.transform([url])
        X_additional = sp.csr_matrix([[len(url), url.count('.')]])
        X_combined = sp.hstack([X_url, X_additional])
        
        # Convert to DMatrix
        dtest = xgb.DMatrix(X_combined)
        
        # Predict
        prediction = MODEL.predict(dtest)
        return 'Bad' if prediction[0] > 0.5 else 'Good'
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error during prediction"