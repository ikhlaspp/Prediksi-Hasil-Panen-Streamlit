@echo off
echo ========================================
echo  Crop Yield Prediction System
echo  Installation Script
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.13 or higher from https://www.python.org/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/3] Installing required packages...
echo This may take a few minutes...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages!
    pause
    exit /b 1
)
echo.

echo [3/3] Verifying installation...
python -c "import streamlit, xgboost, lightgbm, pandas, numpy, sklearn, shap, jupyter, nbconvert, ipykernel" 2>nul
if errorlevel 1 (
    echo WARNING: Some packages may not be installed correctly.
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo.

echo [4/4] Setting up Jupyter kernel...
python -m ipykernel install --user --name python3 --display-name "Python 3" 2>nul
if errorlevel 1 (
    echo WARNING: Could not register Jupyter kernel.
)
echo.

echo ========================================
echo  Installation Complete! 
echo ========================================
echo.
echo You can now run the application using:
echo   run.bat
echo.
echo Or manually with:
echo   streamlit run src/app.py
echo.
pause
