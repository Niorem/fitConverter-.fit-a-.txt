#!/bin/bash

echo "==================================="
echo "     FIT to TXT Converter"
echo "==================================="
echo

# Verifica se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "ERRORE: Python3 non trovato!"
    echo "Installa Python3 con il tuo package manager"
    exit 1
fi

# Verifica/installa dipendenze
echo "Verifica dipendenze..."
if ! python3 -c "import fitparse" 2>/dev/null; then
    echo "Installazione fitparse..."
    pip3 install fitparse --break-system-packages || pip3 install fitparse
fi

# Se non ci sono parametri, prova la versione GUI
if [ $# -eq 0 ]; then
    echo "Avvio interfaccia grafica..."
    python3 fit_to_txt_converter.py 2>/dev/null
    
    # Se la GUI fallisce, mostra info per CLI
    if [ $? -ne 0 ]; then
        echo
        echo "GUI non disponibile (manca tkinter)"
        echo "Usa la versione CLI:"
        echo
        echo "Esempi:"
        echo "  $0 file.fit                    # Converti un file"
        echo "  $0 cartella/                   # Converti tutti i file in una cartella"
        echo "  $0 -r cartella/                # Converti ricorsivamente"
        echo "  $0 cartella/ -o output/        # Specifica cartella output"
        echo
        echo "Per help completo: python3 fit_to_txt_converter_cli.py --help"
    fi
else
    # Usa la versione CLI con i parametri passati
    python3 fit_to_txt_converter_cli.py "$@"
fi
