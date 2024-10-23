@echo off

echo ===========================
echo RUNNING FASTAPI BACKEND
echo ===========================

set dir_venv=venv

IF exist %dir_venv% (
    echo ... A VIRTUAL ENVIRONMENT ALREADY EXISTS
) ELSE (
    echo ... BUILDING VIRTUAL ENVIRONMENT
    CALL python -m venv %dir_venv%
)

echo ... ACTIVATING VIRTUAL ENVIRONMENT
CALL %dir_venv%\Scripts\activate.bat

echo ... INSTALLING DEPENDENCIES
pip install -r requirements.txt

echo ===========================
echo STARTING FASTAPI SERVER
echo ===========================
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000