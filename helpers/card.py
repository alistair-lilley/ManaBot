'''                                                 card.py                                                          '''
'''
    This file contains all the major functions for laoding card information, as well as the card class
'''

import os, json
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from helpers.helpers import stripExt, simplifyString


load_dotenv()

path_to_cards = os.getenv('CARDPATH')

#######################################################################################################################
#######################################################################################################################

# Load the images from the image directory

# Get a dictionary of name:path and a dictionary of simplename:propername by looping through the entire image
# directory and subdirectories
def loadAllImages(imageDir):
    names = set()
    paths = {}
    for c in os.listdir(imageDir):
        name, ext = stripExt(c)
        paths[name] = imageDir+'/'+c
        names.add(name)
    return paths, names

#######################################################################################################################
#######################################################################################################################

# Card class
class Card:
    def __init__(self, featDict):
        self.feats = featDict

    def sendRaw(self):
        toget = ["Mana Cost","Color ID","Type"]
        return {f:self.feats[f] for f in self.feats if f in toget}

    # Print data of a card
    # Prints.... the data from a card
    # but actually returns it as a string
    def printData(self):
        ordered = ["Name", "Mana Cost", "Color(s)", "Color ID", "Type", "P/T", "Text"] #, "Related cards"; get that l8r
        return "\n".join([f'{o}: {self.feats[o]}' for o in ordered if o in self.feats])

#######################################################################################################################
#######################################################################################################################

# SO MUCH SIMPLER
# SO MUCH CLEANER
# although we're missing a few things, fix later
class JSONParser:

    def __init__(self):
        self.NAME = "JSONParser"

    def _extractCard(self,card):
        c = dict()
        c["Name"] = card['name']
        c["Mana Cost"] = str(int(card['convertedManaCost']))
        if 'colors' in card:
            c["Color(s)"] = ''.join(card['colors'])
        else:
            c["Color(s)"] = 'C'
        if 'colorIdentity' in card:
            c["color ID"] = ''.join(card['colorIdentity'])
        else:
            c["Color ID"] = 'C'
        if 'power' in card:
            c["P/T"] = str(card['power'])+'/'+str(card['toughness'])
        else:
            c["P/T"] = "N/A"
        if 'text' in card:
            c["Text"] = card['text']
        else:
            c["Text"] = "N/A"
        c["Type"] = card['type']
        return c


    def parseJSON(self,datapath):
        alldata = json.load(open(datapath))
        allcards = []
        setlevel = alldata['data']
        for s in setlevel:
            for c in setlevel[s]['cards']:
                if 'faceName' in c:
                    continue
                allcards.append(Card(self._extractCard(c)))
        return allcards