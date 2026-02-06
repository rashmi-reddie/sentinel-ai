from sklearn.ensemble import IsolationForest
import numpy as np

def train_basic_model():
    # We create a model that learns what 'normal' transactions look like
    # Normally we'd use real historical data, but we'll seed it here
    model = IsolationForest(contamination=0.1) 
    
    # Fake training data: most transactions are between $10 and $500
    X_train = np.random.uniform(10, 500, (100, 1))
    model.fit(X_train)
    return model

def predict_fraud(model, amount):
    # Returns True if it's an anomaly, False if it's normal
    prediction = model.predict([[amount]])
    return True if prediction[0] == -1 else False