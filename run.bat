@echo off
echo Starting AI Startup Idea Generator...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Streamlit application...
echo.
echo The application will open in your default browser.
echo Press Ctrl+C to stop the application.
echo.
streamlit run app.py
pause
