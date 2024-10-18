# Google Dorking
The script will perform Google Dorking on a domain/list of domains, looking for new subdomains.

## Installation
```bash
pip install -r requirements.txt
```

## Execution
```bash
python3 google_dorking.py -d <domain>
```
or
```bash
python3 google_dorking.py -d <domains>.txt
```

`<domains>.txt` is the list of domains to be used, one per line. The new subdomains gathered in a dictionary will be printed in standard output.