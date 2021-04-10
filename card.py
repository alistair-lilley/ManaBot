'''                                                 card.py                                                          '''
'''
    This file contains all the major functions for laoding card information, as well as the card class
'''

import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from helpers import *
import os


load_dotenv()

path_to_cards = os.getenv('CARDPATH')

# Card class
class Card:
    def __init__(self, featDict):
        self.text, self.colors, self.colorid, self.cost, self.pt,self.related = "","","","","",""
        self.name = featDict["Name"]
        if "Text" in featDict:
            self.text = featDict["Text"]
        if "Colors" in featDict:
            self.colors = featDict["Colors"]
        if "Color ID" in featDict:
            self.colorid = featDict["Color ID"]
        if "Mana cost" in featDict:
            self.cost = featDict["Mana cost"]
        self.cardtype = featDict["Type"]
        if "P/T" in featDict:
            self.pt = featDict["P/T"]
        if "Related" in featDict:
            self.related = featDict["Related"]

    # Print data of a card
    # Prints.... the data from a card
    # but actually returns it as a string
    def printData(self):
        datas = []
        datas.append("Name: "+self.name)
        if self.cost != "":
            datas.append("Mana Cost: "+self.cost)
        if self.colors != "":
            datas.append("Color(s): "+self.colors)
        if self.colorid != "":
            datas.append("Color ID: "+self.colorid)
        datas.append("Type: "+self.cardtype)
        if self.pt != "":
            datas.append("P/T: "+self.pt)
        if self.text != "":
            datas.append("Text: "+self.text)
        if self.related != "":
            datas.append("Related cards: "+self.related)
        return "\n".join(datas)


# Parse the <prop> subtags
# Just get all of the subtag data
def parseProps(elem):
    propeles = {}
    for subele in elem:
        if subele.tag == "colors":
            propeles["Colors"] = subele.text
        elif subele.tag == "manacost":
            propeles["Mana cost"] = subele.text
        elif subele.tag == "coloridentity":
            propeles["Color ID"] = subele.text
        elif subele.tag == "type":
            propeles["Type"] = subele.text
        elif subele.tag == "pt":
            propeles["P/T"] = subele.text
    return propeles

#######################################################################################################################
#######################################################################################################################

# Parsing the XML file of card data

# Parse the <card> subtag
# juuuuust get the data
def parseCard(card):
    elems = {}
    for elem in card:
        if elem.tag == "name":
            elems["Name"] = elem.text
        elif elem.tag == "prop":
            elems.update(parseProps(elem))
    for elem in card:
        if elem.tag == "text":
            elems["Text"] = elem.text
        if elem.tag == "related":
            elems["Related"] = elem.text
    return elems

# Parse the whole tree
# loop through the tree, make each card into a prefix node, then add it to the prefix tree
def parseXML(codfile):
    CODtree = ET.parse(codfile)
    CODroot = CODtree.getroot()
    cards = []
    for child in CODroot:
        if child.tag != "cards":
            continue
        for card in child:
            nodeEles = parseCard(card)
            newEle = Card(nodeEles)
            cards.append(newEle)
    return cards


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