import ipcalc
import socket
from termcolor import cprint
import os
import argparse

def dns_resolve(ip_file, domain_file):
    IPS = set()

    #If target IPs file is provided
    if ip_file:
        #Read all IPs and resolve subnets, then store IPs in a set
        with open(ip_file, "r") as f:
            subnets=[x.replace("\n", "").strip() for x in f.readlines()]
            
            for net in subnets:
                for ip in ipcalc.Network(net):
                    IPS.add(str(ip))

    #If target domains file is provided
    if domain_file:
        #Read all domains
        with open(domain_file,"r") as f:
            domains=[x.replace("\n", "").strip() for x in f.readlines()]

        #Resolve all domains and store related IPs in a set and in a file
        with open("resolved_domains.csv", "w") as f:
            for d in domains:
                f.write(f"{d}, {socket.gethostbyname(d)}\n")
                IPS.add(socket.gethostbyname(d))

    #Store all IPs in an output file
    with open("all_ips.txt", "w") as f:
        IPS = sorted(IPS)

        for ip in IPS:
            f.write(f'{ip}\n')

def input_parameters():
    """
    Parse command line parameters.

    Return
    ----------
    ip_file (str): Path of the IP subnets file to be resolved.

    domain_file (str): Path of the domains file to be resolved.
    """    
    
    ip_file = None
    domain_file = None
    
    #Define argument parser
    parser = argparse.ArgumentParser()

    #Create command line arguments
    parser.add_argument('--ip-file', '-ip', '-i', dest='ip_file', help='Path of the file with all target IPs.')
    parser.add_argument('--domain-file', '-domain', '-d', dest='domain_file', help='Path of the file with all target domains.')
    
    #Parse command line arguments
    args = parser.parse_args()

    #Ask user input filename if invalid as command line argument
    if args.ip_file:
        ip_file=args.ip_file
    
        while not os.path.exists(ip_file):
            print('_IP file_')
            ip_file = input()
    
    #Ask user input filename if invalid as command line argument
    if args.domain_file:
        domain_file=args.domain_file
        
        while not os.path.exists(domain_file):
            print('_Domain file_')
            domain_file = input()

    return ip_file, domain_file

def main():
    ip_file, domain_file = input_parameters()
    
    if ip_file or domain_file:
        dns_resolve(ip_file, domain_file)
    else:
        mode = -1
        while mode>3 or mode<0:
            cprint("\nSelect which option you want to use:", "red")
            cprint("1) Resolve specific domain name", "red")
            cprint("2) Calculate all IPs related to a subnetwork", "red")
            cprint("3) Calculate all IPs and resolve domains from files", "red")
            cprint("0) Exit", "red")

            try:
                mode = int(input())

                if mode==1:
                    cprint("\nType the domain to be resolved:", "yellow")
                    domain = input()
                    cprint(f'{socket.gethostbyname(d)}\n', "blue")
                
                elif mode==2:
                    cprint("\nType the IP subnet to be resolved:", "yellow")
                    IP_net = input()

                    IPS = []
                    for ip in ipcalc.Network(IP_net):
                        IPS.append(str(ip))

                    for a,b,c,d in zip(IPS[::4],IPS[1::4],IPS[2::4],IPS[3::4]):
                        cprint('{:<18}{:<18}{:<18}{:<}'.format(a,b,c,d), "blue")
                
                elif mode==3:  
                    ip_file=''
                    domain_file=''
                    file_exist = False

                    while not file_exist:
                        cprint("\nType the path of the IP subnets file to be resolved:", "yellow")
                        ip_file = input()
                        file_exist = os.path.exists(ip_file)

                    file_exist = False

                    while not file_exist:
                        cprint("\nType the path of the domains file to be resolved:", "yellow")
                        domain_file = input()
                        file_exist = os.path.exists(domain_file)

                    dns_resolve(ip_file, domain_file)

                elif mode==0:
                    exit(0)
                    
                mode = -1
            
            except ValueError:
                print("You need to type a number in the range")    

if __name__=="__main__":
    main()
