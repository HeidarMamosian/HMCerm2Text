from xml.dom import minidom
from bs4 import BeautifulSoup
import unidecode
import argparse, sys, os
from os import listdir
from os.path import isfile, join
import glob
import string


# You can set prefixVar to add it before all generated files
# You can set postfixVar to add it after all generated files

prefixVar='prefix 2018'
postfixVar='sss'

parser=argparse.ArgumentParser()
parser.add_argument('--f', help='Specify the folder containing the cermine files.')
parser.add_argument('--out', help='Specify the output folder.')

args=parser.parse_args()

if(args.f==None):
    print("Please specify the folder containing cermine file.")
    exit()
if(not os.path.isdir(args.f)):
    print( f'Error. { args.f } is not valid path.')
    exit()


if(not os.path.isdir(args.out)):
    print( f'Error. { args.out } is not valid path.')
    exit()


inputfiles = [f for f in glob.glob(f'{args.f}/*.cermzones')]


filesnumber= len(inputfiles)
if(filesnumber==0):
    print("Ther is no file to process.")
    exit()

print("File processing started...")
for i,file in enumerate(inputfiles):
    filename = file
    print(f'{i+1} of {filesnumber} {filename} is processing...')
    
    # Open File
    file = open(filename,encoding="UTF-8")
    text = file.read()
   
    soup = BeautifulSoup(text, 'html.parser')

    # Extract First Author's name
    authorzone = soup.find('zone',attrs={'label': 'MET_AUTHOR'})
    if(authorzone==None):
        first_author='un-extarctable'
    else:
        first_author=authorzone.text
    unaccent_author = unidecode.unidecode(first_author)
    unaccent_author = unaccent_author.replace('\n',"")
    unaccent_author = unaccent_author.replace('.',"")

    
    # Extract Article's title
    titlezone = soup.find('zone',attrs={'label': 'MET_TITLE'})
    if(titlezone==None):
        title="Unextractable"
    else:
        title=titlezone.text
    unaccent_title = unidecode.unidecode(title)
    unaccent_title=unaccent_title.strip()
    unaccent_title=unaccent_title.replace("\n","")
    unaccent_title=unaccent_title.replace(".","")
    

    print(unaccent_title)

    content_list  = soup.findAll('zone', attrs={'label': ['BODY_CONTENT','BODY_HEADING']})

    outfilename = f'{unaccent_author},{unaccent_title}'
    
    outfilename=outfilename.replace("*","")
    outfilename=outfilename.replace("?","")
    outfilename=outfilename.replace("/","")
    outfilename=outfilename.replace("\\","")  
    outfilename=outfilename.replace(":","")
    outfilename=outfilename.replace('"',"")
    outfilename=outfilename.replace(">","")
    outfilename=outfilename.replace('<',"")
    outfilename=outfilename.replace('|',"")
    outfilename=outfilename.replace("'","")
    outfilename=outfilename[:200]

    oldname = os.path.basename(filename).split(".")[0]
    outputfilepathname= f'{args.out}\{prefixVar}{oldname}{postfixVar}.txt'
   
    outfile = open(outputfilepathname, mode="w",encoding="UTF-8")
    for sec in content_list:
        if(sec['label']=="BODY_HEADING"):
            outfile.write(sec.text + '\n')
        else:
            outfile.write(sec.text.replace('\n',' ') + '\n')

    outfile.close()


print("process finished successfully!")