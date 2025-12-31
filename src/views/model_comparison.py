"""
Model Comparison View
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
import plotly.graph_objects as go
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from models.model_loader import load_models
from models.data_loader import load_metrics, load_train_test_data


def render():
    """Render model comparison page"""
    st.header("⚖️ Model Comparison")
    st.markdown("Compare multiple models side-by-side")
    st.markdown("---")
    
    models = load_models()
    metrics_df = load_metrics()
    
    if not models or len(models) < 2:
        st.warning("⚠️ Need at least 2 models for comparison")
        return
    
    st.subheader("🤖 Select Models to Compare")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model1 = st.selectbox("Model 1", list(models.keys()), key='model1')
    
    with col2:
        model2 = st.selectbox("Model 2", 
                             [m for m in models.keys() if m != model1], 
                             key='model2')
    
    if st.button("⚖️ Compare Models", type="primary"):
        with st.spinner("🔄 Running comparison..."):
            _compare_models(model1, model2, models)


def _compare_models(model1, model2, models):
    """Compare two models"""
    try:
        data = load_train_test_data()
        
        if 'X_test' in data and 'y_test' in data:
            X_test = data['X_test']
            y_test = data['y_test']
            
            # Get predictions from both models
            m1 = models[model1]
            m2 = models[model2]
            
            pred1 = m1.predict(X_test) if model1 != 'LightGBM' else m1.predict(X_test)
            pred2 = m2.predict(X_test) if model2 != 'LightGBM' else m2.predict(X_test)
            
            # Calculate metrics
            metrics1 = {
                'R2': r2_score(y_test, pred1),
                'MAE': mean_absolute_error(y_test, pred1),
                'RMSE': np.sqrt(mean_squared_error(y_test, pred1)),
                'MAPE': mean_absolute_percentage_error(y_test, pred1) * 100
            }

            metrics2 = {
                'R2': r2_score(y_test, pred2),
                'MAE': mean_absolute_error(y_test, pred2),
                'RMSE': np.sqrt(mean_squared_error(y_test, pred2)),
                'MAPE': mean_absolute_percentage_error(y_test, pred2) * 100
            }
            
            st.success("✅ Comparison complete!")
            st.markdown("---")
            
            # Metrics comparison
            _render_metrics_comparison(model1, model2, metrics1, metrics2)
            
            # Visual comparison
            _render_visual_comparison(model1, model2, y_test, pred1, pred2)
            
            # Direct comparison scatter
            _render_direct_comparison(model1, model2, y_test, pred1, pred2)
            
        else:
            st.error("❌ Test data not found!")
            
    except Exception as e:
        st.error(f"❌ Comparison error: {str(e)}")
        st.exception(e)


def _render_metrics_comparison(model1, model2, metrics1, metrics2):
    """Render metrics comparison"""
    st.subheader("📊 Metrics Comparison")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(f"{model1} R²", f"{metrics1['R2']:.4f}")
        st.metric(f"{model2} R²", f"{metrics2['R2']:.4f}",
             delta=f"{(metrics2['R2'] - metrics1['R2']):.4f}")
    
    with col2:
        st.metric(f"{model1} MAE", f"{metrics1['MAE']:.4f}")
        st.metric(f"{model2} MAE", f"{metrics2['MAE']:.4f}",
                 delta=f"{(metrics1['MAE'] - metrics2['MAE']):.4f}")
    
    with col3:
        st.metric(f"{model1} RMSE", f"{metrics1['RMSE']:.4f}")
        st.metric(f"{model2} RMSE", f"{metrics2['RMSE']:.4f}",
                 delta=f"{(metrics1['RMSE'] - metrics2['RMSE']):.4f}")
    
    with col4:
        st.metric(f"{model1} MAPE", f"{metrics1['MAPE']:.2f}%")
        st.metric(f"{model2} MAPE", f"{metrics2['MAPE']:.2f}%",
                 delta=f"{(metrics1['MAPE'] - metrics2['MAPE']):.2f}%")


def _render_visual_comparison(model1, model2, y_test, pred1, pred2):
    """Render visual comparison charts"""
    # Convert y_test to numpy array if it's a DataFrame
    if hasattr(y_test, 'values'):
        y_test = y_test.values.flatten()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model 1 predictions
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_test, y=pred1,
            mode='markers',
            name=model1,
            marker=dict(size=8, color='#667eea', opacity=0.6)
        ))
        fig.add_trace(go.Scatter(
            x=[y_test.min(), y_test.max()],
            y=[y_test.min(), y_test.max()],
            mode='lines',
            name='Perfect',
            line=dict(color='#f5576c', dash='dash', width=3)
        ))
        fig.update_layout(
            title=f'{model1} - Actual vs Predicted',
            xaxis_title='Actual',
            yaxis_title='Predicted',
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, key='model1_pred', use_container_width=True)
    
    with col2:
        # Model 2 predictions
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_test, y=pred2,
            mode='markers',
            name=model2,
            marker=dict(size=8, color='#764ba2', opacity=0.6)
        ))
        fig.add_trace(go.Scatter(
            x=[y_test.min(), y_test.max()],
            y=[y_test.min(), y_test.max()],
            mode='lines',
            name='Perfect',
            line=dict(color='#f5576c', dash='dash', width=3)
        ))
        fig.update_layout(
            title=f'{model2} - Actual vs Predicted',
            xaxis_title='Actual',
            yaxis_title='Predicted',
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, key='model2_pred', use_container_width=True)


def _render_direct_comparison(model1, model2, y_test, pred1, pred2):
    """Render direct comparison scatter plot"""
    # Convert y_test to numpy array if it's a DataFrame
    if hasattr(y_test, 'values'):
        y_test = y_test.values.flatten()
    
    st.subheader("🔄 Direct Prediction Comparison")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pred1, y=pred2,
        mode='markers',
        marker=dict(size=8, color=y_test, 
                   colorscale='Viridis',
                   showscale=True,
                   colorbar=dict(title="Actual Yield")),
        text=[f"Actual: {y:.2f}" for y in y_test],
        hovertemplate="Model1: %{x:.2f}<br>Model2: %{y:.2f}<br>%{text}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=[min(pred1.min(), pred2.min()), max(pred1.max(), pred2.max())],
        y=[min(pred1.min(), pred2.min()), max(pred1.max(), pred2.max())],
        mode='lines',
        name='Agreement Line',
        line=dict(color='#f5576c', dash='dash', width=3)
    ))
    fig.update_layout(
        title=f'{model1} vs {model2} Predictions',
        xaxis_title=f'{model1} Predictions',
        yaxis_title=f'{model2} Predictions',
        height=500,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#e5e7eb', family='Inter'),
        xaxis=dict(gridcolor='#1f2937'),
        yaxis=dict(gridcolor='#1f2937')
    )
    st.plotly_chart(fig, key='direct_comparison', use_container_width=True)
    
    st.info("💡 Points closer to the red line indicate both models agree on the prediction")
