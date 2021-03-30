


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