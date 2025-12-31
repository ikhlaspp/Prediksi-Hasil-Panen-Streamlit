"""
Data loading utilities
"""
import os
import pandas as pd
import streamlit as st
from typing import Dict, Optional


# Get paths from config
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from config.settings import (
    DATASET_PATH, X_TRAIN_PATH, X_TEST_PATH, 
    Y_TRAIN_PATH, Y_TEST_PATH, METRICS_PATH
)


@st.cache_data
def load_dataset() -> Optional[pd.DataFrame]:
    """
    Load the main dataset
    
    Returns:
        DataFrame or None if file not found
    """
    try:
        if os.path.exists(DATASET_PATH):
            # CSV uses semicolon as separator and comma as decimal
            df = pd.read_csv(DATASET_PATH, sep=';', decimal=',')
            return df
        else:
            st.warning(f"⚠️ Dataset not found: {DATASET_PATH}")
            return None
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        return None


@st.cache_data
def load_train_test_data() -> Dict[str, pd.DataFrame]:
    """
    Load train/test split data
    
    Returns:
        Dictionary with X_train, X_test, y_train, y_test DataFrames
    """
    data = {}
    
    try:
        if os.path.exists(X_TRAIN_PATH):
            data['X_train'] = pd.read_csv(X_TRAIN_PATH)
        if os.path.exists(X_TEST_PATH):
            data['X_test'] = pd.read_csv(X_TEST_PATH)
        if os.path.exists(Y_TRAIN_PATH):
            data['y_train'] = pd.read_csv(Y_TRAIN_PATH)
        if os.path.exists(Y_TEST_PATH):
            data['y_test'] = pd.read_csv(Y_TEST_PATH)
            
    except Exception as e:
        st.error(f"❌ Error loading train/test data: {str(e)}")
        
    return data


@st.cache_data
def load_metrics() -> Optional[pd.DataFrame]:
    """
    Load model comparison metrics
    
    Returns:
        DataFrame with model metrics or None if not found
    """
    try:
        if os.path.exists(METRICS_PATH):
            metrics_df = pd.read_csv(METRICS_PATH)
            return metrics_df
        else:
            st.warning(f"⚠️ Metrics file not found: {METRICS_PATH}")
            return None
    except Exception as e:
        st.error(f"❌ Error loading metrics: {str(e)}")
        return None


def get_best_model() -> Optional[str]:
    """
    Get the name of the best performing model based on R² score
    
    Returns:
        Name of best model or None if metrics not available
    """
    try:
        metrics_df = load_metrics()
        
        if metrics_df is None or metrics_df.empty:
            return None
            
        # Find model with highest R² score
        if 'R²' in metrics_df.columns and 'Model' in metrics_df.columns:
            best_idx = metrics_df['R²'].idxmax()
            return metrics_df.loc[best_idx, 'Model']
        elif 'r2' in metrics_df.columns and 'Model' in metrics_df.columns:
            best_idx = metrics_df['r2'].idxmax()
            return metrics_df.loc[best_idx, 'Model']
        else:
            return None
            
    except Exception as e:
        st.error(f"❌ Error getting best model: {str(e)}")
        return None
