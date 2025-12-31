"""
Model Performance View
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
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from models.model_loader import load_models, predict
from models.data_loader import load_metrics, load_train_test_data


def render():
    """Render model performance page"""
    st.header("📊 Model Performance Analysis")
    st.markdown("Comprehensive evaluation of all trained models")
    st.markdown("---")
    
    models = load_models()
    metrics_df = load_metrics()
    
    if not models:
        st.error("⚠️ No models found!")
        return
    
    if metrics_df is None:
        st.warning("⚠️ No metrics data available")
        return
    
    # Overview Metrics
    st.subheader("📈 Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    r2_col = 'R2' if 'R2' in metrics_df.columns else ('R²' if 'R²' in metrics_df.columns else None)
    if r2_col is None:
        st.warning("Metrics file missing R2 column; please refresh metrics.")
        return

    best_r2_model = metrics_df.loc[metrics_df[r2_col].idxmax(), 'Model']
    best_mae_model = metrics_df.loc[metrics_df['MAE'].idxmin(), 'Model']
    
    col1.metric("🏆 Best Model (R²)", best_r2_model, 
                f"{metrics_df[r2_col].max():.4f}")
    col2.metric("🎯 Best Model (MAE)", best_mae_model,
                f"{metrics_df['MAE'].min():.4f}")
    col3.metric("📊 Models Trained", len(models))
    col4.metric("📉 Avg RMSE", f"{metrics_df['RMSE'].mean():.4f}")
    
    st.markdown("---")
    
    # Interactive Charts
    tab1, tab2, tab3 = st.tabs(["📊 Metrics Comparison", "📈 Detailed Analysis", "📋 Raw Data"])
    
    with tab1:
        _render_metrics_comparison(metrics_df)
    
    with tab2:
        _render_detailed_analysis(models, metrics_df)
    
    with tab3:
        _render_raw_data(metrics_df)


def _render_metrics_comparison(metrics_df):
    """Render metrics comparison charts"""
    r2_col = 'R2' if 'R2' in metrics_df.columns else ('R²' if 'R²' in metrics_df.columns else None)
    if r2_col is None:
        st.warning("Metrics file missing R2 column; please refresh metrics.")
        return
    col1, col2 = st.columns(2)
    
    with col1:
        # R² Score Comparison
        fig = go.Figure()
        colors = ['#7dd3fc', '#c4b5fd'][:len(metrics_df)]
        fig.add_trace(go.Bar(
            x=metrics_df['Model'],
            y=metrics_df[r2_col],
            marker=dict(
                color=colors,
                line=dict(color='#e0f2fe', width=1.6),
                opacity=1.0
            ),
            text=metrics_df[r2_col].round(4),
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        fig.update_layout(
            title='R² Score Comparison',
            xaxis_title='Model',
            yaxis_title='R² Score',
            height=400,
            template='plotly_dark',
            yaxis=dict(range=[0, 1])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # MAE Comparison
        fig = go.Figure()
        colors = ['#4facfe', '#22d3ee'][:len(metrics_df)]
        fig.add_trace(go.Bar(
            x=metrics_df['Model'],
            y=metrics_df['MAE'],
            marker=dict(
                color=colors,
                line=dict(color='#cfe5ff', width=1.0)
            ),
            text=metrics_df['MAE'].round(4),
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        fig.update_layout(
            title='Mean Absolute Error (MAE)',
            xaxis_title='Model',
            yaxis_title='MAE',
            height=400,
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # RMSE and MAPE
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        colors = ['#f472b6', '#c084fc'][:len(metrics_df)]
        fig.add_trace(go.Bar(
            x=metrics_df['Model'],
            y=metrics_df['RMSE'],
            marker=dict(color=colors, line=dict(color='#ffd7ef', width=1.0)),
            text=metrics_df['RMSE'].round(4),
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        fig.update_layout(
            title='Root Mean Squared Error (RMSE)',
            xaxis_title='Model',
            yaxis_title='RMSE',
            height=400,
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'MAPE' in metrics_df.columns:
            fig = go.Figure()
            colors = ['#22c55e', '#10b981'][:len(metrics_df)]
            fig.add_trace(go.Bar(
                x=metrics_df['Model'],
                y=metrics_df['MAPE'],
                marker=dict(color=colors, line=dict(color='#bbf7d0', width=1.0)),
                text=metrics_df['MAPE'].round(2),
                textposition='auto',
                textfont=dict(color='white', size=12, family='Inter')
            ))
            fig.update_layout(
                title='Mean Absolute Percentage Error (MAPE %)',
                xaxis_title='Model',
                yaxis_title='MAPE (%)',
                height=400,
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)


def _render_detailed_analysis(models, metrics_df):
    """Render detailed analysis section"""
    st.subheader("🔍 Test Set Predictions")
    
    selected_model = st.selectbox("Select Model to Analyze", list(models.keys()))
    
    if st.button("📊 Run Test Predictions", type="primary"):
        with st.spinner("🔄 Generating predictions..."):
            try:
                data = load_train_test_data()
                
                if 'X_test' in data and 'y_test' in data:
                    X_test = data['X_test']
                    # Convert y_test to 1D array if it's a DataFrame
                    y_test = data['y_test'].iloc[:, 0].values if isinstance(data['y_test'], pd.DataFrame) else data['y_test']
                    
                    # Make prediction
                    y_pred = predict(models[selected_model], X_test)
                    
                    # Calculate metrics
                    r2 = r2_score(y_test, y_pred)
                    mae = mean_absolute_error(y_test, y_pred)
                    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("R² Score", f"{r2:.4f}")
                    col2.metric("MAE", f"{mae:.4f}")
                    col3.metric("RMSE", f"{rmse:.4f}")
                    col4.metric("MAPE", f"{mape:.2f}%")
                    
                    # Actual vs Predicted Plot
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=y_test,
                        y=y_pred,
                        mode='markers',
                        name='Predictions',
                        marker=dict(size=10, color='#667eea', opacity=0.7, line=dict(width=1, color='#4c51bf'))
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=[y_test.min(), y_test.max()],
                        y=[y_test.min(), y_test.max()],
                        mode='lines',
                        name='Perfect Prediction',
                        line=dict(color='#f5576c', dash='dash', width=3)
                    ))
                    
                    fig.update_layout(
                        title=f'{selected_model} - Actual vs Predicted Yield',
                        xaxis_title='Actual Yield (tons/ha)',
                        yaxis_title='Predicted Yield (tons/ha)',
                        height=500,
                        hovermode='closest',
                        template='plotly_dark'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Residual Plot
                    residuals = y_test - y_pred
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=y_pred,
                            y=residuals,
                            mode='markers',
                            marker=dict(size=10, color='#fa709a', opacity=0.7, line=dict(width=1, color='#f5576c'))
                        ))
                        fig.add_hline(y=0, line_dash="dash", line_color="#f5576c", line_width=2)
                        fig.update_layout(
                            title='Residual Plot',
                            xaxis_title='Predicted Values',
                            yaxis_title='Residuals',
                            height=400,
                            template='plotly_dark'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = go.Figure()
                        fig.add_trace(go.Histogram(
                            x=residuals,
                            nbinsx=30,
                            marker_color='#4facfe',
                            marker_line=dict(color='#00f2fe', width=1)
                        ))
                        fig.update_layout(
                            title='Residual Distribution',
                            xaxis_title='Residuals',
                            yaxis_title='Frequency',
                            height=400,
                            template='plotly_dark'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Save to session
                    st.session_state['predictions'] = y_pred
                    st.session_state['actual'] = y_test
                    st.session_state['selected_model'] = selected_model
                    
                    st.success("✅ Analysis complete!")
                    
                else:
                    st.error("❌ Test data not found!")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)


def _render_raw_data(metrics_df):
    """Render raw data section"""
    st.subheader("📋 Complete Metrics Table")
    st.dataframe(metrics_df, use_container_width=True)
    
    # Download metrics
    csv = metrics_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Metrics CSV",
        data=csv,
        file_name="model_metrics.csv",
        mime="text/csv",
        type="primary"
    )
