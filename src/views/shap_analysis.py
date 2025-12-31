"""
SHAP Analysis View
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import shap
from models.model_loader import load_models
from models.data_loader import load_train_test_data
from config.settings import CATEGORICAL_COLS


def render():
    """Render SHAP analysis page"""
    st.header("🔍 SHAP Analysis - Model Explainability")
    st.markdown("Understand how each feature contributes to predictions")
    st.markdown("---")
    
    models = load_models()
    
    if not models:
        st.error("⚠️ No models found!")
        return
    
    st.info("💡 **What is SHAP?** SHAP (SHapley Additive exPlanations) explains model predictions by showing how much each feature contributed to the final prediction.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        model_name = st.selectbox("🤖 Select Model for Analysis", list(models.keys()))
    
    with col2:
        sample_size = st.slider("Sample Size", 50, 200, 100, 
                               help="Number of samples to use for SHAP analysis")
    
    analyze_button = st.button("🔬 Generate SHAP Analysis", type="primary", use_container_width=True)
    
    if analyze_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("📂 Loading data...")
            progress_bar.progress(20)
            
            data = load_train_test_data()
            
            if 'X_train' in data and 'X_test' in data:
                X_train = data['X_train']
                X_test = data['X_test']

                # Ensure numeric, aligned frames for SHAP
                X_train, X_test = _prepare_data_for_shap(X_train, X_test)

                # Sample data for faster computation
                X_test_sample = X_test.sample(min(sample_size, len(X_test)), random_state=42)
                
                status_text.text("🧮 Computing SHAP values...")
                progress_bar.progress(40)
                
                model = models[model_name]
                
                # Create explainer on numeric data
                explainer = shap.Explainer(model, X_train.sample(min(100, len(X_train))))
                shap_values = explainer(X_test_sample)
                
                progress_bar.progress(70)
                status_text.text("📊 Generating visualizations...")
                
                st.success("✅ SHAP analysis complete!")
                progress_bar.progress(100)
                status_text.empty()
                
                st.markdown("---")
                
                # Tabs for different visualizations
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary Plot", "📈 Feature Importance", 
                                                   "🎯 Individual Prediction", "📋 Data Table"])
                
                with tab1:
                    _render_summary_plot(shap_values, X_test_sample, model_name)
                
                with tab2:
                    _render_feature_importance(shap_values, X_train, model_name)
                
                with tab3:
                    _render_individual_prediction(shap_values, X_test_sample)
                
                with tab4:
                    _render_data_table(shap_values, X_train, model_name)
                
                # Store in session
                st.session_state['shap_values'] = shap_values
                st.session_state['shap_features'] = X_test_sample
                
            else:
                st.error("❌ Training/Test data not found!")
                
        except Exception as e:
            st.error(f"❌ Error during SHAP analysis: {str(e)}")
            st.exception(e)
        finally:
            progress_bar.empty()
            status_text.empty()


def _render_summary_plot(shap_values, X_test_sample, model_name):
    """Render SHAP summary plot"""
    st.subheader("📊 SHAP Summary Plot")
    st.markdown("Shows the distribution of SHAP values for each feature")
    
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 8), facecolor="#0f172a")
    ax.set_facecolor("#0f172a")
    shap.summary_plot(shap_values, X_test_sample, show=False)
    plt.title(f'SHAP Summary Plot - {model_name}', fontsize=16, pad=20, color="#e5e7eb")
    st.pyplot(fig)
    plt.close()
    
    st.info("""
    **How to read this plot:**
    - Each dot represents a sample
    - Color indicates feature value (red = high, blue = low)
    - X-axis shows impact on prediction
    - Features are ranked by importance (top to bottom)
    """)


def _render_feature_importance(shap_values, X_train, model_name):
    """Render feature importance ranking"""
    st.subheader("📈 Feature Importance Ranking")
    
    feature_importance = pd.DataFrame({
        'Feature': X_train.columns,
        'Importance': np.abs(shap_values.values).mean(axis=0)
    }).sort_values('Importance', ascending=False)
    
    # Interactive bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=feature_importance['Importance'],
        y=feature_importance['Feature'],
        orientation='h',
        marker=dict(
            color=feature_importance['Importance'],
            colorscale='Viridis'
        ),
        text=feature_importance['Importance'].round(4),
        textposition='auto',
        textfont=dict(color='white', size=12, family='Inter')
    ))
    fig.update_layout(
        title=f'Feature Importance - {model_name}',
        xaxis_title='Mean |SHAP Value|',
        yaxis_title='Feature',
        height=500,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#e5e7eb', family='Inter'),
        xaxis=dict(gridcolor='#1f2937'),
        yaxis=dict(categoryorder='total ascending', gridcolor='#1f2937')
    )
    st.plotly_chart(fig, key='shap_waterfall', use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top 5 Features")
        for idx, row in feature_importance.head(5).iterrows():
            st.metric(row['Feature'], f"{row['Importance']:.4f}")
    
    with col2:
        st.markdown("### 📉 Bottom 5 Features")
        for idx, row in feature_importance.tail(5).iterrows():
            st.metric(row['Feature'], f"{row['Importance']:.4f}")


def _render_individual_prediction(shap_values, X_test_sample):
    """Render individual prediction explanation"""
    st.subheader("🎯 Individual Prediction Explanation")
    
    sample_idx = st.slider("Select Sample Index", 0, len(X_test_sample)-1, 0)
    
    st.markdown(f"**Analyzing Sample #{sample_idx}**")
    
    # Waterfall plot
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#0f172a")
    ax.set_facecolor("#0f172a")
    shap.waterfall_plot(shap_values[sample_idx], show=False)
    st.pyplot(fig)
    plt.close()
    
    # Show input features
    st.markdown("### 📋 Input Features for this Sample")
    sample_data = X_test_sample.iloc[sample_idx]
    
    col1, col2 = st.columns(2)
    features_list = list(sample_data.items())
    mid = len(features_list) // 2
    
    with col1:
        for feature, value in features_list[:mid]:
            st.metric(feature, f"{value:.2f}")
    
    with col2:
        for feature, value in features_list[mid:]:
            st.metric(feature, f"{value:.2f}")


def _render_data_table(shap_values, X_train, model_name):
    """Render feature importance data table"""
    st.subheader("📋 Feature Importance Data")
    
    feature_importance = pd.DataFrame({
        'Feature': X_train.columns,
        'Importance': np.abs(shap_values.values).mean(axis=0)
    }).sort_values('Importance', ascending=False)
    
    st.dataframe(feature_importance, use_container_width=True)
    
    csv = feature_importance.to_csv(index=False)
    st.download_button(
        label="📥 Download Feature Importance CSV",
        data=csv,
        file_name=f"shap_importance_{model_name}.csv",
        mime="text/csv"
    )


def _prepare_data_for_shap(X_train: pd.DataFrame, X_test: pd.DataFrame):
    """Align train/test, one-hot encode categoricals, coerce all features to float64."""
    train = X_train.copy()
    test = X_test.copy()

    # One-hot encode known categoricals if present
    cat_cols = [c for c in CATEGORICAL_COLS if c in train.columns]
    if cat_cols:
        train = pd.get_dummies(train, columns=cat_cols, drop_first=False)
        test = pd.get_dummies(test, columns=cat_cols, drop_first=False)
        test = test.reindex(columns=train.columns, fill_value=0)

    # Convert any remaining object columns to category codes
    obj_cols = train.select_dtypes(include=['object']).columns
    for col in obj_cols:
        train[col] = train[col].astype('category').cat.codes
        test[col] = test[col].astype('category').cat.codes

    # Convert boolean columns to int
    bool_cols = train.select_dtypes(include=['bool']).columns
    for col in bool_cols:
        train[col] = train[col].astype(int)
        test[col] = test[col].astype(int)

    # Coerce all columns to numeric, then float64
    for col in train.columns:
        train[col] = pd.to_numeric(train[col], errors='coerce')
        test[col] = pd.to_numeric(test[col], errors='coerce')

    # Final cast to float64 and fill any NaNs with 0
    train = train.astype('float64', errors='ignore').fillna(0)
    test = test.astype('float64', errors='ignore').fillna(0)

    return train, test
