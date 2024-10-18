# Bbot Results Parser
The script will parse the results (CSV file) of the execution of BBot on some targets. 
The program will keep only the domains identified by BBot removing other events results.

## Installation
```bash
pip install -r requirements.txt
```

## Execution
```bash
python3 bbot_results_parser.py -f <bbot_csv_file>
```

The new domains identified by BBot will be stored in the file `results_YYYYMMDD.csv`.