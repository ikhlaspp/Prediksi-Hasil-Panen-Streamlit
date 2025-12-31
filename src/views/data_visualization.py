"""
Data Visualization View
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
import plotly.express as px
from models.data_loader import load_dataset


def render():
    """Render data visualization page"""
    st.header("📈 Data Visualization & Exploratory Analysis")
    st.markdown("Explore the dataset with interactive visualizations")
    st.markdown("---")
    
    df = load_dataset()
    
    if df is None:
        st.error("⚠️ Dataset not found!")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Distribution", "🔗 Correlation", "📉 Feature Analysis"])
    
    with tab1:
        _render_overview(df)
    
    with tab2:
        _render_distribution(df)
    
    with tab3:
        _render_correlation(df)
    
    with tab4:
        _render_feature_analysis(df)


def _render_overview(df):
    """Render dataset overview"""
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Samples", f"{df.shape[0]:,}")
    col2.metric("Features", df.shape[1] - 1)
    col3.metric("Crops Types", df['Crop'].nunique())
    col4.metric("Soil Types", df['Soil_Type'].nunique())
    
    st.markdown("### 📋 Sample Data")
    st.dataframe(df.head(20), use_container_width=True)
    
    st.markdown("### 📊 Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)
    
    # Missing values
    st.markdown("### 🔍 Data Quality Check")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        st.success("No missing values detected across all features.")
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=missing.index,
            y=missing.values,
            marker_color='#f59e0b',
            text=missing.values,
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        fig.update_layout(
            title='Missing Values per Feature',
            xaxis_title='Feature',
            yaxis_title='Count',
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)


def _render_distribution(df):
    """Render feature distributions"""
    st.subheader("📈 Feature Distributions")

    # Yield distribution
    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df['Yield_tons_per_hectare'],
            nbinsx=30,
            marker_color='#4facfe',
            marker_line=dict(color='#00f2fe', width=1)
        ))
        fig.update_layout(
            title='Yield Distribution',
            xaxis_title='Yield (tons/hectare)',
            yaxis_title='Frequency',
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=df['Yield_tons_per_hectare'],
            marker_color='#764ba2',
            marker=dict(color='#764ba2', line=dict(color='#667eea', width=2))
        ))
        fig.update_layout(
            title='Yield Box Plot',
            yaxis_title='Yield (tons/hectare)',
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)

    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'Yield_tons_per_hectare' in numerical_cols:
        numerical_cols.remove('Yield_tons_per_hectare')

    selected_feature = st.selectbox("Select Feature to Visualize", numerical_cols)

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[selected_feature],
            nbinsx=30,
            marker_color='#4facfe',
            marker_line=dict(color='#00f2fe', width=1)
        ))
        fig.update_layout(
            title=f'{selected_feature} Distribution',
            xaxis_title=selected_feature,
            yaxis_title='Frequency',
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=df[selected_feature],
            marker_color='#fa709a',
            marker=dict(color='#fa709a', line=dict(color='#f5576c', width=2))
        ))
        fig.update_layout(
            title=f'{selected_feature} Box Plot',
            yaxis_title=selected_feature,
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)


def _render_correlation(df):
    """Render correlation analysis"""
    st.subheader("🔗 Feature Correlations")
    
    numerical_df = df.select_dtypes(include=[np.number])
    corr_matrix = numerical_df.corr()
    
    # Correlation heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10, "color": "white"}
    ))
    fig.update_layout(
        title='Feature Correlation Matrix',
        height=600,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#e5e7eb', family='Inter')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top correlations with yield
    if 'Yield_tons_per_hectare' in corr_matrix.columns:
        st.markdown("### 🎯 Correlations with Yield")
        yield_corr = corr_matrix['Yield_tons_per_hectare'].sort_values(ascending=False)[1:]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=yield_corr.values,
            y=yield_corr.index,
            orientation='h',
            marker=dict(
                color=yield_corr.values,
                colorscale='RdYlGn',
                cmid=0
            ),
            text=yield_corr.values.round(3),
            textposition='auto',
            textfont=dict(color='white', size=11, family='Inter')
        ))
        fig.update_layout(
            title='Feature Correlation with Yield',
            xaxis_title='Correlation Coefficient',
            yaxis_title='Feature',
            height=400,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)


def _render_feature_analysis(df):
    """Render yield analysis by categories"""
    st.subheader("📉 Yield Analysis by Categories")
    
    # Yield by Crop
    col1, col2 = st.columns(2)
    
    with col1:
        crop_yield = df.groupby('Crop')['Yield_tons_per_hectare'].mean().sort_values(ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=crop_yield.values,
            y=crop_yield.index,
            orientation='h',
            marker_color='#38ef7d',
            text=crop_yield.values.round(2),
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        fig.update_layout(
            title='Average Yield by Crop Type',
            xaxis_title='Average Yield (tons/ha)',
            yaxis_title='Crop',
            height=500,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        soil_yield = df.groupby('Soil_Type')['Yield_tons_per_hectare'].mean().sort_values(ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=soil_yield.values,
            y=soil_yield.index,
            orientation='h',
            marker_color='#fa709a',
            text=soil_yield.values.round(2),
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        fig.update_layout(
            title='Average Yield by Soil Type',
            xaxis_title='Average Yield (tons/ha)',
            yaxis_title='Soil Type',
            height=500,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e5e7eb', family='Inter'),
            xaxis=dict(gridcolor='#1f2937'),
            yaxis=dict(gridcolor='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Weather vs Yield
    weather_yield = df.groupby('Weather_Condition')['Yield_tons_per_hectare'].mean().sort_values(ascending=False)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=weather_yield.index,
        y=weather_yield.values,
        marker_color=['#667eea', '#764ba2', '#f093fb'],
        text=weather_yield.values.round(2),
        textposition='auto',
        textfont=dict(color='white', size=12, family='Inter')
    ))
    fig.update_layout(
        title='Average Yield by Weather Condition',
        xaxis_title='Weather Condition',
        yaxis_title='Average Yield (tons/ha)',
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#e5e7eb', family='Inter'),
        xaxis=dict(gridcolor='#1f2937'),
        yaxis=dict(gridcolor='#1f2937'),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter: Temperature vs Rainfall vs Yield
    # Create a size column with positive values only
    df_scatter = df.copy()
    df_scatter['size_col'] = df_scatter['Yield_tons_per_hectare'].abs() + 1  # Add 1 to ensure all positive
    
    fig = px.scatter(df_scatter, 
                    x='Temperature_Celsius', 
                    y='Rainfall_mm',
                    color='Yield_tons_per_hectare',
                    size='size_col',
                    hover_data=['Crop', 'Soil_Type'],
                    color_continuous_scale='Viridis',
                    title='Temperature vs Rainfall (colored by Yield)')
    fig.update_layout(
        height=500,
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#e5e7eb', family='Inter'),
        xaxis=dict(gridcolor='#1f2937'),
        yaxis=dict(gridcolor='#1f2937')
    )
    st.plotly_chart(fig, use_container_width=True)
