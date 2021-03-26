'''                             COD to TXT converter                            '''
'''
        This file converts .cod files to .txt files; .cod files are an .xml format file
        Specifically, it will take a filepath for a .cod and write a new file as a .txt with the same name
'''
import xml.etree.ElementTree as ET

# Convert cod to txt
# filepath is the base path (in this case, the path to the bot directory)
# filename is the name without .cod
def convert(filepath,filename,ext):
    # get filename as txt and cod
    nametxt = filename+'.txt'
    namefull = filename+ext
    fullpath = filepath+'/toparse/'+namefull
    wf = open(filepath+'/txts/'+nametxt,'w') # Open up a writable txt
    if ext == '.cod':
        CODtree = ET.parse(fullpath) # Get the cod file as an xml tree
        root = CODtree.getroot() # get root
        cards = [] # initialize cards list
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
    # converst .mwDecks
    # Treats them as text files
    elif ext == '.mwDeck':
        deckFile = [line.strip().split() for line in open(fullpath)]
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
    else:
        # Catches if something went wrong so it doesn't jsut crash
        cards = ["error"]
    allcards = '\n'.join(cards) # make into string
    # write and close
    wf.write(allcards)
    wf.close()