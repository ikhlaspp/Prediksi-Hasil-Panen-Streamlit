"""
Single Prediction View
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd
from datetime import datetime
from models.model_loader import load_models, predict
from models.data_loader import load_dataset, load_train_test_data


def render():
    """Render single prediction page"""
    st.header("🔮 Single Crop Yield Prediction")
    st.markdown("Enter farm parameters to predict crop yield")
    st.markdown("---")
    
    # Load models and training column template
    models = load_models()
    df = load_dataset()
    data_splits = load_train_test_data()
    
    if not models:
        st.error("⚠️ No models found! Please train models first.")
        return
    
    if df is None:
        st.error("⚠️ Dataset not found!")
        return

    if 'X_train' not in data_splits:
        st.error("⚠️ Training columns not found. Please retrain or ensure train splits exist.")
        return

    train_columns = data_splits['X_train'].columns.tolist()
    
    # Input Form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌾 Crop & Soil Information")
        
        soil_types = df['Soil_Type'].unique().tolist()
        soil_type = st.selectbox("🌍 Soil Type", soil_types, help="Select the type of soil")
        
        crops = df['Crop'].unique().tolist()
        crop = st.selectbox("🌱 Crop Type", crops, help="Select the type of crop")
        
        weather_conditions = df['Weather_Condition'].unique().tolist()
        weather = st.selectbox("☁️ Weather Condition", weather_conditions, 
                               help="Select weather condition")
        
        fertilizer = st.radio("🧪 Fertilizer Used?", [True, False], 
                             format_func=lambda x: "Yes" if x else "No")
        
        irrigation = st.radio("💧 Irrigation Used?", [True, False],
                             format_func=lambda x: "Yes" if x else "No")
    
    with col2:
        st.subheader("📊 Environmental Parameters")
        
        rainfall = st.slider("🌧️ Rainfall (mm)", 
                            min_value=float(df['Rainfall_mm'].min()),
                            max_value=float(df['Rainfall_mm'].max()),
                            value=float(df['Rainfall_mm'].mean()),
                            help="Annual rainfall in millimeters")
        
        temperature = st.slider("🌡️ Temperature (°C)", 
                               min_value=float(df['Temperature_Celsius'].min()),
                               max_value=float(df['Temperature_Celsius'].max()),
                               value=float(df['Temperature_Celsius'].mean()),
                               help="Average temperature in Celsius")
        
        days = st.slider("📅 Days to Harvest", 
                        min_value=int(df['Days_to_Harvest'].min()),
                        max_value=int(df['Days_to_Harvest'].max()),
                        value=int(df['Days_to_Harvest'].mean()),
                        help="Number of days until harvest")
    
    st.markdown("---")
    
    # Model Selection
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_model = st.selectbox("🤖 Select Model for Prediction", 
                                      list(models.keys()),
                                      help="Choose the ML model for prediction")
    with col2:
        st.markdown("##")
        predict_button = st.button("🚀 Predict Yield", type="primary", use_container_width=True)
    
    if predict_button:
        try:
            with st.spinner("🔄 Making prediction..."):
                # Build a one-hot row aligned to training columns
                row = {col: 0 for col in train_columns}

                # Helper to set one-hot if the column exists
                def _set_one_hot(prefix: str, value: str):
                    col_name = f"{prefix}_{value}"
                    if col_name in row:
                        row[col_name] = 1

                _set_one_hot("Soil_Type", soil_type)
                _set_one_hot("Crop", crop)
                _set_one_hot("Weather_Condition", weather)

                # Set numeric / boolean columns if present
                if 'Rainfall_mm' in row:
                    row['Rainfall_mm'] = rainfall
                if 'Temperature_Celsius' in row:
                    row['Temperature_Celsius'] = temperature
                if 'Days_to_Harvest' in row:
                    row['Days_to_Harvest'] = days
                if 'Fertilizer_Used' in row:
                    row['Fertilizer_Used'] = int(fertilizer)
                if 'Irrigation_Used' in row:
                    row['Irrigation_Used'] = int(irrigation)

                features = pd.DataFrame([row], columns=train_columns)
                
                # Make prediction
                prediction = predict(models[selected_model], features)[0]
                
                # Display Results
                st.markdown("---")
                st.success("✅ Prediction Complete!")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(37,99,235,0.92) 0%, rgba(124,58,237,0.92) 100%); 
                                padding: 3rem; border-radius: 22px; text-align: center; color: white;
                                border: 1px solid rgba(255,255,255,0.15);
                                box-shadow: 0 26px 65px rgba(124,58,237,0.35);
                                backdrop-filter: blur(14px);'>
                        <h2 style="color:#f0f9ff;">🌾 Predicted Yield</h2>
                        <h1 style='font-size: 4rem; margin: 1rem 0; background: linear-gradient(135deg, #93c5fd 0%, #a78bfa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{prediction:.2f}</h1>
                        <h3 style="color:#e0f2fe;">tons/hectare</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("##")
                
                # Input Summary
                with st.expander("📋 View Input Summary"):
                    summary_col1, summary_col2 = st.columns(2)
                    with summary_col1:
                        st.markdown(f"""
                        **🌾 Crop Information:**
                        - Soil Type: `{soil_type}`
                        - Crop: `{crop}`
                        - Weather: `{weather}`
                        - Fertilizer: `{'Yes' if fertilizer else 'No'}`
                        - Irrigation: `{'Yes' if irrigation else 'No'}`
                        """)
                    with summary_col2:
                        st.markdown(f"""
                        **📊 Environmental Data:**
                        - Rainfall: `{rainfall:.2f} mm`
                        - Temperature: `{temperature:.2f} °C`
                        - Days to Harvest: `{days} days`
                        - Model Used: `{selected_model}`
                        """)
                
                # Save prediction history
                if 'prediction_history' not in st.session_state:
                    st.session_state['prediction_history'] = []
                
                st.session_state['prediction_history'].append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'model': selected_model,
                    'prediction': prediction,
                    'inputs': {
                        'soil': soil_type,
                        'crop': crop,
                        'weather': weather,
                        'rainfall': rainfall,
                        'temperature': temperature,
                        'fertilizer': fertilizer,
                        'irrigation': irrigation,
                        'days': days
                    }
                })
                
        except Exception as e:
            st.error(f"❌ Prediction Error: {str(e)}")
            st.exception(e)
