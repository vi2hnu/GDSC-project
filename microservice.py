from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model and encoders
model = joblib.load("trained_model.pkl")
career_encoder = joblib.load("career_encoder.pkl")
career_mapping = joblib.load("career_mapping.pkl")

# Function to preprocess input data
def preprocess_input_data(input_data):
    # Rename features to match training data
    input_data['Interested Domain'] = input_data.pop('InterestedDomain', None)


    return input_data

# Function to handle the prediction
@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json  # Get JSON input from request
    
    print(f"Received input data: {input_data}")  # Log the received input
    
    # Preprocess and encode the input data to match the training set
    input_data = preprocess_input_data(input_data)
    
    # Convert to a DataFrame for prediction
    input_df = pd.DataFrame([input_data])
    
    # Make prediction using the trained model
    prediction = model.predict(input_df)
    
    # Map prediction back to the career
    predicted_career = career_mapping[round(prediction[0])]
    
    # Return the predicted career as a JSON response
    return jsonify({"predicted_career": predicted_career})

if __name__ == '__main__':
    app.run(debug=True)
