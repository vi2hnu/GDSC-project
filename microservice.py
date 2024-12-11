# career_prediction_service.py
import pandas as pd
from flask import Flask, request, jsonify
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load model and career mapping at startup
model = joblib.load('career_prediction_model.joblib')
career_mapping = joblib.load('career_mapping.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from request
    data = request.get_json()
    
    # Convert JSON data to DataFrame
    input_data = pd.DataFrame([data])
    
    # Predict with the loaded model
    prediction = model.predict(input_data)
    
    # Convert prediction to career
    predicted_career = career_mapping[int(prediction[0])]
    
    return jsonify({'predicted_career': predicted_career})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
