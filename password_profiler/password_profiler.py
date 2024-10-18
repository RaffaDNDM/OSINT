from termcolor import cprint
from datetime import datetime
from pyfiglet import Figlet
from alive_progress import alive_bar
from random import seed
from random import randint

#Victim information to be inserted
USER_INFO=[ "First name",
    "Surname",
    "Nickname",
    "Birthday (DDMMYYYY)"
]

#Victim's parent information to be inserted
PARTNER_INFO=[ "Partner name",
    "Partner surname",
    "Partner nickname",
    "Partner birthday (DDMMYYYY)",
    "Marriage date (DDMMYYYY)"
]

#Victim's children information to be inserted
CHILDREN_INFO=[ "Children's names (separated by comma)",
    "Children nicknames (separated by comma)",
    "Children birthdays (separated by comma)(DDMMYYYY)"
]

#Victim additional information to be inserted
ADDITIONAL_INFO=[ "Pets names (separated by comma)",
    "Company's name",
    "Other keywords (separated by comma)" 
]

#All information dictionary
PROFILER_INFO={ "User": USER_INFO,
    "Partner": PARTNER_INFO,
    "Children": CHILDREN_INFO,
    "Additional": ADDITIONAL_INFO
}

#Symbols to be used in passwords
SYMBOLS = """~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/"""

#Mapping of letters to numbers in Passwords
MAP_CHAR_TO_SYMBOL={ 'a': '4',
    'b': '8',
    'e': '3',
    'g': '9',
    'i': '1',
    'o': '0',
    'q': '9',
    "s": '5',
    't': '7',
    'z': '2'
}

def input_analyser(ask_dates=True):
    global PROFILER_INFO
    dates = []
    keywords = []

    #Ask information about victim and store them
    for info_type in PROFILER_INFO:
        cprint(f'\n{info_type.upper()} INFORMATION', "red")
        cprint(f'_________________________________', "red")
        for k in PROFILER_INFO[info_type]:
            if (not ask_dates) and '(DDMMYYYY)' in k:
                continue
            
            print(f'{k}: ', end='')
            x=input()
            x=x.replace(' ', '')

            #Split multiple information separated by comma
            if '(separated by comma)' in k:
                single_info = [item.lower() for item in x.split(',')]
                
                #Check if multiple information respect date format (if specified)
                if '(DDMMYYYY)' in k:
                    single_info = [datetime.strptime(d, "%d%m%Y") for d in single_info]
                    #Store dates
                    dates.extend(single_info)
                else:
                    #Store info specified as keywords
                    keywords.extend(single_info)

            #Check if the information respect date format (if specified)
            elif '(DDMMYYYY)' in k:
                #Store date
                single_info = datetime.strptime(x, "%d%m%Y")
                dates.append(single_info)

            else:
                #Store info specified as keyword
                keywords.append(x.lower())

    #Return stored information
    return set(dates), set(keywords)

def save_print_perms(PERMUTATIONS):
    #Save passwords in a file (one for each line)
    with open('passwords.txt', 'w') as f:
        f.write('\n'.join(PERMUTATIONS))

    cprint('\nPress any key to see the passwords list (CTRL+C to exit)', 'yellow')
    
    #Print all passwords on command line (one for each line)
    try:
        y=input()
    except KeyboardInterrupt:
        exit(1)

    for a,b,c in zip(PERMUTATIONS[::3],PERMUTATIONS[1::3],PERMUTATIONS[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))

    print('')

def permutation_dates(dates):
    PERM_DATES=set()

    #E.g. 15-th Februrary 1970
    for d in dates:
        #1970
        PERM_DATES.add(str(d.year))
        #70
        PERM_DATES.add(str(d.year)[2:])
        #15021970
        PERM_DATES.add(d.strftime("%d%m")+str(d.year))
        #150270
        PERM_DATES.add(d.strftime("%d%m%y"))
        #02151970
        PERM_DATES.add(d.strftime("%m%d")+str(d.year))
        #021570
        PERM_DATES.add(d.strftime("%m%d%y"))
        #19701502
        PERM_DATES.add(str(d.year)+d.strftime("%d%m"))
        #701502
        PERM_DATES.add(d.strftime("%y%d%m"))
        #19700215
        PERM_DATES.add(str(d.year)+d.strftime("%m%d"))
        #700215
        PERM_DATES.add(d.strftime("%y%m%d"))

    return PERM_DATES

def map_keyword(keywords):
    global MAP_CHAR_TO_SYMBOL
    
    MAPPED_KEYWORDS=list(keywords)

    #Map characters in each keyword to numbers
    for i in range(len(MAPPED_KEYWORDS)):
        mapped_key=MAPPED_KEYWORDS[i][0].upper()

        for c in MAPPED_KEYWORDS[i][1:]:
            if c in MAP_CHAR_TO_SYMBOL:
                mapped_key+=MAP_CHAR_TO_SYMBOL[c]
            else:
                mapped_key+=c

        MAPPED_KEYWORDS[i]=mapped_key

    return MAPPED_KEYWORDS

