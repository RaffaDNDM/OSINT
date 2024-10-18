from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from termcolor import cprint
import argparse

LINE = "_________________________________________________________"

def arg_parser():
    '''
    Parser of command line arguments
    '''
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-img", "-input", "-in", "-f", "-file", dest="file", help="Filepath of the image to be analysed.")
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.file:
        parser.print_help()
        exit(1)
    
    img_file=args.file
    print("\n")
    cprint('Image file:   ', 'yellow', attrs=['bold',], end='')
    print(f'{img_file}', end='\n\n')


    return img_file


def menu(exifdata, tags_names=[]):
    # To get to headers, you treat the Message() as a dict:    
    cprint('\nSelect the header you want to visualize\n'+LINE, 'blue')

    if len(tags_names):
        for i in range(len(tags_names)):
            cprint(f"{i+1}. {tags_names[i][1]}", 'cyan')
    else:
        cprint("0 tags identified.", 'cyan')
        cprint(LINE, 'blue',end="\n\n")
        exit(0)

    cprint('CTRL+C to stop the program...', 'green')
    cprint(LINE, 'blue')  

    try:
        choice = int(input())
        
        if choice<1 or choice>(len(tags_names)):
            raise ValueError
        else:
            tag = tags_names[choice-1][1]
            data = exifdata.get(tags_names[choice-1][0])

            if isinstance(data, bytes):
                data = data.decode()
            
            cprint(f'{tag}:', 'yellow')
            print(data)

    except ValueError:
        print(f"Insert a number in range 1-{len(tags_names)}", 'red')


def main():
    img_file = arg_parser()

    with Image.open(img_file) as img:
        # extract EXIF data
        exifdata = img.getexif()

        #Save tags names
        tags_names=[]
        
        for x in exifdata:
            tag=TAGS.get(x, x)
            tags_names.append((x,tag))

        try:
            while True:
                menu(exifdata, tags_names)
        except KeyboardInterrupt:
            exit(0)


if __name__=="__main__":
    main()