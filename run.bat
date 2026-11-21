@echo off
title FileGuard - Ultra 3D Cybersecurity Laboratory
echo =====================================================================
echo           FILEGUARD - SUSPICIOUS FILE TYPE DETECTION SYSTEM
echo =====================================================================
echo.
echo [Step 1/2] Installing required libraries (streamlit, pillow)...
python -m pip install streamlit pillow
echo.
echo [Step 2/2] Launching FileGuard 3D Application...
python -m streamlit run app.py
pause
