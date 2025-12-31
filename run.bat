@echo off
echo ========================================
echo  Crop Yield Prediction System
echo ========================================
echo.

set MODE=%1
if "%MODE%"=="" set MODE=app

if "%MODE%"=="notebook" (
    echo  Starting Jupyter Notebook...
) else if "%MODE%"=="execute" (
    echo  Executing Jupyter Notebooks...
) else if "%MODE%"=="app" (
    echo  Starting Application with Notebooks...
) else (
    echo Usage: run.bat [app^|notebook^|execute]
    echo   app      - Start Streamlit application with notebooks ^(default^)
    echo   notebook - Start Jupyter Notebook server
    echo   execute  - Execute all Jupyter notebooks
    echo.
    pause
    exit /b 1
)
echo ========================================
echo.

if "%MODE%"=="notebook" (
    echo Checking if Jupyter and nbconvert are installed...
    python -c "import jupyter, nbconvert, ipykernel" 2>nul
    if errorlevel 1 (
        echo ERROR: Jupyter, nbconvert, or ipykernel is not installed!
        echo Please install with: pip install jupyter nbconvert ipykernel
        echo.
        pause
        exit /b 1
    )

    echo Starting Jupyter Notebook server...
    echo.
    echo The notebook will open in your browser automatically.
    echo.
    echo Press Ctrl+C to stop the server.
    echo ========================================
    echo.

    REM FIX: Add current directory to PYTHONPATH so models module can be found
    for %%i in ("%~dp0.") do set "SCRIPT_DIR=%%~fi"
    set PYTHONPATH=%PYTHONPATH%;%SCRIPT_DIR%

    jupyter notebook

    if errorlevel 1 (
        echo.
        echo ERROR: Failed to start Jupyter Notebook!
        echo Please check the error messages above.
        echo.
        pause
    )
) else if "%MODE%"=="execute" (
    echo Checking if Jupyter and nbconvert are installed...
    python -c "import jupyter, nbconvert, ipykernel" 2>nul
    if errorlevel 1 (
        echo ERROR: Jupyter, nbconvert, or ipykernel is not installed!
        echo Please install with: pip install jupyter nbconvert ipykernel
        echo.
        pause
        exit /b 1
    )

    echo Executing notebooks in sequence...
    echo ========================================
    echo.

    REM FIX: Add current directory to PYTHONPATH so models module can be found
    for %%i in ("%~dp0.") do set "SCRIPT_DIR=%%~fi"
    set PYTHONPATH=%PYTHONPATH%;%SCRIPT_DIR%

    echo [1/3] Executing EDA_Preprocessing.ipynb...
    echo.
    jupyter nbconvert --execute --to notebook --inplace notebooks/EDA_Preprocessing.ipynb
    if errorlevel 1 (
        echo ERROR: Failed to execute EDA_Preprocessing.ipynb
        pause
        exit /b 1
    )
    echo EDA_Preprocessing.ipynb executed successfully!
    echo.

    echo [2/3] Executing Baseline_Model.ipynb...
    echo.
    jupyter nbconvert --execute --to notebook --inplace notebooks/Baseline_Model.ipynb
    if errorlevel 1 (
        echo ERROR: Failed to execute Baseline_Model.ipynb
        pause
        exit /b 1
    )
    echo Baseline_Model.ipynb executed successfully!
    echo.

    echo [3/3] Executing Final_Model_XGBoost.ipynb...
    echo.
    jupyter nbconvert --execute --to notebook --inplace notebooks/Final_Model_XGBoost.ipynb
    if errorlevel 1 (
        echo ERROR: Failed to execute Final_Model_XGBoost.ipynb
        pause
        exit /b 1
    )
    echo Final_Model_XGBoost.ipynb executed successfully!
    echo.

    echo ========================================
    echo All notebooks executed successfully!
    echo ========================================
    echo.
    pause
) else (
    echo Checking if packages are installed...
    python -c "import streamlit, jupyter, nbconvert, ipykernel" 2>nul
    if errorlevel 1 (
        echo ERROR: Required packages ^(streamlit, jupyter, nbconvert, ipykernel^) are not installed!
        echo Please run install.bat first.
        echo.
        pause
        exit /b 1
    )

    echo Executing notebooks first...
    echo ========================================
    echo.

    REM FIX: Add current directory to PYTHONPATH so models module can be found
    for %%i in ("%~dp0.") do set "SCRIPT_DIR=%%~fi"
    set PYTHONPATH=%PYTHONPATH%;%SCRIPT_DIR%

    echo [1/3] Executing EDA_Preprocessing.ipynb...
    echo.
    jupyter nbconvert --execute --to notebook --inplace notebooks/EDA_Preprocessing.ipynb
    if errorlevel 1 (
        echo ERROR: Failed to execute EDA_Preprocessing.ipynb
        pause
        exit /b 1
    )
    echo EDA_Preprocessing.ipynb executed successfully!
    echo.

    echo [2/3] Executing Baseline_Model.ipynb...
    echo.
    jupyter nbconvert --execute --to notebook --inplace notebooks/Baseline_Model.ipynb
    if errorlevel 1 (
        echo ERROR: Failed to execute Baseline_Model.ipynb
        pause
        exit /b 1
    )
    echo Baseline_Model.ipynb executed successfully!
    echo.

    echo [3/3] Executing Final_Model_XGBoost.ipynb...
    echo.
    jupyter nbconvert --execute --to notebook --inplace notebooks/Final_Model_XGBoost.ipynb
    if errorlevel 1 (
        echo ERROR: Failed to execute Final_Model_XGBoost.ipynb
        pause
        exit /b 1
    )
    echo Final_Model_XGBoost.ipynb executed successfully!
    echo.

    echo ========================================
    echo Notebooks executed successfully!
    echo Starting Streamlit application...
    echo ========================================
    echo.
    echo The app will open in your browser automatically.
    echo If not, open: http://localhost:8501
    echo.
    echo Press Ctrl+C to stop the server.
    echo ========================================
    echo.

    REM FIX: Add current directory to PYTHONPATH so models module can be found
    for %%i in ("%~dp0.") do set "SCRIPT_DIR=%%~fi"
    set PYTHONPATH=%PYTHONPATH%;%SCRIPT_DIR%

    streamlit run src/app.py

    if errorlevel 1 (
        echo.
        echo ERROR: Failed to start the application!
        echo Please check the error messages above.
        pause
    )
)
