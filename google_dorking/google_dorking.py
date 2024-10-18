from urllib.parse import urlparse
from googlesearch import search, get_useragent
import argparse
import os
import socket

def resolve(domain):
    try:
        result = socket.gethostbyname_ex(domain)
        return (result[1], result[2])
    except socket.gaierror:
        return ("N/A", "N/A")

class NoDomainSpecified(Exception):
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
    parser.add_argument("-d", "-domain", dest="domain", help="Domain/Path of a TXT file with domains (to be used in Google Dorking)")
    #Parse command line arguments
    args = parser.parse_args()
    
    domains = []
    #Check if the arguments have been specified on command line
    
    try:
        if not args.domain:
            raise NoDomainSpecified()
        else:
            filename, extension = os.path.splitext(args.domain)
            
            if extension == '.txt':
                if not os.path.exists(args.domain):
                    raise NoDomainSpecified()
                else:
                    with open(args.domain, "r") as f:
                        domains = [l.replace("\n", "") for l in f.readlines()]
            else:
                domains.append(args.domain)
    except NoDomainSpecified:
        parser.print_help()
        exit(0)
        
    return domains

def google_dorking(domains):
    result_domains = {}

    for d in domains:
        print(get_useragent())
        result = search(f"site:{d}", sleep_interval=10, num_results=400)

        urls = set()
        
        for url in result:
            urls.add(url)

            parsed_url = urlparse(url)
            if not parsed_url.hostname in result_domains:
                result_domains[parsed_url.hostname]=resolve(parsed_url.hostname)

    print(result_domains)

def main():
    domains = args_parser()
    google_dorking(domains)


if __name__=="__main__":
    main()