import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib
import os
import pandas as pd

class WorkoutGenerator:
    def __init__(self):
        # Get the base directory (project root)
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        # Define file paths
        self.model_path = os.path.join(self.base_dir, 'app', 'static', 'models', 'workout_model.joblib')
        self.label_encoders_path = os.path.join(self.base_dir, 'app', 'static', 'models', 'label_encoders.joblib')
        
        # Load the trained model and label encoders
        try:
            self.model = joblib.load(self.model_path)
            self.label_encoders = joblib.load(self.label_encoders_path)
        except Exception as e:
            print(f"Error loading model files: {str(e)}")
            raise
        
        # Define categorical columns
        self.categorical_columns = ['Age Group', 'Gender', 'Fitness Goal', 'Fitness Level', 'Equipment', 'Days per Week']
    
    def _convert_age_to_group(self, age):
        if age <= 25:
            return '18-25'
        elif age <= 35:
            return '26-35'
        elif age <= 45:
            return '36-45'
        else:
            return '46+'
    
    def generate_workout_plan(self, user_data):
        try:
            # Convert age to age group
            age_group = self._convert_age_to_group(user_data['age'])
            
            # Prepare input data with correct format
            input_data = {
                'Age Group': [age_group],
                'Gender': [user_data['gender']],
                'Fitness Goal': [user_data['fitness_goal']],
                'Fitness Level': [user_data['fitness_level']],
                'Equipment': [user_data['equipment']],
                'Days per Week': [user_data['days_per_week']]
            }
            
            # Transform input data using label encoders
            for column in self.categorical_columns:
                input_data[column] = self.label_encoders[column].transform(input_data[column])
            
            # Create DataFrame
            input_df = pd.DataFrame(input_data)
            
            # Make prediction
            workout_profile = int(self.model.predict(input_df)[0])  # Convert to integer
            
            return {
                'workout_profile': workout_profile,
                'model_version': '1.0',
                'confidence_score': 0.85  # Placeholder confidence score
            }
        except Exception as e:
            print(f"Error generating workout profile: {str(e)}")
            raise

    def _get_exercises_for_type(self, workout_type):
        # This is a simplified example. In a real application, you would have a more
        # comprehensive exercise database
        exercise_db = {
            'strength': [
                {'name': 'Bench Press', 'sets': 3, 'reps': 10},
                {'name': 'Squats', 'sets': 3, 'reps': 12},
                {'name': 'Deadlifts', 'sets': 3, 'reps': 8}
            ],
            'cardio': [
                {'name': 'Running', 'duration': 20},
                {'name': 'Jump Rope', 'duration': 15},
                {'name': 'Burpees', 'duration': 10}
            ]
        }
        return exercise_db.get(workout_type, []) 