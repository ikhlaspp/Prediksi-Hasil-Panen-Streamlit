"""
Batch Prediction View
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
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from models.model_loader import load_models
from models.data_loader import load_train_test_data


def render():
    """Render batch prediction page"""
    st.header("🤖 Batch Prediction")
    st.markdown("Upload a CSV file to predict yields for multiple samples")
    st.markdown("---")
    
    models = load_models()
    
    if not models:
        st.error("⚠️ No models found!")
        return
    
    st.info("📋 **Required columns:** Soil_Type, Crop, Rainfall_mm, Temperature_Celsius, Fertilizer_Used, Irrigation_Used, Weather_Condition, Days_to_Harvest")
    
    # Option to use test dataset
    use_test_data = st.checkbox("📊 Use Test Dataset (160 samples)", help="Automatically load X_test.csv for batch prediction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not use_test_data:
            uploaded_file = st.file_uploader("📁 Upload CSV File", type=['csv'])
        else:
            uploaded_file = None
            st.info("✓ Using test dataset: data/X_test.csv")
    
    with col2:
        selected_model = st.selectbox("🤖 Select Model", list(models.keys()))
    
    if use_test_data:
        _process_test_dataset(selected_model, models)
    elif uploaded_file is not None:
        _process_uploaded_file(uploaded_file, selected_model, models)
    else:
        _show_sample_format()


def _process_test_dataset(selected_model, models):
    """Process test dataset (160 samples)"""
    try:
        train_data = load_train_test_data()
        
        if train_data is None:
            st.error("❌ Test dataset not found. Please run split_dataset.py first.")
            return
        
        X_test = train_data['X_test']
        y_test = train_data['y_test']
        
        st.success(f"✅ Test dataset loaded: {X_test.shape[0]} rows, {X_test.shape[1]} columns")
        
        st.subheader("📋 Preview Test Data")
        preview_df = X_test.head(10).copy()
        preview_df['Actual_Yield'] = y_test[:10] if isinstance(y_test, pd.Series) else y_test[:10]
        st.dataframe(preview_df, use_container_width=True)
        
        if st.button("🚀 Run Batch Prediction on Test Data", type="primary"):
            with st.spinner("🔄 Processing predictions..."):
                try:
                    # Make predictions
                    model = models[selected_model]
                    predictions = model.predict(X_test)
                    
                    # Create results dataframe with original features
                    # Convert y_test to Series if it's a DataFrame
                    if isinstance(y_test, pd.DataFrame):
                        y_test_values = y_test.iloc[:, 0].values  # Get first column as numpy array
                    else:
                        y_test_values = y_test if isinstance(y_test, (list, pd.Series)) else y_test
                    
                    df_results = pd.DataFrame({
                        'Fertilizer_Used': X_test['Fertilizer_Used'].values,
                        'Irrigation_Used': X_test['Irrigation_Used'].values,
                        'Rainfall_mm': X_test['Rainfall_mm'].values,
                        'Temperature_Celsius': X_test['Temperature_Celsius'].values,
                        'Days_to_Harvest': X_test['Days_to_Harvest'].values,
                        'Actual_Yield': y_test_values,
                        'Predicted_Yield': predictions,
                        'Error': y_test_values - predictions,
                        'Abs_Error': abs(y_test_values - predictions)
                    })
                    
                    st.success("✅ Predictions completed!")
                    
                    # Display results
                    st.subheader("📊 Prediction Results (First 20 rows)")
                    st.dataframe(df_results.head(20), use_container_width=True)
                    
                    # Calculate metrics
                    # Convert y_test to 1D array if it's a DataFrame
                    y_true = y_test.iloc[:, 0].values if isinstance(y_test, pd.DataFrame) else y_test
                    
                    mae = mean_absolute_error(y_true, predictions)
                    rmse = np.sqrt(mean_squared_error(y_true, predictions))
                    r2 = r2_score(y_true, predictions)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Samples", len(predictions))
                    col2.metric("MAE", f"{mae:.3f}")
                    col3.metric("RMSE", f"{rmse:.3f}")
                    col4.metric("R² Score", f"{r2:.3f}")
                    
                    # Visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Actual vs Predicted
                        fig1 = go.Figure()
                        fig1.add_trace(go.Scatter(
                            x=y_test, 
                            y=predictions,
                            mode='markers',
                            marker=dict(color='#667eea', size=8, opacity=0.6),
                            name='Predictions'
                        ))
                        fig1.add_trace(go.Scatter(
                            x=[y_test.min(), y_test.max()],
                            y=[y_test.min(), y_test.max()],
                            mode='lines',
                            line=dict(color='#f87171', dash='dash', width=2),
                            name='Perfect Prediction'
                        ))
                        fig1.update_layout(
                            title='Actual vs Predicted Yield',
                            xaxis_title='Actual Yield (tons/ha)',
                            yaxis_title='Predicted Yield (tons/ha)',
                            height=400,
                            plot_bgcolor='#0f172a',
                            paper_bgcolor='#0f172a',
                            font=dict(color='#e5e7eb', family='Inter'),
                            xaxis=dict(gridcolor='#1f2937'),
                            yaxis=dict(gridcolor='#1f2937')
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        # Error distribution
                        fig2 = go.Figure()
                        fig2.add_trace(go.Histogram(
                            x=df_results['Error'],
                            nbinsx=30,
                            marker_color='#667eea',
                            marker_line=dict(color='#764ba2', width=1)
                        ))
                        fig2.update_layout(
                            title='Prediction Error Distribution',
                            xaxis_title='Error (Actual - Predicted)',
                            yaxis_title='Frequency',
                            height=400,
                            plot_bgcolor='#0f172a',
                            paper_bgcolor='#0f172a',
                            font=dict(color='#e5e7eb', family='Inter'),
                            xaxis=dict(gridcolor='#1f2937'),
                            yaxis=dict(gridcolor='#1f2937')
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    # Download results
                    csv = df_results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Test Predictions",
                        data=csv,
                        file_name=f"test_predictions_{selected_model}.csv",
                        mime="text/csv",
                        type="primary"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Prediction error: {str(e)}")
                    st.exception(e)
    
    except Exception as e:
        st.error(f"❌ Error loading test dataset: {str(e)}")
        st.exception(e)


def _process_uploaded_file(uploaded_file, selected_model, models):
    """Process uploaded CSV file"""
    try:
        # Try different separators
        try:
            df_input = pd.read_csv(uploaded_file, sep=';', decimal=',')
        except:
            df_input = pd.read_csv(uploaded_file)
        
        st.success(f"✅ File loaded: {df_input.shape[0]} rows, {df_input.shape[1]} columns")
        
        st.subheader("📋 Preview Uploaded Data")
        st.dataframe(df_input.head(10), use_container_width=True)
        
        if st.button("🚀 Run Batch Prediction", type="primary"):
            with st.spinner("🔄 Processing predictions..."):
                try:
                    # Load training columns template for one-hot alignment
                    train_data = load_train_test_data()
                    train_columns = train_data['X_train'].columns.tolist()
                    
                    # Prepare features with one-hot encoding
                    df_processed = df_input.copy()
                    
                    # Convert boolean columns to int first
                    if 'Fertilizer_Used' in df_processed.columns:
                        df_processed['Fertilizer_Used'] = df_processed['Fertilizer_Used'].astype(int)
                    if 'Irrigation_Used' in df_processed.columns:
                        df_processed['Irrigation_Used'] = df_processed['Irrigation_Used'].astype(int)
                    
                    # One-hot encode categorical columns
                    categorical_cols = [col for col in ['Soil_Type', 'Crop', 'Weather_Condition'] 
                                      if col in df_processed.columns]
                    
                    if categorical_cols:
                        df_processed = pd.get_dummies(df_processed, columns=categorical_cols, drop_first=True)
                    
                    # Align to training columns
                    for col in train_columns:
                        if col not in df_processed.columns:
                            df_processed[col] = 0
                    
                    # Keep only training columns in correct order
                    df_processed = df_processed[train_columns]
                    
                    # Make predictions
                    model = models[selected_model]
                    predictions = model.predict(df_processed)
                    
                    # Add predictions to original dataframe
                    df_results = df_input.copy()
                    df_results['Predicted_Yield'] = predictions
                    
                    st.success("✅ Predictions completed!")
                    
                    # Display results
                    st.subheader("📊 Prediction Results")
                    st.dataframe(df_results, use_container_width=True)
                    
                    # Statistics
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Predictions", len(predictions))
                    col2.metric("Avg Predicted Yield", f"{predictions.mean():.2f}")
                    col3.metric("Max Predicted Yield", f"{predictions.max():.2f}")
                    col4.metric("Min Predicted Yield", f"{predictions.min():.2f}")
                    
                    # Visualization
                    fig = go.Figure()
                    fig.add_trace(go.Histogram(
                        x=predictions,
                        nbinsx=30,
                        marker_color='#667eea',
                        marker_line=dict(color='#764ba2', width=1)
                    ))
                    fig.update_layout(
                        title='Distribution of Predicted Yields',
                        xaxis_title='Predicted Yield (tons/ha)',
                        yaxis_title='Frequency',
                        height=400,
                        plot_bgcolor='#0f172a',
                        paper_bgcolor='#0f172a',
                        font=dict(color='#e5e7eb', family='Inter'),
                        xaxis=dict(gridcolor='#1f2937'),
                        yaxis=dict(gridcolor='#1f2937')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Download results
                    csv = df_results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Predictions",
                        data=csv,
                        file_name=f"batch_predictions_{selected_model}.csv",
                        mime="text/csv",
                        type="primary"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Prediction error: {str(e)}")
                    st.exception(e)
    
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.exception(e)


def _show_sample_format():
    """Show sample file format"""
    st.markdown("### 📄 Sample File Format")
    sample_data = {
        'Soil_Type': ['Sandy', 'Clay', 'Loam'],
        'Crop': ['Rice', 'Wheat', 'Cotton'],
        'Rainfall_mm': [1000.0, 850.5, 920.3],
        'Temperature_Celsius': [25.5, 22.0, 28.3],
        'Fertilizer_Used': [True, False, True],
        'Irrigation_Used': [True, True, False],
        'Weather_Condition': ['Rainy', 'Sunny', 'Cloudy'],
        'Days_to_Harvest': [120, 110, 130]
    }
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)
    
    csv_sample = sample_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Sample Template",
        data=csv_sample,
        file_name="sample_batch_input.csv",
        mime="text/csv"
    )
