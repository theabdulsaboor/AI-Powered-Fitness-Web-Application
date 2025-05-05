import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Get the base directory (project root)
base_dir = os.path.abspath(os.path.dirname(__file__))

# Define file paths
combinations_path = os.path.join(base_dir, 'cvs', 'updated_workout_plan_combinations.csv')
workout_plans_path = os.path.join(base_dir, 'cvs', 'workout_profile_classifications.csv')
model_path = os.path.join(base_dir, 'app', 'static', 'models', 'workout_model.joblib')
label_encoders_path = os.path.join(base_dir, 'app', 'static', 'models', 'label_encoders.joblib')

# Load the datasets with different encodings
try:
    combinations_df = pd.read_csv(combinations_path, encoding='utf-8')
except UnicodeDecodeError:
    combinations_df = pd.read_csv(combinations_path, encoding='latin1')

try:
    workout_plans_df = pd.read_csv(workout_plans_path, encoding='utf-8')
except UnicodeDecodeError:
    workout_plans_df = pd.read_csv(workout_plans_path, encoding='latin1')

# Create label encoders for categorical variables
label_encoders = {}
categorical_columns = ['Age Group', 'Gender', 'Fitness Goal', 'Fitness Level', 'Equipment', 'Days per Week']

for column in categorical_columns:
    label_encoders[column] = LabelEncoder()
    combinations_df[column] = label_encoders[column].fit_transform(combinations_df[column])

# Prepare features and target
X = combinations_df[categorical_columns]
y = combinations_df['Workout Profile']

# Train the Decision Tree model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Save the model and label encoders
joblib.dump(model, model_path)
joblib.dump(label_encoders, label_encoders_path)

print("Model and label encoders have been saved successfully!")

# Create a function to predict workout profile
def predict_workout_profile(age, gender, fitness_goal, fitness_level, equipment, days_per_week):
    # Convert age to age group
    if age <= 25:
        age_group = '18-25'
    elif age <= 35:
        age_group = '26-35'
    elif age <= 45:
        age_group = '36-45'
    else:
        age_group = '46+'
    
    # Prepare input data
    input_data = {
        'Age Group': [age_group],
        'Gender': [gender],
        'Fitness Goal': [fitness_goal],
        'Fitness Level': [fitness_level],
        'Equipment': [equipment],
        'Days per Week': [days_per_week]
    }
    
    # Transform input data using label encoders
    for column in categorical_columns:
        input_data[column] = label_encoders[column].transform(input_data[column])
    
    # Create DataFrame
    input_df = pd.DataFrame(input_data)
    
    # Make prediction
    workout_profile = model.predict(input_df)[0]
    
    # Get workout plan
    workout_plan = workout_plans_df[workout_plans_df['Workout Profile'] == workout_profile].iloc[0]
    
    return {
        'workout_profile': int(workout_profile),
        'summary': workout_plan['Summary'],
        'workout': workout_plan['Workout']
    }

# Test the function
test_input = {
    'age': 25,
    'gender': 'Male',
    'fitness_goal': 'Weight Loss',
    'fitness_level': 'Beginner',
    'equipment': 'No Equipment',
    'days_per_week': '1-3'
}

result = predict_workout_profile(**test_input)
print("\nTest prediction:")
print(f"Workout Profile: {result['workout_profile']}")
print(f"Summary: {result['summary']}")
print(f"Workout Plan: {result['workout']}") 