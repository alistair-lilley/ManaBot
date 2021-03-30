'''                             Parse Cards to prefTree                                     '''
'''
        File for parsing an element tree of cards into a prefix tree for use elsewhere
        Three functions:
        parseCOD -> parseCard -> parseProps (from top to bottom)
        parseCOD is the main function
        parseCard gets the card attribtues
        parseProps gets the attributes from the <prop> subtags
'''
import xml.etree.ElementTree as ET
from card import Card
from dotenv import load_dotenv
from helpers import *
import os

load_dotenv()

path_to_cards = os.getenv('CARDPATH')

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
def parseCOD(codfile):
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



if __name__ == "__main__":
    cards = parseCOD(path_to_cards)
    mS(cards)
    #print([card.name for card in cards])
    phytow = binarySearch(cards, "Phyrexian Tower")
    print(phytow.name)
    phyalt = binarySearch(cards, "phyrexian altar")
    print(phyalt.name)
    a = findSimilar(cards, "aaaaaaaaa")
    print(a)