# 🌾 Crop Yield Prediction System

> **An intelligent agricultural prediction platform powered by Machine Learning**

Predict crop yields based on environmental and agricultural factors with high accuracy. This system helps farmers and agricultural planners make data-driven decisions.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52-red.svg)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.1-green.svg)](https://xgboost.ai/)

---

## 🎯 What Does This Do?

This system predicts **crop yield (tons per hectare)** based on:
- 🌧️ **Rainfall** (mm)
- 🌡️ **Temperature** (°C)
- 🌱 **Soil Type** (Clay, Loam, Sandy)
- 🌾 **Crop Type** (Rice, Wheat, Cotton, etc.)
- 🧪 **Fertilizer Usage** (Yes/No)
- 💧 **Irrigation** (Yes/No)
- ⛅ **Weather Conditions** (Sunny, Rainy, Cloudy)
- 📅 **Days to Harvest**

**Result:** Get accurate yield predictions to optimize your farming strategy! 🚜

---

## ✨ Features

### 🔮 Single Prediction
Enter farm parameters and get instant yield predictions with confidence scores.

### 🤖 Batch Prediction
Upload a CSV file with multiple farm scenarios and get predictions for all at once.

### 📊 Data Visualization
Explore interactive charts showing:
- Feature correlations
- Yield distributions
- Historical trends

### ⚖️ Model Comparison
Compare performance of different ML algorithms:
- Decision Tree
- Random Forest
- **XGBoost** (Best performer! 🏆)
- LightGBM

### 🔍 SHAP Analysis
Understand **why** the model makes predictions:
- Feature importance rankings
- Impact of each factor on yield
- Transparent AI explanations

### 📈 Model Performance Dashboard
Track accuracy metrics:
- R² Score
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

---

## 🚀 Quick Start

### 🪟 Windows Users (Easiest Way!)

**Just double-click these files:**

1. **`install.bat`** - Installs all dependencies automatically
2. **`run.bat`** - Starts the application

**That's it!** 🎉 The app will open in your browser at `http://localhost:8501`

---

### 🐧 Manual Installation (All Platforms)

#### Step 1: Install Python
Make sure you have **Python 3.13+** installed.

Check your version:
```bash
python --version
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install all necessary libraries automatically.

#### Step 3: Run the App
```bash
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 User Guide

### Making Your First Prediction

1. **Open the app** in your browser
2. Navigate to **"Single Prediction"** page
3. Fill in the form:
   - Select your soil type
   - Choose your crop
   - Enter rainfall amount (mm)
   - Enter temperature (°C)
   - Select fertilizer usage
   - Select irrigation status
   - Choose weather condition
   - Enter days to harvest
4. Click **"Predict Yield"**
5. See your result instantly! 📊

### Batch Predictions

1. Go to **"Batch Prediction"** page
2. **Option 1:** Click "Use Test Dataset" to try with sample data
3. **Option 2:** Upload your own CSV file
   - Download the sample template first
   - Fill in your data
   - Upload the file
4. Click **"Run Batch Prediction"**
5. Download results as CSV

---

## 🗂️ Project Structure

```
📦 Final-Project-Machine-Learning/
├── 📂 data/                    # Training and test datasets
│   ├── dataset_800.csv         # Original 800 samples
│   ├── X_train.csv            # Training features (640 samples)
│   ├── X_test.csv             # Test features (160 samples)
│   ├── y_train.csv            # Training targets
│   └── y_test.csv             # Test targets
│
├── 📂 notebooks/               # Jupyter notebooks for analysis
│   ├── EDA_Preprocessing.ipynb          # Data exploration
│   ├── Baseline_Model.ipynb             # Baseline modeling
│   └── Final_Model_XGBoost.ipynb        # Final model training
│
├── 📂 models/                  # Trained ML models
│   ├── xgboost_model.json     # XGBoost (Best model!)
│   ├── lightgbm_model.txt     # LightGBM
│   ├── random_forest.pkl      # Random Forest
│   └── decision_tree.pkl      # Decision Tree
│
├── 📂 src/                     # Application source code
│   ├── app.py                 # Main Streamlit app
│   ├── 📂 models/              # Data and model loaders
│   ├── 📂 views/               # UI pages
│   ├── 📂 components/          # Reusable UI components
│   └── 📂 config/              # Settings and configurations
│
├── requirements.txt           # Python dependencies
└── README.md                  # You are here! 📍
```

---

## 📊 Model Performance

Our best model achieves:
- ✅ **R² Score:** ~0.95+ (Excellent!)
- ✅ **MAE:** <0.5 tons/ha
- ✅ **RMSE:** <0.7 tons/ha

These metrics mean the predictions are highly accurate and reliable for real-world use.

---

## 🎓 For Developers

Want to understand the code or contribute?

👉 See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for:
- Architecture details
- Code organization
- Development workflow
- API documentation
- How to add new features

---

## 🛠️ Technologies Used

- **Python 3.13** - Programming language
- **Streamlit** - Web interface
- **XGBoost** - Best ML algorithm
- **LightGBM** - Fast gradient boosting
- **scikit-learn** - ML utilities
- **SHAP** - Model explainability
- **pandas** - Data processing
- **Plotly** - Interactive charts

---

## ❓ Troubleshooting

### App won't start?
```bash
# Try this instead:
python -m streamlit run src/app.py
```

### Missing packages?
```bash
# Reinstall all dependencies:
pip install -r requirements.txt --upgrade
```

### Model files not found?
Make sure you're running the app from the project root directory:
```bash
cd Final-Project-Machine-Learning
streamlit run src/app.py
```

---

## 🤝 Support

Need help? Have questions?
- Check the [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- Review the Jupyter notebooks in `notebooks/` folder
- Check the code documentation in source files

---

## 📝 License

This project is developed for academic purposes.

---

## 🌟 Acknowledgments

Built with ❤️ for Machine Learning coursework.

**Happy Predicting! 🌾✨**
