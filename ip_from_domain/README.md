# IP from domain
The program will perform several tasks:
1. Resolve specific domain name
2. Calculate all IPs related to a subnetwork
3. Calculate all IPs and resolve domains from files

## Installation
```bash
pip3 install -r requirements.txt
```

## Cheat sheet
### Calculate all IPs and resolve domains from files
```bash
python3 ip_from_domain.py -ip scope_ips.txt -d scope_domains.txt
```
where:
- `scope_ips.txt` is the file containing target IPs;
- `scope_domains.txt` is the file containing target domains.

If at least one of the files doesn't exist it will be asked again on command line.
All the IPs, from either target domains file or target IPs file, will be stored in the file `all_ips.txt`.

If a target domains file is provided, a new file `resolved_domains.csv` will be created. The file will contain two columns:
- domain;
- resolved IP.

**Another execution modality:**
```bash
python3 ip_from_domain.py
```
Then select option *3* and provide path of target IPs and domains files.

### Resolve specific domain name
```bash
python3 ip_from_domain.py
```
Then select option *1* and provide domain to be resolved.

### Calculate all IPs related to a subnetwork
```bash
python3 ip_from_domain.py
```
Then select option *2* and IP subnet (e.g. 127.0.0.1/24) to be resolved in all its IPs.

## Help command
```bash
python3 ip_from_domain.py --help
```