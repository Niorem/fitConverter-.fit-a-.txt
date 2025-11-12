@echo off
title FIT to TXT Converter
echo ===================================
echo     FIT to TXT Converter
echo ===================================
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Scarica Python da https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Installa dipendenze se necessario
echo Verifica dipendenze...
pip show fitparse >nul 2>&1
if errorlevel 1 (
    echo Installazione fitparse...
    pip install fitparse
)

REM Avvia l'applicazione
if "%1"=="" (
    REM Se non ci sono parametri, prova la versione GUI
    echo Avvio interfaccia grafica...
    python fit_to_txt_converter.py
    if errorlevel 1 (
        echo.
        echo GUI non disponibile, uso versione CLI
        echo.
        echo Uso: %0 cartella_con_file_fit
        echo.
        pause
    )
) else (
    REM Se ci sono parametri, usa la versione CLI
    python fit_to_txt_converter_cli.py %*
)

pause
