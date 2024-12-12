from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
import google.generativeai as genai

genai.configure(api_key="Gemini-api")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

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
    
    # Send requests to chat session and get the message content
    response1 = chat_session.send_message(f"tell me about this job in 10 words followed by if it is (high pay/low pay/average pay). Job: {career_mapping[round(prediction[0])]}")
    response2 = chat_session.send_message(f"tell me about this job in 10 words followed by if it is (high pay/low pay/average pay). Job: {career_mapping[round(prediction[0]) + 1]}")
    response3 = chat_session.send_message(f"tell me about this job in 10 words followed by if it is (high pay/low pay/average pay). Job: {career_mapping[round(prediction[0]) - 1]}")
    
    # Extract the content of each response
    response1_text = career_mapping[round(prediction[0])] +". Job desc: "+ response1.text[:-1]
    response2_text = career_mapping[round(prediction[0])+1]+". Job desc: "+ response2.text[:-1]
    response3_text = career_mapping[round(prediction[0])-1]+". Job desc: "+  response3.text[:-1]
    
    # Return the predicted career along with the responses as a JSON
    return jsonify({"predicted_career": [response1_text, response2_text, response3_text]})


if __name__ == '__main__':
    app.run(debug=True)
