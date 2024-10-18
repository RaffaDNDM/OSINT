from termcolor import colored, cprint
import csv
import colorama

LINE = '___________________________________________________'

class TelephoneParser:
    '''
    Parser of the telephone numbers.

    Args:
        zones_path (str):
        operators_path (str):
        special_path (str):

    Attributes:
        ZONES_PATH (str): Path of the file with home prefix
                          and related zones of Italy

        OPERATORS_FILENAME (str): Path of the file with mobile prefix
                                  and related telephone operators

        SPECIAL_FILENAME (str): Path of the file with special numbers
                                and related services

        __ZONES (dict): Dictionary of couples (k, v) where:
                        k: home prefix
                        v=(v1, v2): zone of Italy 
                                    [v1 = region, v2=district]

        __OPERATORS (dict): Dictionary of couples (k, v) where:
                            k: mobile prefix
                            v: telephone operator

        __SPECIAL_NUMS (dict): Dictionary of couples (k, v) where:
                               k: special number
                               v: service related  
    '''

    ZONES_PATH = 'prefix_zones.csv'
    OPERATORS_FILENAME = 'prefix_operators.csv'
    SPECIAL_FILENAME = 'special_numbers.csv'
    __ZONES = {}
    __OPERATORS = {}
    __SPECIAL_NUMS = {}

    def __init__(self, zones_path=ZONES_PATH, 
                       operators_path=OPERATORS_FILENAME, 
                       special_path=SPECIAL_FILENAME):

        #Read the file with home prefixes and related zones
        with open(zones_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                if row[0] not in self.__ZONES:
                    self.__ZONES[row[0]] = [(row[1],row[2])]
                else:
                    self.__ZONES[row[0]].append((row[1],row[2]))

        #Read the file with mobile prefixes and related operators
        with open(operators_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.__OPERATORS={row[0]:row[1] for row in csv_reader}

        #Read the file with special numbers and related services
        with open(special_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.__SPECIAL_NUMS={row[0]:row[1] for row in csv_reader}

    def info(self, phone_num):
        '''
        Analyse the phone number.

        Args:
            phone_num (str): Phone number.
        '''

        #Remove prefix +39 for calls
        if len(phone_num) > 2 and phone_num[:3] == '+39':
            phone_num = phone_num[3:]

        if phone_num.startswith('3'):
            #Mobile phone number
            self.operator_from_num(phone_num)
        
        elif phone_num.startswith('0'):
            #Home phone number
            self.zone_from_num(phone_num)

        else:
            #Special number
            self.special_num(phone_num)

    def zone_from_num(self, phone_num):
        '''
        Analyse the home phone number.

        Args:
            phone_num (str): Home phone number.
        '''

        if len(phone_num) < 6 or len(phone_num) > 11:
            print('Invalid number', end='\n\n')
            return

        #Extract and analyse the prefix of the phone
        #(prefix can have from 2 to 5 digits)
        prefix = ''

        for i in range(2, 6):
            if phone_num[:i] in self.__ZONES:
                prefix = phone_num[:i]
                break

        if prefix == '':
            print('Prefix not found', end='\n\n')
        else:
            #Prefix found
            self.print_zones(prefix)

    def operator_from_num(self, phone_num):
        '''
        Analyse the mobile phone number.

        Args:
            phone_num (str): Mobile phone number.
        '''

        if len(phone_num) < 9 or len(phone_num)>10:
            print('Invalid number', end='\n\n')
            return

        #Extract and analyse the prefix of the phone
        #(prefix can have from 2 to 4 digits)
        prefix = ''
        
        for i in range(0, 2):
            if phone_num[:(4-i)] in self.__OPERATORS:
                prefix = phone_num[:(4-i)]
                break

        if prefix == '':
            print('Prefix not found', end='\n\n')
        else:
            #Prefix found
            cprint(self.__OPERATORS[prefix])

    def special_num(self, phone_num):
        '''
        Analyse the special phone number.

        Args:
            phone_num (str): Special phone number.
        '''
        
        if len(phone_num) < 3:
            print('Invalid number', end='\n\n')
            return

        if phone_num in self.__SPECIAL_NUMS:
            #Prefix found
            cprint(self.__SPECIAL_NUMS[phone_num], 'yellow', end='\n\n')
        else:
            print('Prefix not found', end='\n\n')


    def print_zones(self, prefix):
        '''
        Print all the district related to the prefix.

        Args:
            prefix (str): Prefix of the phone number
        '''

        for (region, town) in self.__ZONES[prefix]:
            print(colored(region, 'yellow')+f'-> {town}')

        print(' ')

def main():
    global LINE

    colorama.init()
    print('')
    parser = TelephoneParser()
    
    while True:
        try:
            cprint(f'Insert the phone number (CTRL+C to exit)\n{LINE}', 'blue')
            phone_num = input()
            cprint(LINE, 'blue')
            parser.info(phone_num)
        except KeyboardInterrupt:
            cprint('\nExit from program\n', 'red')
            exit(0)

if __name__=='__main__':
    main()