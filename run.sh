#!/bin/bash
echo "========================================"
echo " Crop Yield Prediction System"
echo "========================================"

# Check if mode is specified
MODE=${1:-app}

if [ "$MODE" = "notebook" ]; then
    echo " Starting Jupyter Notebook..."
elif [ "$MODE" = "execute" ]; then
    echo " Executing Jupyter Notebooks..."
elif [ "$MODE" = "app" ]; then
    echo " Starting Application with Notebooks..."
else
    echo "Usage: $0 [app|notebook|execute]"
    echo "  app      - Start Streamlit application with notebooks (default)"
    echo "  notebook - Start Jupyter Notebook server"
    echo "  execute  - Execute all Jupyter notebooks"
    exit 1
fi
echo "========================================"

# Memastikan folder venv ada
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

# Mengaktifkan venv
source .venv/bin/activate

if [ "$MODE" = "notebook" ] || [ "$MODE" = "execute" ]; then
    echo "Checking if Jupyter and nbconvert are installed..."
    python -c "import jupyter, nbconvert, ipykernel" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "ERROR: Jupyter, nbconvert, or ipykernel is not installed!"
        echo "Please install with: pip install jupyter nbconvert ipykernel"
        exit 1
    fi

    if [ "$MODE" = "notebook" ]; then
        echo "Starting Jupyter Notebook server..."
        echo "The notebook will open in your browser."
        echo "Press Ctrl+C to stop."
    else
        echo "Executing notebooks in sequence..."
        echo "========================================"
        echo ""
    fi
elif [ "$MODE" = "app" ]; then
    echo "Checking if packages are installed..."
    python -c "import streamlit, jupyter, nbconvert, ipykernel" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "ERROR: Required packages (streamlit, jupyter, nbconvert, ipykernel) are not installed!"
        echo "Please run ./install.sh first."
        exit 1
    fi

    echo "Executing notebooks first..."
    echo "========================================"
    echo ""
fi

# FIX: Menambahkan direktori saat ini ke PYTHONPATH agar folder 'models' terbaca
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}"

# Menjalankan aplikasi atau notebook dari root directory
if [ "$MODE" = "notebook" ]; then
    jupyter notebook
elif [ "$MODE" = "execute" ]; then
    echo "[1/3] Executing EDA_Preprocessing.ipynb..."
    jupyter nbconvert --execute --to notebook --inplace notebooks/EDA_Preprocessing.ipynb
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to execute EDA_Preprocessing.ipynb"
        exit 1
    fi
    echo "EDA_Preprocessing.ipynb executed successfully!"
    echo ""

    echo "[2/3] Executing Baseline_Model.ipynb..."
    jupyter nbconvert --execute --to notebook --inplace notebooks/Baseline_Model.ipynb
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to execute Baseline_Model.ipynb"
        exit 1
    fi
    echo "Baseline_Model.ipynb executed successfully!"
    echo ""

    echo "[3/3] Executing Final_Model_XGBoost.ipynb..."
    jupyter nbconvert --execute --to notebook --inplace notebooks/Final_Model_XGBoost.ipynb
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to execute Final_Model_XGBoost.ipynb"
        exit 1
    fi
    echo "Final_Model_XGBoost.ipynb executed successfully!"
    echo ""

    echo "========================================"
    echo "All notebooks executed successfully!"
    echo "========================================"
elif [ "$MODE" = "app" ]; then
    # Execute notebooks first
    echo "[1/3] Executing EDA_Preprocessing.ipynb..."
    jupyter nbconvert --execute --to notebook --inplace notebooks/EDA_Preprocessing.ipynb
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to execute EDA_Preprocessing.ipynb"
        exit 1
    fi
    echo "EDA_Preprocessing.ipynb executed successfully!"
    echo ""

    echo "[2/3] Executing Baseline_Model.ipynb..."
    jupyter nbconvert --execute --to notebook --inplace notebooks/Baseline_Model.ipynb
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to execute Baseline_Model.ipynb"
        exit 1
    fi
    echo "Baseline_Model.ipynb executed successfully!"
    echo ""

    echo "[3/3] Executing Final_Model_XGBoost.ipynb..."
    jupyter nbconvert --execute --to notebook --inplace notebooks/Final_Model_XGBoost.ipynb
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to execute Final_Model_XGBoost.ipynb"
        exit 1
    fi
    echo "Final_Model_XGBoost.ipynb executed successfully!"
    echo ""

    echo "========================================"
    echo "Notebooks executed successfully!"
    echo "Starting Streamlit application..."
    echo "========================================"
    echo "URL: http://localhost:8501"
    echo "Press Ctrl+C to stop."

    streamlit run src/app.py
fi
