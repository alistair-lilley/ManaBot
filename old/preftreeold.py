'''                         Prefix tree                         '''
'''
    this file contains the class for the prefix tree
    Overview: Each node is a card object that contains the following attributes:
        - Name
        - text
        - colors
        - color ID
        - mana cost
        - type
        - power/toughness
        - related cards
    as well as two meta attributes:
        - children
        - level (of tree)
    The class has 6 methods:
        - printData - Prints the attribute data of a single node (minus level and children attributes)
        - searchChildren - recursively searches through children to find a card
        - addChild - recursively searches for a place to add a new node; throws error if it exists
        - findAndPrint - recursively searches for a card and prints its data
        - findAllSim - initiates a search for lowest edit distance cards
        - findSimilar - recursively looks through nodes and records which card names have the lowest edit dist
'''
import eDistC
from loadImages import simplifyName


def addResult(name, cname, top, N):
    # get the two names to lowercase no punctuation
    sname = simplifyName(name)
    c = simplifyName(cname)
    # Gets edit distance
    dist = eDistC.edist(c, sname, len(c), len(sname))
    # Adds edit distance to top
    top[name] = dist
    # If there are more than N names in top, remove the one with the highest edit distance
    if len(top) > N:
        maxCard = max(top, key=top.get)
        del (top[maxCard])
    return top




# Prefix tree structures
# I'm using a prefix tree because it's quick and easy and runs fast

# individual node
# has a feature for each aspect of the card i want to print
# the features should be self explanatory
class PrefNode:
    def __init__(self, featDict):
        self.text, self.colors, self.colorid, self.cost, self.pt,self.related = "","","","","",""
        self.level = 0 # This is the level of the tree this node is on
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
        self.children = []

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

    # Searches through children to find a card with a matching name
    # Returns None if it can't find one
    def searchChildren(self, cname):
        # If this card is it, return itself
        if self.name == cname:
            return self
        # Loop through children to find it
        for c in self.children:
            # Check if this child is the card, and return if so
            if simplifyName(cname) == simplifyName(c.name):
                return c
            # Check if this child has matching letters (if so, the card will be a child of this child)
            if simplifyName(cname)[:c.level] == simplifyName(c.name)[:c.level]:
                return c.searchChildren(cname)
        return None

    # Add a child to the tree
    # v for verbose
    def addChild(self, child, v=False):
        # searches through children to see if child exists
        for c in self.children:
            if child.name == c.name:
                if v:
                    print("Card exists")
                return False
        # Loops through children to see if it can go below any of them
        for c in self.children:
            if child.name[:c.level] == c.name[:c.level]:
                return c.addChild(child)
        # Otherwise, adds to own children with a level of +1
        child.level = self.level+1
        self.children.append(child)
        if v:
            print("Card added:",child.name)
        return True

    # Find a card and print its information
    def findAndPrint(self, cname):
        # Recursively search
        foundCard = self.searchChildren(cname)
        # If it doesn't exist, return an error
        if foundCard == None:
            error = "Card not found. Did you mean...\n"
            return(error)
        # If it does, return the data from it
        return foundCard.printData()

    # Initiate recursive search for similar cardnames
    def findAllSim(self, cname, N=7):
        top = {} # Dictionary of top N cards
        # Recursively searches and edits top
        top = self.findSimilar(self, cname, N, top)
        # Returns top as a list, ordered from lowest edit distance to highest edit distance
        return list(sorted(top,key=top.get))

    # iteratively seasrch for similar cards
    def findSimilar(self, par, cname, N, top):
        parents = [par]
        parchilds = [0]
        i = 0
        while len(parents) > 0:
            top = addResult(parents[i].name, cname, top, N)
            while parchilds[i] < len(parents[i].children):
                if not parents[i].children[parchilds[i]].children:
                    top = addResult(parents[i].children[parchilds[i]].name, cname, top, N)
                    parchilds[i] += 1
                    continue
                if parents[i].children[parchilds[i]].children:
                    parents.append(parents[i].children[parchilds[i]])
                    parchilds.append(0)
                    parchilds[i] += 1
                    i += 1
                    continue
            parents = parents[:-1]
            parchilds = parchilds[:-1]
            i -= 1
        return top


    # gets all cards for any reason needed
    def allCards(self, cardList):
        if self.name != '':
            cardList.append(self.name)
        for c in self.children:
            cardList = c.allCards(cardList)
        return cardList

