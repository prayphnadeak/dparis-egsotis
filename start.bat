@echo off
chcp 65001 > nul

:: ─── Deteksi IP LAN ──────────────────────────────────────────────────────────
for /f "delims=" %%i in ('powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex (Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Select-Object -First 1).ifIndex).IPAddress"') do set LOCAL_IP=%%i
if "%LOCAL_IP%"=="" set LOCAL_IP=127.0.0.1

:: ─── Simpan IP ke environment agar dibaca run_backend.bat / run_frontend.bat ─
set DPARIS_IP=%LOCAL_IP%

:: ─── Update frontend/.env ─────────────────────────────────────────────────────
(
echo # D'PARIS EGSOTIS – dibuat otomatis oleh start.bat
echo VITE_API_URL=http://%LOCAL_IP%:8001
) > "%~dp0frontend\.env"

:: ─── Buka 2 window CMD ────────────────────────────────────────────────────────
start "" cmd /k "set DPARIS_IP=%LOCAL_IP% & cd /d "%~dp0backend" & call run_backend.bat"
timeout /t 4 /nobreak > nul
start "" cmd /k "set DPARIS_IP=%LOCAL_IP% & cd /d "%~dp0frontend" & call run_frontend.bat"
