@echo off

REM Start backend server

cd backend
call venv\Scripts\activate
python main.py
