@echo off
title FileGuard - Ultra 3D Cybersecurity Laboratory
echo =====================================================================
echo           FILEGUARD - SUSPICIOUS FILE TYPE DETECTION SYSTEM
echo =====================================================================
echo.
echo [Step 1/2] Checking Python and installing required packages...
python -m pip install -r requirements.txt
echo.
echo [Step 2/2] Launching FileGuard 3D Application on http://localhost:8501...
python -m streamlit run app.py
pause
