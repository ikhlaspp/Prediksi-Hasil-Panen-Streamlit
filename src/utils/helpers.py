"""
Helper utility functions
"""
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error


def calculate_metrics(y_true, y_pred):
    """Calculate all evaluation metrics"""
    return {
        'R2': r2_score(y_true, y_pred),
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'MAPE': mean_absolute_percentage_error(y_true, y_pred) * 100
    }


def encode_features(df, encoders):
    """Encode categorical features"""
    df_encoded = df.copy()
    
    for col, encoder in encoders.items():
        if col in df_encoded.columns:
            df_encoded[col] = encoder.transform(df_encoded[col])
    
    return df_encoded


def prepare_input_features(data, encoders):
    """Prepare input features for prediction"""
    features = pd.DataFrame({
        'Soil_Type': [encoders['Soil_Type'].transform([data['soil']])[0]],
        'Crop': [encoders['Crop'].transform([data['crop']])[0]],
        'Rainfall_mm': [data['rainfall']],
        'Temperature_Celsius': [data['temperature']],
        'Fertilizer_Used': [int(data['fertilizer'])],
        'Irrigation_Used': [int(data['irrigation'])],
        'Weather_Condition': [encoders['Weather_Condition'].transform([data['weather']])[0]],
        'Days_to_Harvest': [data['days']]
    })
    
    return features


def validate_csv_upload(df, required_columns):
    """Validate uploaded CSV file"""
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing columns: {', '.join(missing_cols)}"
    
    return True, "Validation successful"


def format_number(number, decimals=2):
    """Format number with specific decimal places"""
    return f"{number:.{decimals}f}"


def format_percentage(number, decimals=2):
    """Format number as percentage"""
    return f"{number:.{decimals}f}%"
