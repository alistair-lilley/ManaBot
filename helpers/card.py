'''                                                 card.py                                                          '''
'''
    This file contains all the major functions for laoding card information, as well as the card class
'''

import os
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
    paths, names = {}, {}
    for d in os.listdir(imageDir):
        for c in os.listdir(imageDir+'/'+d):
            propName, ext = stripExt(c)
            paths[propName] = d+'/'+c
            simpleName = simplifyString(propName)
            names[simpleName] = propName
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
        ordered = ["Name", "Mana Cost", "Color(s)", "Color ID", "Type", "P/T", "Text", "Related cards"]
        return "\n".join([f'{o}: {self.feats[o]}' for o in ordered if o in self.feats])

#######################################################################################################################
#######################################################################################################################


# XML Parser class
# Cuz why not, let's make EVERYTHING an object!!!
class XMLParser:
    def __init__(self):
        self.NAME="XMLParser"

    # Parse the <prop> subtags
    # Just get all of the subtag data
    def _parseProps(self, elem):
        propeles = {}
        for subele in elem:
            if subele.tag == "colors":
                propeles["Color(s)"] = subele.text
            elif subele.tag == "manacost":
                propeles["Mana Cost"] = subele.text
            elif subele.tag == "coloridentity":
                propeles["Color ID"] = subele.text
            elif subele.tag == "type":
                propeles["Type"] = subele.text
            elif subele.tag == "pt":
                propeles["P/T"] = subele.text
        return propeles


    # Parsing the XML file of card data

    # Parse the <card> subtag
    # juuuuust get the data
    def _parseCard(self, card):
        elems = {}
        for elem in card:
            if elem.tag == "name":
                elems["Name"] = elem.text
            elif elem.tag == "prop":
                elems.update(self._parseProps(elem))
        for elem in card:
            if elem.tag == "text":
                elems["Text"] = elem.text
            if elem.tag == "related":
                elems["Related cards"] = elem.text
        return elems

    # Parse the whole tree
    # loop through the tree, make each card into a prefix node, then add it to the prefix tree
    def parseXML(self, codfile):
        CODtree = ET.parse(codfile)
        CODroot = CODtree.getroot()
        cards = []
        for child in CODroot:
            if child.tag != "cards":
                continue
            for card in child:
                nodeEles = self._parseCard(card)
                newEle = Card(nodeEles)
                cards.append(newEle)
        return cards


