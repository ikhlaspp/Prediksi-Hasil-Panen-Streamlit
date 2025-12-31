"""
Configuration settings for the Crop Yield Prediction System
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')

# Dataset paths
DATASET_PATH = os.path.join(DATA_DIR, 'dataset_800.csv')
X_TRAIN_PATH = os.path.join(DATA_DIR, 'X_train.csv')
X_TEST_PATH = os.path.join(DATA_DIR, 'X_test.csv')
Y_TRAIN_PATH = os.path.join(DATA_DIR, 'y_train.csv')
Y_TEST_PATH = os.path.join(DATA_DIR, 'y_test.csv')

# Model paths (only Decision Tree and XGBoost)
MODEL_PATHS = {
    'Decision Tree': os.path.join(MODEL_DIR, 'decision_tree.pkl'),
    'XGBoost': os.path.join(MODEL_DIR, 'xgboost_model.json')
}

METRICS_PATH = os.path.join(MODEL_DIR, 'model_comparison.csv')

# App configuration
APP_TITLE = "Crop Yield Prediction System"
APP_ICON = "🌾"
APP_LAYOUT = "wide"

# Import theme configuration
from config.theme import COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS, TRANSITIONS

# Categorical columns
CATEGORICAL_COLS = ['Soil_Type', 'Crop', 'Weather_Condition']

# Feature names
FEATURE_NAMES = [
    'Soil_Type', 'Crop', 'Rainfall_mm', 'Temperature_Celsius',
    'Fertilizer_Used', 'Irrigation_Used', 'Weather_Condition', 'Days_to_Harvest'
]

# Page names
PAGES = {
    'home': '🏠 Home',
    'prediction': '🔮 Single Prediction',
    'performance': '📊 Model Performance',
    'shap': '🔍 SHAP Analysis',
    'visualization': '📈 Data Visualization',
    'batch': '🤖 Batch Prediction',
    'comparison': '⚖️ Model Comparison'
}
