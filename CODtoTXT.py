'''                             COD to TXT converter                            '''
'''
        This file converts .cod files to .txt files; .cod files are an .xml format file
        Specifically, it will take a filepath for a .cod and write a new file as a .txt with the same name
'''
import xml.etree.ElementTree as ET

# Convert cod to txt
# filepath is the base path (in this case, the path to the bot directory)
# filename is the name without .cod
def convert(filepath,filename):
    # get filename as txt and cod
    nametxt = filename+'.txt'
    namecod = filename+'.cod'
    wf = open(filepath+'/txts/'+nametxt,'w') # Open up a writable txt
    CODtree = ET.parse(filepath+'/cods/'+namecod) # Get the cod file as an xml tree
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
    allcards = '\n'.join(cards) # make into string
    # write and close
    wf.write(allcards)
    wf.close()