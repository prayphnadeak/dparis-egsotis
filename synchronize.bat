@echo off
echo =======================================================
echo Sinkronisasi Data Excel ke Database (D'Paris Egsotis)
echo =======================================================
echo.

cd /d "%~dp0backend"

echo [1/4] Mengsinkronisasi data Akomodasi...
python scripts\seed_akomodasi.py
echo.

echo [2/4] Mengsinkronisasi data Kuliner...
python scripts\seed_kuliner.py
echo.

echo [3/4] Mengsinkronisasi data Wisata...
python scripts\seed_wisata.py
echo.

echo [4/4] Mengsinkronisasi data Transportasi...
python scripts\import_transportasi.py
echo.

echo =======================================================
echo Sinkronisasi Selesai! Data terbaru sudah tersimpan.
echo =======================================================
pause
