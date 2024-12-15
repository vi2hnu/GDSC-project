#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('/home/vishnu/Documents/Vit/project/cs_students.csv')

# Encode categorical columns
career_encoder = LabelEncoder()
data['Future Career'] = career_encoder.fit_transform(data['Future Career'])
career_mapping = {index: career for index, career in enumerate(career_encoder.classes_)}

domain_encoder = LabelEncoder()
data['Interested Domain'] = domain_encoder.fit_transform(data['Interested Domain'])

projects_encoder = LabelEncoder()
data['Projects'] = projects_encoder.fit_transform(data['Projects'])

# Drop unnecessary columns
data = data.drop(['Student ID', 'Name', 'Major'], axis=1)

# Encode Gender
data['Gender'] = data['Gender'].apply(lambda x: 0 if x == "Female" else 1)

# One-hot encoding for Python, SQL, and Java skills
data = data.join(pd.get_dummies(data["Python"]).astype(int)).drop("Python", axis=1)
data = data.join(pd.get_dummies(data['SQL'], prefix='SQL').astype(int)).drop("SQL", axis=1)
data = data.join(pd.get_dummies(data['Java'], prefix='Java').astype(int)).drop("Java", axis=1)

# Prepare data for training
X = data.drop('Future Career', axis=1)
y = data['Future Career']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
reg = RandomForestRegressor(random_state=42)
reg.fit(X_train, y_train)

# Evaluate the model
print(f"Model Accuracy: {reg.score(X_test, y_test):.2f}")

# Save the trained model and encoders
joblib.dump(reg, "trained_model.pkl")
joblib.dump(career_encoder, "career_encoder.pkl")
joblib.dump(domain_encoder, "domain_encoder.pkl")
joblib.dump(projects_encoder, "projects_encoder.pkl")
joblib.dump(career_mapping, "career_mapping.pkl")

print("Model and encoders saved successfully!")

# Example prediction
sample_data = {
    'Gender': 0,
    'Age': 20,
    'GPA': 3.2,
    'Interested Domain': 10,
    'Projects': 15,
    'Average': 0,
    'Strong': 1,
    'Weak': 0,
    'SQL_Average': 0,
    'SQL_Strong': 1,
    'SQL_Weak': 0,
    'Java_Average': 0,
    'Java_Strong': 0,
    'Java_Weak': 1
}
single_sample_df = pd.DataFrame([sample_data])
prediction = reg.predict(single_sample_df)
predicted_career = career_mapping[int(prediction[0])]
print(f"Predicted Career: {predicted_career}")
