#!/usr/bin/env python3
"""
FIT to TXT Converter - Versione CLI
Converte file .fit (Garmin/fitness) in file .txt leggibili
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

# Prova a importare fitparse
try:
    from fitparse import FitFile
except ImportError:
    print("Installazione di fitparse in corso...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fitparse", "--break-system-packages"])
    from fitparse import FitFile


class FitToTxtConverterCLI:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        
    def log(self, message: str):
        """Stampa un messaggio se verbose è attivo"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def convert_file(self, fit_file: Path, output_dir: Path) -> bool:
        """
        Converte un singolo file .fit in .txt
        
        Args:
            fit_file: Path al file .fit
            output_dir: Directory dove salvare il file .txt
            
        Returns:
            True se la conversione ha successo, False altrimenti
        """
        try:
            # Leggi il file FIT
            fitfile = FitFile(str(fit_file))
            
            # Nome file output
            txt_file = output_dir / f"{fit_file.stem}.txt"
            
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"=== Conversione file FIT: {fit_file.name} ===\n")
                f.write(f"Data conversione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                # Informazioni sessione
                f.write("INFORMAZIONI SESSIONE\n")
                f.write("-" * 30 + "\n")
                
                session_data = {}
                lap_data = []
                records = []
                
                # Estrai tutti i dati
                for record in fitfile.get_messages():
                    record_dict = {}
                    
                    for field in record:
                        if field.value is not None:
                            field_name = field.name
                            field_value = field.value
                            
                            # Formatta alcuni valori speciali
                            if isinstance(field_value, datetime):
                                field_value = field_value.strftime('%Y-%m-%d %H:%M:%S')
                            
                            record_dict[field_name] = field_value
                    
                    # Categorizza i record
                    if record.name == 'session':
                        session_data = record_dict
                    elif record.name == 'lap':
                        lap_data.append(record_dict)
                    elif record.name == 'record':
                        records.append(record_dict)
                
                # Scrivi dati sessione
                if session_data:
                    for key, value in session_data.items():
                        f.write(f"{key}: {value}\n")
                
                # Scrivi dati lap
                if lap_data:
                    f.write("\n\nDATI LAP\n")
                    f.write("-" * 30 + "\n")
                    for i, lap in enumerate(lap_data, 1):
                        f.write(f"\nLap {i}:\n")
                        for key, value in lap.items():
                            f.write(f"  {key}: {value}\n")
                
                # Scrivi record (punti dati)
                if records:
                    f.write("\n\nPUNTI DATI REGISTRATI\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Totale punti: {len(records)}\n\n")
                    
                    # Scrivi intestazioni
                    if records:
                        headers = list(records[0].keys())
                        f.write("Campi disponibili: " + ", ".join(headers) + "\n\n")
                        
                        # Scrivi primi 10 e ultimi 10 record come esempio
                        f.write("Primi 10 record:\n")
                        for record in records[:10]:
                            # Formatta output più leggibile
                            formatted = []
                            for k, v in record.items():
                                if k in ['timestamp', 'position_lat', 'position_long', 'altitude', 
                                        'heart_rate', 'power', 'cadence', 'speed', 'distance']:
                                    formatted.append(f"{k}={v}")
                            f.write("  " + " | ".join(formatted) + "\n")
                        
                        if len(records) > 20:
                            f.write("\n... [record intermedi omessi] ...\n\n")
                            f.write("Ultimi 10 record:\n")
                            for record in records[-10:]:
                                formatted = []
                                for k, v in record.items():
                                    if k in ['timestamp', 'position_lat', 'position_long', 'altitude', 
                                            'heart_rate', 'power', 'cadence', 'speed', 'distance']:
                                        formatted.append(f"{k}={v}")
                                f.write("  " + " | ".join(formatted) + "\n")
            
            self.log(f"✓ Convertito: {fit_file.name} -> {txt_file.name}")
            return True
            
        except Exception as e:
            self.log(f"✗ Errore con {fit_file.name}: {str(e)}")
            return False
    
    def convert_batch(self, input_path: Path, output_path: Path = None, 
                     recursive: bool = False) -> Tuple[int, int]:
        """
        Converte file .fit in batch
        
        Args:
            input_path: Path alla cartella o file .fit
            output_path: Path alla cartella di output (opzionale)
            recursive: Se True, cerca file .fit anche nelle sottocartelle
            
        Returns:
            Tupla (successi, fallimenti)
        """
        # Se output_path non è specificato, usa la stessa cartella dell'input
        if output_path is None:
            if input_path.is_file():
                output_path = input_path.parent
            else:
                output_path = input_path
        
        # Crea cartella output se non esiste
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Trova tutti i file .fit
        fit_files = []
        if input_path.is_file() and input_path.suffix.lower() == '.fit':
            fit_files = [input_path]
        elif input_path.is_dir():
            if recursive:
                fit_files = list(input_path.rglob("*.fit")) + list(input_path.rglob("*.FIT"))
            else:
                fit_files = list(input_path.glob("*.fit")) + list(input_path.glob("*.FIT"))
        
        if not fit_files:
            self.log(f"Nessun file .fit trovato in {input_path}")
            return 0, 0
        
        self.log(f"Trovati {len(fit_files)} file .fit da convertire")
        
        successful = 0
        failed = 0
        
        for i, fit_file in enumerate(fit_files, 1):
            print(f"[{i}/{len(fit_files)}] Conversione di {fit_file.name}...", end=" ")
            
            if self.convert_file(fit_file, output_path):
                successful += 1
                print("✓")
            else:
                failed += 1
                print("✗")
        
        return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description='Converte file .fit (Garmin/Fitness) in file .txt leggibili',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  # Converti un singolo file
  %(prog)s percorso/al/file.fit
  
  # Converti tutti i file in una cartella
  %(prog)s percorso/alla/cartella/
  
  # Converti ricorsivamente (incluse sottocartelle)
  %(prog)s -r percorso/alla/cartella/
  
  # Specifica cartella di output
  %(prog)s percorso/input/ -o percorso/output/
  
  # Modalità silenziosa
  %(prog)s -q percorso/alla/cartella/
        """
    )
    
    parser.add_argument('input', type=str, 
                       help='File .fit o cartella contenente file .fit')
    parser.add_argument('-o', '--output', type=str, default=None,
                       help='Cartella di output (default: stessa cartella dell\'input)')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Cerca file .fit anche nelle sottocartelle')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Modalità silenziosa (meno output)')
    
    args = parser.parse_args()
    
    # Converti i path
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None
    
    # Verifica che l'input esista
    if not input_path.exists():
        print(f"Errore: {input_path} non esiste")
        sys.exit(1)
    
    # Crea il converter
    converter = FitToTxtConverterCLI(verbose=not args.quiet)
    
    # Esegui la conversione
    print(f"\nFIT to TXT Converter")
    print("=" * 40)
    
    successful, failed = converter.convert_batch(input_path, output_path, args.recursive)
    
    # Report finale
    print("\n" + "=" * 40)
    print("CONVERSIONE COMPLETATA")
    print(f"✓ Successo: {successful} file")
    if failed > 0:
        print(f"✗ Falliti: {failed} file")
    
    # Exit code basato sul successo
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
