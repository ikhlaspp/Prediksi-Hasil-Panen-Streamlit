#!/bin/bash
echo "========================================"
echo " Crop Yield Prediction System"
echo " Installation Script (Virtual Env)"
echo "========================================"
echo ""

echo "[1/3] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed!"
    exit 1
fi

# Membuat virtual environment jika belum ada
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Mengaktifkan venv
source .venv/bin/activate

echo ""
echo "[2/3] Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install packages!"
    exit 1
fi

echo ""
echo "[3/3] Verifying installation..." [cite: 9]
python -c "import streamlit, xgboost, lightgbm, pandas, numpy, sklearn, shap, jupyter, nbconvert, ipykernel" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "WARNING: Some packages may not be installed correctly." [cite: 9]
    exit 1
fi

echo ""
echo "[4/4] Setting up Jupyter kernel..."
python -m ipykernel install --user --name python3 --display-name "Python 3" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Could not register Jupyter kernel."
fi

echo ""
echo "========================================"
echo " Installation Complete!" [cite: 10]
echo "========================================"
