# Developer Guide - Crop Yield Prediction System

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [View Development](#view-development)
5. [Component Development](#component-development)
6. [Styling Guide](#styling-guide)
7. [Best Practices](#best-practices)

## 🎯 Project Overview

This is a machine learning web application for predicting crop yields built with:
- **Framework**: Streamlit
- **ML Models**: Decision Tree, Random Forest, XGBoost, LightGBM
- **Architecture**: MVC (Model-View-Controller)
- **Visualization**: Plotly, Matplotlib
- **Explainability**: SHAP

## 🏗️ Architecture

### MVC Pattern

```
User Request → Sidebar → app_mvc.py (Controller) → View → Components → Response
                                    ↓
                                  Models
                                    ↓
                              Data/ML Models
```

### Layer Responsibilities

1. **Views** (`src/views/`)
   - Handle page rendering
   - Manage user interactions
   - Display data and results
   - No business logic

2. **Models** (`src/models/`)
   - Load ML models
   - Load datasets
   - Handle predictions
   - Data processing

3. **Components** (`src/components/`)
   - Reusable UI elements
   - Sidebar navigation
   - Card components
   - No business logic

4. **Utils** (`src/utils/`)
   - Helper functions
   - Styling utilities
   - Common calculations

5. **Config** (`src/config/`)
   - Application settings
   - Constants
   - Paths

## 📁 File Structure

```
Final-Project-Machine-Learning/
├── src/
│   ├── app_mvc.py              # Main controller
│   ├── app.py                  # Legacy (preserved)
│   │
│   ├── config/
│   │   └── settings.py         # App configuration
│   │
│   ├── models/
│   │   ├── model_loader.py     # ML model loading
│   │   └── data_loader.py      # Dataset loading
│   │
│   ├── views/                  # Page views
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── single_prediction.py
│   │   ├── model_performance.py
│   │   ├── shap_analysis.py
│   │   ├── data_visualization.py
│   │   ├── batch_prediction.py
│   │   └── model_comparison.py
│   │
│   ├── components/             # Reusable components
│   │   ├── sidebar.py
│   │   └── cards.py
│   │
│   └── utils/                  # Utilities
│       ├── styling.py
│       └── helpers.py
│
├── data/                       # Datasets
│   ├── dataset_800.csv
│   ├── X_train.csv, X_test.csv
│   └── y_train.csv, y_test.csv
│
├── models/                     # Trained models
│   ├── xgboost_model.json
│   ├── lightgbm_model.txt
│   └── model_comparison.csv
│
└── notebooks/                  # Jupyter notebooks
    ├── EDA_Preprocessing.ipynb
    ├── Baseline_Model.ipynb
    └── Final_Model_XGBoost.ipynb
```

## 🎨 View Development

### Creating a New View

1. **Create View File** (`src/views/my_view.py`)

```python
"""
My View - Description
"""
import streamlit as st
from models.model_loader import load_models
from models.data_loader import load_dataset
from components.cards import gradient_card

def render():
    """Main render function"""
    st.header("📊 My View Title")
    st.markdown("Description of this view")
    st.markdown("---")
    
    # Your view logic here
    _render_content()

def _render_content():
    """Private function for rendering content"""
    # Implementation
    pass
```

2. **Update `views/__init__.py`**

```python
from . import my_view

__all__ = ['home', 'my_view', ...]
```

3. **Update `app_mvc.py` Routing**

```python
from views import my_view

# In main():
elif selected_page == "My View":
    my_view.render()
```

4. **Add to `config/settings.py`**

```python
PAGES = {
    'my_view': '📊 My View',
    # ...
}
```

### View Best Practices

✅ **DO:**
- Start function with docstring
- Use private functions (`_function_name`) for internal logic
- Use tabs for complex layouts
- Add loading spinners for long operations
- Handle errors gracefully
- Use session_state for persistence

❌ **DON'T:**
- Put business logic in views
- Duplicate code
- Use global variables
- Mix rendering and data processing
- Hardcode values

### View Template

```python
"""
View Name - Description
"""
import streamlit as st
from models.model_loader import load_models
from models.data_loader import load_dataset
from components.cards import gradient_card
from utils.helpers import format_number


def render():
    """Render [view name] page"""
    st.header("📊 Page Title")
    st.markdown("Page description")
    st.markdown("---")
    
    # Load data
    data = load_dataset()
    
    if data is None:
        st.error("⚠️ Data not available")
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    
    with tab1:
        _render_tab1(data)
    
    with tab2:
        _render_tab2(data)
    
    with tab3:
        _render_tab3(data)


def _render_tab1(data):
    """Render first tab"""
    st.subheader("Section Title")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Metric 1", "Value 1")
    col2.metric("Metric 2", "Value 2")
    col3.metric("Metric 3", "Value 3")
    
    # Content
    gradient_card("Title", "Content")


def _render_tab2(data):
    """Render second tab"""
    pass


def _render_tab3(data):
    """Render third tab"""
    pass
```

## 🧩 Component Development

### Creating Reusable Components

**File**: `src/components/my_component.py`

```python
"""
My Component - Description
"""
import streamlit as st

def my_component(title, content, **kwargs):
    """
    Display a custom component
    
    Args:
        title: Component title
        content: Component content
        **kwargs: Additional options
    """
    with st.container():
        st.markdown(f"### {title}")
        st.write(content)
```

### Component Guidelines

1. **Single Responsibility**: One component = one purpose
2. **Reusable**: Works in different contexts
3. **Customizable**: Accept parameters for customization
4. **Documented**: Clear docstrings
5. **Type Hints**: Use type annotations

### Example: Card Component

```python
def gradient_card(
    title: str,
    content: str,
    gradient: str = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
) -> None:
    """
    Display a card with gradient background
    
    Args:
        title: Card title
        content: Card content (supports markdown)
        gradient: CSS gradient string
    """
    st.markdown(f"""
    <div style="
        background: {gradient};
        padding: 20px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)
```

## 🎨 Styling Guide

### Color Scheme

```python
# Primary Colors
PRIMARY = "#667eea"
SECONDARY = "#764ba2"

# Gradients
GRADIENT_PURPLE = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
GRADIENT_BLUE = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
GRADIENT_GREEN = "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
GRADIENT_ORANGE = "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
```

### Typography

```css
font-family: 'Poppins', sans-serif;
```

### Component Styles

```python
def styled_button(label, key=None):
    """Create a styled button"""
    st.markdown("""
    <style>
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    return st.button(label, key=key, type="primary")
```

## 💡 Best Practices

### 1. Caching

```python
@st.cache_resource
def load_models():
    """Cache models (objects)"""
    return models

@st.cache_data
def load_dataset():
    """Cache data (serializable)"""
    return df
```

### 2. Error Handling

```python
try:
    result = risky_operation()
    st.success("✅ Success!")
except FileNotFoundError:
    st.error("❌ File not found")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.exception(e)  # Show full traceback in expander
```

### 3. User Feedback

```python
with st.spinner("🔄 Processing..."):
    result = long_operation()

st.success("✅ Complete!")
st.info("💡 Tip: You can...")
st.warning("⚠️ Warning: Be careful...")
st.error("❌ Error occurred!")
```

### 4. Progress Indicators

```python
progress_bar = st.progress(0)
status_text = st.empty()

for i in range(100):
    progress_bar.progress(i + 1)
    status_text.text(f"Processing... {i+1}%")

progress_bar.empty()
status_text.empty()
```

### 5. Session State

```python
# Initialize
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Use
st.session_state['history'].append(value)

# Access
history = st.session_state['history']
```

### 6. Layout Optimization

```python
# Use columns for side-by-side
col1, col2, col3 = st.columns(3)

# Use tabs for organization
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])

# Use expanders for details
with st.expander("See details"):
    st.write("Details here")

# Use containers
with st.container():
    st.write("Grouped content")
```

## 🚀 Running the App

### Development Mode

```bash
streamlit run src/app_mvc.py
```

### Production Mode

```bash
streamlit run src/app_mvc.py --server.port=8501 --server.address=0.0.0.0
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] All pages load without errors
- [ ] Navigation works correctly
- [ ] Forms accept valid input
- [ ] Forms reject invalid input
- [ ] Predictions return results
- [ ] Charts render correctly
- [ ] Downloads work
- [ ] Session state persists
- [ ] Error messages are clear

### Unit Testing Template

```python
import pytest
from views import home

def test_render_home():
    """Test home view renders"""
    # Implementation
    pass
```

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

## 🤝 Contributing

1. Create feature branch
2. Follow naming conventions
3. Write clear docstrings
4. Test your changes
5. Update documentation
6. Submit pull request

## 📝 Code Style

- **Python**: PEP 8
- **Docstrings**: Google style
- **Type hints**: Use when possible
- **Naming**: snake_case for functions, PascalCase for classes
- **Line length**: Max 100 characters

---

**Last Updated**: December 2024
**Maintainer**: Development Team
