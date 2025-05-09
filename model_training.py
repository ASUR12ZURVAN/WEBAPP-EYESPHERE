# train_model.py (run once outside Django)
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

# Create output directory
os.makedirs('eyeapp/ml', exist_ok=True)

# Data: line numbers and logMAR
line_numbers = np.arange(1, 16)
logmar_values = 1.0 - 0.1 * (line_numbers - 1)
diopter_values = -2.5 * logmar_values

# Fit model
model = LinearRegression()
model.fit(logmar_values.reshape(-1, 1), diopter_values)

# Save model
joblib.dump(model, 'eyeapp/ml/snellen_diopter_model.joblib')
print("Model saved to eyeapp/ml/snellen_diopter_model.joblib")
