'''                                                 CARD MANAGER                                                     '''
'''
    This file is designed to create a singular, all-encompassing card manager object.
'''
from PIL import Image
# Aiogram imports
# Custom file imports
from helpers.card import XMLParser, loadAllImages
from helpers.helpers import *

XMLP = XMLParser()

def checkNamesDict(l,d):
    for item in l:
        if item not in d:
            print(f"Warning! {item} missing from dictionary!")

class CardMgr:
    def __init__(self,image_path,data_path,bot_path,metg,bot):
        self.cmds = ['!card']
        self.bot = bot
        self.metg = metg
        self.image_path = image_path
        self.data_path = data_path
        self.bot_path = bot_path
        # Image loading info
        self.image_path_d, self.image_name_d = loadAllImages(image_path)
        self.prevcards = {} # Records cards previously searched for quicker lookup
        # Data loading info
        self.cards = {simplifyString(c.feats["Name"]):c for c in XMLP.parseXML(data_path)}
        self.cardnames = [card for card in self.cards] # A sorted list of the cards for quick searching
        mS(self.cardnames)
        # The recent similars search, so that its callable by both search functions
        print(f"Lengths: cardnames {len(self.cardnames)}, cards {len(self.cards)}, image paths {len(self.image_path_d)}"
              f", image names {len(self.image_name_d)}")
        self.similars = []

    ############################################################################
    ############################################################################
    ############################################################################

    async def handle(self,cmd,query):
        if cmd == "!card":
            card = await self._getCard(query)
            return [card[0],card[1],None]

    ############################################################################
    ############################################################################
    ############################################################################

    # Getting basic data

    # Get both parts of card
    async def _getCard(self,cardname):
        try:
            cardpic = await self._searchImage(cardname)
        except:
            await self.bot.send_message(self.metg,"Whoa! Big error in card pic search\nNext is card data search")
            cardpic = None

        try:
            cardd = await self._searchDescription(cardname)
        except:
            await self.bot.send_message(self.metg, "Whoa! Big error in card data search")
            cardd = None
        return [cardd, cardpic]


    # Get raw dict data from card
    def getRaw(self,cardname):
        try:
            return self.cards[cardname].sendRaw()
        except:
            return None

        ############################################################################
        ############################################################################
        ############################################################################
        ############################################################################
        ############################################################################
        ############################################################################




            # Image section

    # Initialize image search
    async def _searchImage(self,cardname):
        self.similars = findSimilar(self.cardnames, cardname)
        setting = "Card image" # For default function
        try:
            cardpic = await self._getImage(cardname)
        except:
            cardpic = await self._getDefault(cardname,setting)
        return cardpic


    async def _getImage(self,cardname):
        # gets the proper name
        if cardname in self.image_name_d:
            propName = self.image_name_d[cardname]
        else:
            # Get the most similar name if can't find it...
            self.similars = findSimilar(self.cardnames, cardname)
            propName = self.image_name_d[self.similars[0]]
        # gets the path to image via proper name
        path = self.image_path + '/' + self.image_path_d[propName] #+ '/' + propName + '.jpg'
        # Checks to see if the file is too beeg
        sizecheck = Image.open(path)
        if sizecheck.size[0] > 350:
            # and resizes it to 350 if so
            resized = sizecheck.resize((350, 466), Image.ANTIALIAS)
            # if it resizes, it saves the resized pic to /resizedpics and gets the path
            path = self.bot_path + '/data/resizedpics/' + propName + '.jpg'
            resized.save(path)
        # That part is specifically to make sure it CAN send the file, cuz if it's too big it wont send
        # then return the path
        return path


        ############################################################################
        ############################################################################
        ############################################################################




        # Description section

    async def _searchDescription(self,cardname):
        setting = "Card data"
        try:
            carddata = await self._getDescription(cardname)
        except:
            carddata = await self._getDefault(cardname,setting)
        return carddata


    async def _getDescription(self,cardname):
        try:
            card = self.cards[cardname]
            simstr = ''
        except:
            if not self.similars:
                self.similars = findSimilar(self.cardnames, cardname)
            # If it couldn't find the card...
            # Add onto cardData the similar results
            card = self.cards[self.similars[0]]
            propSims = [self.cards[sim].feats["Name"] for sim in self.similars]
            simstr = '\n'.join(propSims[1:])
        cardData = card.printData()
        if cardData == '':
            cardData = "No data for this card."
        if simstr:
            cardData = f'Card not found. Closest match:\n{cardData}\n\nDid you mean...\n{simstr}'
        self.similars = []
        return cardData

        ############################################################################
        ############################################################################
        ############################################################################




        # Default

    async def _getDefault(self,cardname,setting):
        return f"{setting} for {cardname} not found."