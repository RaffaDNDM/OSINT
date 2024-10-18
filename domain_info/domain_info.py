import whois
from ip2geotools.databases.noncommercial import DbIpCity
import socket
from termcolor import cprint, colored

def IP_from_domain(domain):
    try:
        IP = socket.gethostbyname(domain)
        return IP

    except socket.gaierror:
        print("The domain doesn't exist")
        return ''

def geo_location(IP):
    '''
    Obtain location information of a specified IP.

    Args:
        IP (str): IP of the domain you want to analyse

    Returns:
        DbIpCity (Object): Location info of the address, IP
    '''
    return DbIpCity.get(IP, api_key='free')

def domain_whois(domain):
    '''
    Obtain information about a domain.

    Args:
        domain (str): Web domain you want to analyse

    Returns:
        whois_result (dict): Information about the specified domain.
    '''
    return whois.whois(domain)

def geo_print(location):
    '''
        Print information in the location object.

        Args:
            location (Object): Object returned by domain_whois() funtion
    '''

    cprint('City:', 'cyan', end=' ')
    print(location.city)
    cprint('Region:', 'cyan', end=' ')
    print(location.region)
    cprint('Country:', 'cyan', end=' ')
    print(location.country)

def whois_print(whois_result):
    '''
        Print information in the whoise dictionary.

        Args:
            whois_result (dict): Dictionary returned by geo_location() funtion
    '''

    for k in whois_result:
        cprint(f'{k}:', 'green', end=' ')
        print(whois_result[k])

def main():
    while True:
        try:
            cprint('Insert the domain you want to check (CTRL+C to exit)', 'blue')
            cprint('_____________________________________________________', 'blue')
            domain = input()
            IP = IP_from_domain(domain)

            if IP != '':
                cprint('_____________________________________________________', 'blue')
                cprint('IP:', 'red', end=' ')
                print(IP, end='\n\n')

                whois_print(domain_whois(domain))
                print('')
                geo_print(geo_location(IP))

            cprint('_____________________________________________________', 'blue', end='\n\n')

        except KeyboardInterrupt:
            break

if __name__=='__main__':
    main()