'''                             COD to TXT converter                            '''
'''
        This file converts .cod files to .txt files; .cod files are an .xml format file
        Specifically, it will take a filepath for a .cod and write a new file as a .txt with the same name
'''
import os, shutil
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from helpers import stripExt


# Main convert function
def convert(path_to_bot,f):
    # parse name and get paths
    name, ext = stripExt(f)
    srcpath = path_to_bot+"/toparse/"
    textpath = path_to_bot+"/txts/"

    # flist is a list of tuples of (path, filename) so that it uploads the file and a palatable name for it
    # Collect it dynamically
    if ext in ['.cod','.mwDeck']:
        convertDeck(srcpath,textpath,name,ext)
        flist = [(textpath+name+'.txt',name+'.txt')]
    elif ext == '.zip':
        flist = convertZip(path_to_bot,f)
    else:
        flist = [None]
    return flist

# Converts a whole zip by unzipping it, then converting each file within the unzipped dir
# There may be filename collisions but... that's a later project
def convertZip(path_to_bot,Z):
    zipname, zext = stripExt(Z)
    # mkdir with same name as zip
    subparse = path_to_bot+"/toparse/"+zipname
    subtext = path_to_bot+"/txts/"+zipname
    # Make sure there aren't any of these dirs, then make them
    # Baseically ensure they exist and are empty
    if os.path.exists(subparse):
        shutil.rmtree(subparse)
    if os.path.exists(subtext):
        shutil.rmtree(subtext)
    os.mkdir(subparse)
    os.mkdir(subtext)
    # extract all to that dir
    with ZipFile(path_to_bot+"/toparse/"+Z) as zf:
        zf.extractall(subparse)
    # Convert all the files and collect their paths,names
    flist = []
    return convertDir(subparse,subtext,flist)

# Converts a directory recursively
def convertDir(dirpath,textpath,flist):
    for df in os.listdir(dirpath):
        # Recurse if theres a dir
        if os.path.isdir(dirpath+'/'+df):
            flist = convertDir(dirpath+'/'+df,textpath,flist)
        # Convert if it's a cod or mwDeck
        else:
            fname, fext = stripExt(df)
            if fext in ['.cod','.mwDeck']:
                convertDeck(dirpath+'/',textpath+'/',fname,fext)
                flist.append((textpath+'/'+fname+'.txt',fname+'.txt'))
    return flist

# Convert a deck
# Basically goes through each possible extension and runs convert on it
def convertDeck(srcpath,textpath,name,ext):
    if ext == '.cod':
        cards = convertCod(srcpath,name+ext)
    elif ext == '.mwDeck':
        cards = convertmwDeck(srcpath+name+ext)
    # Just in case, so it doesn't completely crash
    else:
        cards = ['error']
    # Write
    with open(textpath+name+'.txt','w') as wf:
        wf.write('\n'.join(cards))

# Converts a .cod file, which is basically an .xml file
def convertCod(filepath,namefull):
    fullpath = filepath+namefull
    CODtree = ET.parse(fullpath)  # Get the cod file as an xml tree
    root = CODtree.getroot()  # get root
    cards = []  # initialize cards list
    # Loop through etree
    for child in root:
        # Skip any section that isn't a card zone
        if child.tag != 'zone':
            continue
        # Loop through children of a card zone
        for c in child:
            # Get the number of a type of card along with what the card is (e.g. '1 Sol Ring' or '10 Plains')
            cardline = c.attrib['number'] + " " + c.attrib['name']
            # If it's sideboarded, add 'SB: '
            if child.attrib['name'] != 'main':
                cardline = 'SB: ' + cardline
            # append to all cards
            cards.append(cardline)
    return cards

# Converts .mwDeck, which is basically a .txt file formatted differently from how Cockatrice likes them pasted in
def convertmwDeck(filepath):
    # Process it like a .txt
    deckFile = [line.strip().split() for line in open(filepath)]
    cards = []
    for line in deckFile:
        # ignores comment lines
        if line[0] == '//':
            continue
        # Adjusts SB lines since its a little different
        elif line[0] == 'SB:':
            cards.append(' '.join(line[:2]+line[3:]))
        else:
            cards.append(' '.join([line[0]]+line[2:]))
    return cards