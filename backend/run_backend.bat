@echo off
chcp 65001 > nul
title D'PARIS Backend
color 0A
cd /d "%~dp0"
echo.
echo  ================================================
echo    D'PARIS EGSOTIS  ^|  BACKEND  ^|  port 8001
echo  ================================================
echo.
echo  Akses: http://%DPARIS_IP%:8001
echo  Docs : http://%DPARIS_IP%:8001/docs
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