def has_numbers(inputString):
    #Check if a string contains a number
    return any(char.isdigit() for char in inputString)

def keyword_permutation(keywords):
    global SYMBOLS

    # For each keyword:
    # > num symbols
    cprint("\n\nRESUME", "blue")
    cprint(f'_________________________________', "blue")
    print(f'{len(keywords)} keywords', end='\n\n')
    
    num_perm=len(keywords)*len(SYMBOLS)
    
    PERMUTATIONS = []
    #Replace some keywords characters with numbers
    keywords = map_keyword(keywords)
    
    with alive_bar(num_perm) as bar:
        seed(1)

        #If a keyword has not digit after mapping, append two random digits to the keyword
        for i in range(len(keywords)):            
            if not(has_numbers(keywords[i])):
                keywords[i]+= (str(randint(0,9))+str(randint(0,9)))
            
            #Append a symbol to the keyword
            for s in SYMBOLS:
                PERMUTATIONS.append(keywords[i]+s)
                bar()

    ADD_PERMUTATIONS=[]
    
    #Create passwords by concatenating two different keywords
    for x in PERMUTATIONS:
        for y in PERMUTATIONS:
            if x!=y:
                ADD_PERMUTATIONS.append(x+y)

    PERMUTATIONS.extend(ADD_PERMUTATIONS)
    save_print_perms(PERMUTATIONS)


def simple_permutation(dates, keywords):
    global SYMBOLS

    # For each keyword:
    # > num permutated dates (short and long year formats)
    # > 2 position of dates (beginning/end)
    # > num symbols
    cprint("\n\nRESUME", "blue")
    cprint(f'_________________________________', "blue")
    print(f'{len(keywords)} keywords')
    print(f'{len(dates)} dates', end='\n\n')

    PERMUTATIONS = []
    #Compute dates with all possible formats 
    PERM_DATES = permutation_dates(dates)

    num_perm=len(keywords)*len(PERM_DATES)*2*len(SYMBOLS)

    with alive_bar(num_perm) as bar:
        #Create possible passwords
        for k in keywords:
            #Capitalize first letter
            key_capitalized=k[0].upper()+k[1:]                
            
            for d in PERM_DATES:
                for s in SYMBOLS:
                    #K3yw0rd02151970?
                    PERMUTATIONS.append(key_capitalized+d+s)
                    bar()
                    #02151970K3yw0rd?
                    PERMUTATIONS.append(d+key_capitalized+s)
                    bar()

    save_print_perms(PERMUTATIONS)


def mixed_permutation(dates, keywords):
    global SYMBOLS

    # For each keyword:
    # > num permutated dates (short and long year formats)
    # > 2 position of dates (beginning/end)
    # > num symbols
    cprint("\n\nRESUME", "blue")
    cprint(f'_________________________________', "blue")
    print(f'{len(keywords)} keywords')
    print(f'{len(dates)} dates', end='\n\n')
    
    PERMUTATIONS = []
    #Compute dates with all possible formats 
    PERM_DATES = permutation_dates(dates)
    #Replace some keywords characters with numbers
    keywords = map_keyword(keywords)

    num_perm=len(keywords)*len(PERM_DATES)*2*len(SYMBOLS)
    print(num_perm)

    with alive_bar(num_perm) as bar:
        #Create possible passwords
        for k in keywords:
            for d in PERM_DATES:
                for s in SYMBOLS:
                    #Keyword02151970?
                    PERMUTATIONS.append(k+d+s)
                    bar()
                    #02151970Keyword?
                    PERMUTATIONS.append(d+k+s)
                    bar()

    save_print_perms(PERMUTATIONS)

def main():
    #Title
    f = Figlet(font='slant')
    print(f.renderText('Password Profiler'))

    #Menu
    choice=0
    while choice<1 or choice>3:
        print('')
        cprint("Select the type of parser you want to use:", "yellow")
        cprint("1) Standard permutation (e.g. Keyword01251970?, 01251970Keyword?)", "yellow")
        cprint("2) Keyword permutation (e.g. K3yw0rd?, Keyword46?)", "yellow")
        cprint("3) Standard + Keyword permutation (e.g. K3yw0rd01251970?, 01251970K3yw0rd?)", "yellow")

        try:
            choice = int(input())
        except ValueError:
            pass

    #Passwords generation
    if(choice==1):
        dates, keywords = input_analyser()
        simple_permutation(dates, keywords)
    elif(choice==2):
        dates, keywords = input_analyser(ask_dates=False)
        keyword_permutation(keywords)
    elif(choice==3):
        dates, keywords = input_analyser()
        mixed_permutation(dates, keywords)

if __name__=="__main__":
    main()