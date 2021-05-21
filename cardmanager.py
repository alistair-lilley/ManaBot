'''                                                 CARD MANAGER                                                     '''
'''
    This file is designed to create a singular, all-encompassing card manager object.
'''
import hashlib, discord
from PIL import Image
# Aiogram imports
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputFile
# Custom file imports
from card import XMLParser, loadAllImages
from helpers import *

XMLP = XMLParser()

def checkNamesDict(l,d):
    for item in l:
        if item not in d:
            print(f"Warning! {item} missing from dictionary!")

class CardMgr:
    def __init__(self,image_path,data_path,bot_path,admin,bot=None):
        self.bot = bot
        self.me = admin
        self.image_path = image_path
        self.data_path = data_path
        self.bot_path = bot_path
        # Image loading info
        self.image_path_d, self.image_name_d = loadAllImages(image_path)
        self.prevcards = {} # Records cards previously searched for quicker lookup
        # Data loading info
        self.cards = {simplifyString(c.name):c for c in XMLP.parseXML(data_path)}
        self.cardnames = [card for card in self.cards] # A sorted list of the cards for quick searching
        mS(self.cardnames)
        # The recent similars search, so that its callable by both search functions
        print(f"Lengths: cardnames {len(self.cardnames)}, cards {len(self.cards)}, image paths {len(self.image_path_d)}"
              f", image names {len(self.image_name_d)}")
        #    print(item)
        self.similars = []

    ############################################################################
    ############################################################################
    ############################################################################

    # Get both parts of card
    async def getCard(self,cardname):
        try:
            cardpic = await self._searchImage(cardname)
        except:
            await self.bot.send_message(self.me,"Whoa! Big error in card pic search\nNext is card data search")
            cardpic = None

        try:
            cardd = await self._searchDescription(cardname)
        except:
            await self.bot.send_message(self.me, "Whoa! Big error in card data search")
            cardd = None
        return [cardpic, cardd]

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
        pic_result_id = hashlib.md5(cardname.encode()).hexdigest() # Get hashcode for message id number
        try:
            cardpic = await self._getImage(cardname,pic_result_id)
        except:
            cardpic = await self._getDefault(cardname,pic_result_id,setting)
        return cardpic


    async def _getImage(self,cardname,pic_result_id):
        # gets the proper name
        if cardname in self.image_name_d:
            propName = self.image_name_d[cardname]
        else:
            # Get the most similar name if can't find it...
            self.similars = findSimilar(self.cardnames, cardname)
            propName = self.image_name_d[self.similars[0]]
        # gets the path to image via proper name
        path = self.image_path + '/' + self.image_path_d[propName] #+ '/' + propName + '.jpg'
        if self.bot:
            # This try tries finding the file id in the dictionary and load the card if it's already been sent
            if propName in self.prevcards:
                photoid = self.prevcards[propName]
            # Its except loads or reloads the image if it cant find the file id
            else:
                # Checks to see if the file is too beeg
                sizecheck = Image.open(path)
                if sizecheck.size[0] > 350:
                    # and resizes it to 350 if so
                    resized = sizecheck.resize((350, 466), Image.ANTIALIAS)
                    # if it resizes, it saves the resized pic to /resizedpics and gets the path
                    path = self.bot_path + '/resizedpics/' + propName + '.jpg'
                    resized.save(path)
                # That part is specifically to make sure it CAN send the file, cuz if it's too big it wont send
                cardphoto = InputFile(path)
                # Sends the pic to me, saves the file id, and deletes the photo
                pic = await self.bot.send_photo(self.me, cardphoto)
                self.prevcards[propName] = pic.photo[0].file_id
                await self.bot.delete_message(self.me, pic.message_id)
                photoid = self.prevcards[propName]
                # Creates the cardpic variable for sending the file
            # sends cardpic
            cardpic = InlineQueryResultCachedPhoto(id=pic_result_id, photo_file_id=photoid)
        else:
            # send file
            with open(path, 'rb') as f:
                cardpic = discord.File(f)
        return cardpic

        ############################################################################
        ############################################################################
        ############################################################################

        # Description section

    async def _searchDescription(self,cardname):
        setting = "Card data"
        data_result_id = hashlib.sha256((cardname).encode()).hexdigest()
        try:
            carddata = await self._getDescription(cardname,data_result_id)
        except:
            carddata = await self._getDefault(cardname,data_result_id,setting)
        return carddata


    async def _getDescription(self,cardname,data_result_id):
        try:
            card = self.cards[cardname]
            simstr = ''
        except:
            if not self.similars:
                self.similars = findSimilar(self.cardnames, cardname)
            # If it couldn't find the card...
            # Add onto cardData the similar results
            card = self.cards[self.similars[0]]
            propSims = [self.cards[sim].name for sim in self.similars]
            simstr = '\n'.join(propSims[1:])
        propName = card.name
        cardData = card.printData()
        if cardData == '':
            cardData = "No data for this card."
        if simstr:
            cardData = f'Card not found. Closest match:\n{cardData}\n\nDid you mean...\n{simstr}'
        if self.bot:
            # Creates message content from card data
            input_content = InputTextMessageContent(cardData)
            # Creates result article to send-
            carddata = InlineQueryResultArticle(
                id=data_result_id,
                title=f'Information for {propName!r}',
                input_message_content=input_content,
            )
            # clear similars for the next search
        else:
            carddata = cardData
        self.similars = []
        return carddata

        ############################################################################
        ############################################################################
        ############################################################################

        # Default

    async def _getDefault(self,cardname,result_id,setting):
        err = f"{setting} for {cardname} not found."
        if self.bot:
            await self.bot.send_message(self.me, f"A {setting} error occurred with this query: {cardname}")
            # Prints a debugging error
            #print(f"{setting} not found: {cardname}")
            # Creates a card image error to send
            if setting == "Card image":
                err += f" Cockatrice does not have an image for this card."
            input_content = InputTextMessageContent(err)
            result = InlineQueryResultArticle(
                id=result_id,
                title=err,
                input_message_content=input_content,
            )
        else:
            result = err
        return result
