'''                                                 CARD MANAGER                                                     '''
'''
    This file is designed to create a singular, all-encompassing card manager object.
'''
from helpers.card import JSONParser, loadAllImages
from helpers.helperfns import *

JSONP = JSONParser()

def checkNamesDict(l,d):
    for item in l:
        if item not in d:
            print(f"Warning! {item} missing from dictionary!")

class CardMgr:
    def __init__(self,image_path,data_path,metg,bot):
        self.cmds = ['!card']
        self.bot = bot
        self.metg = metg
        self.image_path = image_path
        self.data_path = data_path
        self.prevcards = dict() # quicker lookup of previous searched card
        self.similars = []
        self.image_path_d, self.image_name_d = loadAllImages(self.image_path)
        self.cards = dict()
        self.cards_by_len = dict()
        self.cards = []
        self.update() # I feel like this is bad practice? but it reduces code

    ############################################################################
    ############################################################################

    # This is for when there is a data update
    def update(self):
        print("Updating CardManager")
        self.image_path_d, self.image_name_d = loadAllImages(self.image_path)
        try:
            self.cards = {simplifyString(c.feats["Name"]):c for c in JSONP.parseJSON(self.data_path)}
            for card in self.cards:
                self.cards_by_len[len(card)] = self.cards_by_len.get(len(card),[]) + [card]
            print(f"Lengths: cards {len(self.cards)}, "
                  f"image paths {len(self.image_path_d)}, "
                  f"image names {len(self.image_name_d)}")
        except:
            print("Json file not found")

    ############################################################################
    ############################################################################

    async def handle(self,cmd,query):
        if cmd == "!card":
            card = await self._getCard(query)
            return card
        elif cmd == "!raw":
            card = self._getRaw(query)
            return card

    ############################################################################
    ############################################################################

    def _getRaw(self,cardname):
        try:
            return [self.cards[cardname].sendRaw(), None, None]
        except:
            return [None, None, None]

    ############################################################################
    ############################################################################

    # Getting all data

    async def _getCard(self,cardname):
        if cardname not in self.prevcards:
            try:
                namelen = len(cardname)
                if namelen < 6:
                    namelen = 6
                elif namelen > max(self.cards_by_len)-7:
                    namelen = max(self.cards_by_len)-7
                similar_candidates = []
                for i in range(namelen-5,namelen+6):
                    similar_candidates += self.cards_by_len[i]
                self.similars = findSimilar(similar_candidates,cardname)
                self.prevcards[cardname] = self.similars
                self.prevcards[self.similars[0]] = [self.similars[0]]
            except:
                pass
        else:
            self.similars = self.prevcards[cardname]

        try:
            cardd = await self._searchDescription(cardname)
        except:
            await self.bot.send_message(self.metg, "Whoa! Big error in card data search\nNext is card pic search")
            cardd = "An error occurred searching" + cardname

        try:
            cardpic = await self._searchImage()
        except:
            await self.bot.send_message(self.metg,"Whoa! Big error in card pic search")
            cardpic = "data/default.jpg"

        self.similars = []

        return [cardd, cardpic, None]

        ############################################################################
        ############################################################################

    # Description section

    async def _searchDescription(self,cardname):
        try:
            carddata = await self._getDescription()
        except:
            print("Whoa! Big error in getting card description")
            carddata = f"Card data for {cardname} not found."
        return carddata


    async def _getDescription(self):
        card = self.cards[self.similars[0]]
        simstr = ''
        if len(self.similars) > 1:
            propSims = [self.cards[sim].feats["Name"] for sim in self.similars[1:]]
            simstr = '\n'.join(propSims)
        cardData = card.printData()
        if cardData == '':
            cardData = "No data for this card."
        if simstr:
            cardData = f'Card not found. Closest match:\n{cardData}\n\nDid you mean...\n{simstr}'
        return cardData

        ############################################################################
        ############################################################################

    # Image section

    async def _searchImage(self):
        try:
            cardpic = await self._getImage()
        except:
            print("Whoa! Big error in getting card image.")
            cardpic = "data/default.jpg"

        return cardpic


    async def _getImage(self):
        propName = self.similars[0]
        path = self.image_path_d[propName]
        # Checks to see if the file is too big because telegram won't send pictures that are over 350 pixels
        sizecheck = Image.open(path)
        if sizecheck.size[0] > 375:
            resized = sizecheck.resize((375, 500), Image.ANTIALIAS)
            path = '/data/resizedpics/' + propName + '.jpg'
            resized.save(path)
        return path

        ############################################################################
        ############################################################################
