#!/usr/bin/env python3
"""
FIT to TXT Converter
Converte file .fit (Garmin/fitness) in file .txt leggibili
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import threading
from pathlib import Path

# Prova a importare fitparse
try:
    from fitparse import FitFile
except ImportError:
    print("Installazione di fitparse in corso...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fitparse", "--break-system-packages"])
    from fitparse import FitFile


class FitToTxtConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("FIT to TXT Converter")
        self.root.geometry("700x600")
        
        # Variabili
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.processing = False
        self.files_to_process = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Crea l'interfaccia grafica"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titolo
        title = ttk.Label(main_frame, text="FIT to TXT Converter", 
                         font=('Helvetica', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Selezione cartella input
        ttk.Label(main_frame, text="Cartella file .fit:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_folder, width=50).grid(row=1, column=1, pady=5, padx=5)
        ttk.Button(main_frame, text="Sfoglia", command=self.select_input_folder).grid(row=1, column=2, pady=5)
        
        # Selezione cartella output
        ttk.Label(main_frame, text="Cartella output:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=50).grid(row=2, column=1, pady=5, padx=5)
        ttk.Button(main_frame, text="Sfoglia", command=self.select_output_folder).grid(row=2, column=2, pady=5)
        
        # Checkbox per usare stessa cartella
        self.same_folder = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Salva nella stessa cartella dei file .fit", 
                       variable=self.same_folder, command=self.toggle_output_folder).grid(
                           row=3, column=0, columnspan=3, pady=10)
        
        # Frame per i pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.scan_button = ttk.Button(button_frame, text="Scansiona file", command=self.scan_files)
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.convert_button = ttk.Button(button_frame, text="Converti tutti", 
                                        command=self.start_conversion, state='disabled')
        self.convert_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Label stato
        self.status_label = ttk.Label(main_frame, text="Pronto")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Text area per log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurazione grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        # Disabilita inizialmente la selezione output
        self.toggle_output_folder()
        
    def log(self, message):
        """Aggiunge un messaggio al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def select_input_folder(self):
        """Seleziona la cartella con i file .fit"""
        folder = filedialog.askdirectory(title="Seleziona cartella con file .fit")
        if folder:
            self.input_folder.set(folder)
            if self.same_folder.get():
                self.output_folder.set(folder)
            self.log(f"Cartella input selezionata: {folder}")
            
    def select_output_folder(self):
        """Seleziona la cartella di output"""
        folder = filedialog.askdirectory(title="Seleziona cartella di output")
        if folder:
            self.output_folder.set(folder)
            self.log(f"Cartella output selezionata: {folder}")
            
    def toggle_output_folder(self):
        """Abilita/disabilita selezione cartella output"""
        if self.same_folder.get():
            self.output_folder.set(self.input_folder.get())
            # Disabilita controlli output
            for widget in self.root.grid_slaves():
                if isinstance(widget, ttk.Frame):
                    for child in widget.grid_slaves():
                        if child.grid_info()['row'] == 2 and child.grid_info()['column'] in [1, 2]:
                            child.config(state='disabled')
        else:
            # Abilita controlli output
            for widget in self.root.grid_slaves():
                if isinstance(widget, ttk.Frame):
                    for child in widget.grid_slaves():
                        if child.grid_info()['row'] == 2 and child.grid_info()['column'] in [1, 2]:
                            child.config(state='normal')
                            
    def scan_files(self):
        """Scansiona la cartella per trovare file .fit"""
        if not self.input_folder.get():
            messagebox.showwarning("Attenzione", "Seleziona prima una cartella input")
            return
            
        folder = Path(self.input_folder.get())
        self.files_to_process = list(folder.glob("*.fit")) + list(folder.glob("*.FIT"))
        
        if not self.files_to_process:
            self.log("Nessun file .fit trovato nella cartella")
            messagebox.showinfo("Info", "Nessun file .fit trovato nella cartella selezionata")
            return
            
        self.log(f"Trovati {len(self.files_to_process)} file .fit")
        self.convert_button.config(state='normal')
        self.status_label.config(text=f"Pronti {len(self.files_to_process)} file per la conversione")
        
    def start_conversion(self):
        """Avvia la conversione in un thread separato"""
        if self.processing:
            return
            
        if not self.files_to_process:
            messagebox.showwarning("Attenzione", "Scansiona prima i file")
            return
            
        # Avvia conversione in thread separato
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
        
    def convert_files(self):
        """Converte tutti i file .fit in .txt"""
        self.processing = True
        self.convert_button.config(state='disabled')
        self.scan_button.config(state='disabled')
        
        output_dir = Path(self.output_folder.get() or self.input_folder.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        total_files = len(self.files_to_process)
        successful = 0
        failed = 0
        
        self.progress['maximum'] = total_files
        
        for i, fit_file in enumerate(self.files_to_process, 1):
            self.status_label.config(text=f"Conversione {i}/{total_files}: {fit_file.name}")
            self.log(f"Conversione di {fit_file.name}...")
            
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
                        f.write("\n\nDAT LAP\n")
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
                                f.write(str(record) + "\n")
                            
                            if len(records) > 20:
                                f.write("\n... [record intermedi omessi] ...\n\n")
                                f.write("Ultimi 10 record:\n")
                                for record in records[-10:]:
                                    f.write(str(record) + "\n")
                
                self.log(f"✓ Convertito: {fit_file.name} -> {txt_file.name}")
                successful += 1
                
            except Exception as e:
                self.log(f"✗ Errore con {fit_file.name}: {str(e)}")
                failed += 1
            
            self.progress['value'] = i
            self.root.update_idletasks()
        
        # Completamento
        self.processing = False
        self.convert_button.config(state='normal')
        self.scan_button.config(state='normal')
        
        message = f"Conversione completata!\n\n✓ Successo: {successful} file\n✗ Falliti: {failed} file"
        self.status_label.config(text="Conversione completata")
        self.log(message)
        messagebox.showinfo("Completato", message)
        
        # Reset
        self.files_to_process = []
        self.progress['value'] = 0


def main():
    root = tk.Tk()
    app = FitToTxtConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
