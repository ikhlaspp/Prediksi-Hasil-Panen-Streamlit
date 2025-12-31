"""
Model loading utilities
"""
import os
import pickle
import joblib
import streamlit as st
import xgboost as xgb
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional


# Get model paths from config
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from config.settings import MODEL_PATHS


@st.cache_resource
def load_models() -> Dict[str, Any]:
    """
    Load all trained models
    
    Returns:
        Dict mapping model names to loaded model objects
    """
    models = {}
    
    for model_name, model_path in MODEL_PATHS.items():
        try:
            if not os.path.exists(model_path):
                st.warning(f"⚠️ Model file not found: {model_path}")
                continue
                
            if model_name == 'XGBoost':
                # Load XGBoost model from JSON
                model = xgb.XGBRegressor()
                model.load_model(model_path)
                models[model_name] = model
            else:
                # Load joblib/pickle models (Decision Tree, etc.)
                try:
                    # Try joblib first (preferred for sklearn models)
                    models[model_name] = joblib.load(model_path)
                except Exception:
                    # Fallback to pickle
                    with open(model_path, 'rb') as f:
                        models[model_name] = pickle.load(f)
                    
        except Exception as e:
            st.error(f"❌ Error loading {model_name}: {str(e)}")
            
    return models


def predict(model: Any, input_data: pd.DataFrame) -> Optional[np.ndarray]:
    """
    Make prediction using the provided model
    
    Args:
        model: Trained model object
        input_data: DataFrame with features
        
    Returns:
        Predicted values as numpy array or None if error occurs
    """
    try:
        prediction = model.predict(input_data)
        
        # Ensure prediction is a numpy array
        if isinstance(prediction, np.ndarray):
            return prediction
        else:
            return np.array([prediction])
            
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        return None
