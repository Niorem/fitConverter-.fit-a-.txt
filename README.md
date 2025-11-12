# FIT to TXT Converter

Applicazione per convertire in batch file .fit (Garmin/Fitness) in file di testo leggibili.

## Caratteristiche

- ✅ Conversione batch di centinaia di file .fit simultaneamente
- ✅ Interfaccia grafica semplice e intuitiva
- ✅ Estrazione completa dei dati: sessione, lap, punti GPS, potenza, HR, cadenza, ecc.
- ✅ Log dettagliato delle operazioni
- ✅ Progress bar per monitorare l'avanzamento

## Installazione

### Requisiti
- Python 3.7 o superiore
- pip (gestore pacchetti Python)

### Installazione dipendenze

```bash
pip install fitparse --break-system-packages
```

O usando il file requirements:

```bash
pip install -r requirements.txt --break-system-packages
```

## Utilizzo

1. **Avviare l'applicazione:**
   ```bash
   python fit_to_txt_converter.py
   ```
   
   Oppure rendila eseguibile:
   ```bash
   chmod +x fit_to_txt_converter.py
   ./fit_to_txt_converter.py
   ```

2. **Seleziona la cartella con i file .fit:**
   - Clicca su "Sfoglia" accanto a "Cartella file .fit"
   - Seleziona la cartella contenente i tuoi file .fit

3. **Scegli dove salvare i file convertiti:**
   - Di default, i file .txt saranno salvati nella stessa cartella dei .fit
   - Puoi deselezionare "Salva nella stessa cartella" per scegliere una cartella diversa

4. **Scansiona i file:**
   - Clicca su "Scansiona file" per vedere quanti file .fit sono stati trovati

5. **Avvia la conversione:**
   - Clicca su "Converti tutti" per iniziare
   - La progress bar mostrerà l'avanzamento
   - Il log mostrerà i dettagli di ogni conversione

## Formato output

Ogni file .txt conterrà:

### Informazioni Sessione
- Data e ora dell'attività
- Durata totale
- Distanza
- Velocità media e massima
- Frequenza cardiaca media e massima
- Potenza media e massima (se disponibile)
- Cadenza media
- Calorie bruciate
- Tipo di sport

### Dati Lap
- Informazioni dettagliate per ogni lap/giro
- Tempi parziali
- Distanze
- Metriche di performance

### Punti dati registrati
- Timestamp di ogni punto
- Posizione GPS (lat/lon)
- Altitudine
- Frequenza cardiaca
- Potenza
- Cadenza
- Velocità
- Temperatura
- Altri sensori disponibili

## Troubleshooting

### Errore: "No module named 'fitparse'"
L'app proverà ad installare automaticamente fitparse. Se fallisce, installalo manualmente:
```bash
pip install fitparse --break-system-packages
```

### File .fit non riconosciuti
Assicurati che i file abbiano estensione .fit o .FIT e che non siano corrotti.

### Conversione lenta
La conversione di file molto grandi (>10MB) può richiedere tempo. L'app processa i file uno alla volta per evitare problemi di memoria.

## Note tecniche

- L'app usa la libreria `fitparse` per decodificare il formato binario FIT
- I file originali .fit non vengono modificati
- I file .txt di output sono in formato UTF-8
- Per file con molti punti dati (attività lunghe), vengono mostrati solo i primi e ultimi 10 record per mantenere il file leggibile

## Esempio di utilizzo per ciclisti

Perfetto per:
- Archiviare le tue uscite in un formato leggibile
- Analizzare i dati con altri strumenti
- Condividere informazioni senza bisogno di software specifici
- Backup dei dati in formato testo

## Licenza

Uso libero per scopi personali e commerciali.
