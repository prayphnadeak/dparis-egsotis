@echo off
chcp 65001 > nul
title D'PARIS Frontend
color 0B
cd /d "%~dp0"
echo.
echo  ================================================
echo    D'PARIS EGSOTIS  ^|  FRONTEND  ^|  port 5173
echo  ================================================
echo.
echo  Akses: http://%DPARIS_IP%:5173
echo.
npm run dev -- --host 0.0.0.0
