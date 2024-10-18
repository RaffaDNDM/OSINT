import argparse
import os
import csv
from ipwhois import IPWhois
from alive_progress import alive_bar
import datetime

class NoFileSpecified(Exception):
    '''
    Error raised if the user doesn't specify a valid network IP address
    '''
    pass

def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-f", "-file", dest="file", help="Path of the CSV file with Bbot results")
    #Parse command line arguments
    args = parser.parse_args()
    
    results_f = None
    #Check if the arguments have been specified on command line
    try:
        if (not args.file):
            raise NoFileSpecified()
        else:
            filename, extension = os.path.splitext(args.file)
            
            if (extension != '.csv') or (not os.path.exists(args.file)):
                raise NoFileSpecified()
            else:
                results_f = args.file
    except NoFileSpecified:
        parser.print_help()
        exit(0)
        
    return results_f

def bbot_parsing(csv_file):
    import socket
    
    domains = {}  
    num_rows = 0
    with open(csv_file, "r") as f:
        num_rows = len(f.readlines())

    with open(csv_file, "r") as f:
        content = csv.DictReader(f)
        
        resolved_IPs = set()
        
        with alive_bar(num_rows) as bar:
            for line in content:
                bar()
                if line['Event type']=="DNS_NAME":
                    IPs = line['IP Address'].split(',')
                    
                    for ip in IPs:
                        if ip and ip not in resolved_IPs:
                            try:
                                #print(ip)
                                resolved_IPs.add(ip)
                                # Check if IPv4 format
                                socket.inet_pton(socket.AF_INET, ip)
                                
                                # Domain from IP
                                resolution = socket.gethostbyaddr(ip)
                                
                                # Whois
                                obj = IPWhois(ip)
                                res=obj.lookup_whois()
                                #print(type(res))

                                # If resolution is different from the hostname retrieved by Bbot and related to IP address
                                
                                for alias in resolution[1]:
                                    pass

                                    domains[resolution[0]]={}
                                    domains[resolution[0]]['IP'] = ip

                                    if res['nets']:
                                        domains[resolution[0]]['Network'] = res['asn_cidr']
                                        domains[resolution[0]]['Network Name'] = res['nets'][0]['name']
                                        domains[resolution[0]]['Organization Name'] = res['nets'][0]['description']
                                    #domains.add((alias,ip))
                            
                                if line['Event data'] not in domains:
                                    domains[line['Event data']] = {}
                                    domains[line['Event data']]['IP'] = ip
                                    domains[line['Event data']]['Network'] = res['asn_cidr']
                                    domains[line['Event data']]['Network Name'] = res['nets'][0]['name']
                                    domains[line['Event data']]['Organization Name'] = res['nets'][0]['description']    
                            except socket.error:
                                pass
                
    with open(f"results_{datetime.datetime.now().strftime('%Y%m%d')}.csv", "w") as f:
        f.write(f"Domain,IP,Network,Network Name,Organization Name,Detection Technology\n")
        for d in domains:
            f.write(f"{d},{domains[d]['IP']},{domains[d]['Network']},{domains[d]['Network Name']},{domains[d]['Organization Name']},BBOT\n")
    return domains

def main():
    csv_file = args_parser()
    domains = bbot_parsing(csv_file)


if __name__=="__main__":
    main()