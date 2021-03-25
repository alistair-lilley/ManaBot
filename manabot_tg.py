import os, logging, hashlib
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from PIL import Image
from preftree import PrefNode
from CARDparser import parseCOD
from loadImages import loadAllImages, simplifyName
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputFile

# Load all environment variables
load_dotenv()
TOKEN = os.getenv('TGTOKEN')
path_to_cards = os.getenv('CARDPATH')
path_to_bot = os.getenv('BOTPATH')
imageDirs = os.getenv('IMAGEPATH')
me = os.getenv('KOKIO')

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

# Get the basic data: pre fix tree and name dictionaries
cardTree = PrefNode({"Name": '', "Type": ''})
parseCOD(path_to_cards, cardTree)

images, names = loadAllImages(imageDirs)

# This specifically stores the file id of cards already sent with the bot so it doesn't have to send the same cards
# over and over and over again
foundCards = {}

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

# Inline handler
# Man, fuck inline bots, they're such a pain
# This function gets a card based on typing it in on the inline
@dp.inline_handler()
async def postCard(message: InlineQuery):
    # Get cardname simplified
    cardname = simplifyName(message.query)
    # Sets description and pic to None in case the try-except fails
    cardd, cardpic = None, None
    # Try-except for the card image
    try:
        # gets the proper name
        propName = names[cardname]
        # gets the path to the proper name
        path = imageDirs + '/' + images[propName] + '/' + propName + '.jpg'
        # Sets an id for sending the message
        result_id: str = hashlib.md5(cardname.encode()).hexdigest()
        # This try tries finding the file id in the dictionary
        try:
            cardpic = InlineQueryResultCachedPhoto(id=result_id,photo_file_id=foundCards[propName])
        # Its except loads or reloads the image if it cant find the file id
        except:
            # Checks to see if the file is too beeg
            sizecheck = Image.open(path)
            if sizecheck.size[0] > 300:
                # and resizes it to 375x500 if so
                resized = sizecheck.resize((300,400), Image.ANTIALIAS)
                path = path_to_bot+'/resizedpics/'+propName+'.jpg' # if it resizes, it gets the new pic's file path
                resized.save(path)
            # That part is specifically to make sure it CAN send the file, cuz if it's too big it wont send
            cardphoto = InputFile(path)
            # Sends the pic to me, saves the file id, and deletes the photo
            pic = await bot.send_photo(me,cardphoto)
            foundCards[propName] = pic.photo[0].file_id
            await bot.delete_message(me,pic.message_id)
            # Creates the cardpic variable for sending the file
            cardpic = InlineQueryResultCachedPhoto(id=result_id, title=[propName],photo_file_id=foundCards[propName])
    # If all that fails...
    except:
        # Prints a debugging error
        print("Card image not found:",cardname)
        # Creates a card image error to send
        err = "Image for " + cardname + " not found"
        input_content = InputTextMessageContent(err)
        result_id: str = hashlib.md5(cardname.encode()).hexdigest()
        cardpic = InlineQueryResultArticle(
            id=result_id,
            title=f'Can\'t find image for {cardname!r}.',
            input_message_content=input_content,
        )
    # Try-except for card text
    try:
        # This is mostly just so it doesn't crash in the next lines
        # It sets "propName" to cardname, then if it exists in the names dictionary, it replaces it
        propName = cardname
        if cardname in names:
            propName = names[cardname]
        # Gets card data from card prefix tree
        cardData = cardTree.findAndPrint(cardname)
        # Id for message
        c = cardname+'1'
        result_id: str = hashlib.md5(c.encode()).hexdigest()
        # Creates message content from card data
        input_content = InputTextMessageContent(cardData)
        # Creates result article to send-
        cardd = InlineQueryResultArticle(
            id=result_id,
            title=f'Information for {propName!r}',
            input_message_content=input_content,
        )
        # If it couldn't find the card...
        if cardData == "Card not found. Did you mean...\n":
            # Add onto cardData the similar results
            simcards = cardData+'\n'.join(cardTree.findAllSim(cardname))
            input_content = InputTextMessageContent(simcards)
            # Use that as the card data
            cardd = InlineQueryResultArticle(
                id=result_id,
                title=f'Info not found. Did you mean...',
                input_message_content=input_content,
            )
    except:
        print("Card not found. Big error.")

    # Results array
    # Store cardpic and cardd if they are found; if they failed, ignore them
    res = []
    if cardpic != None:
        res.append(cardpic)
    if cardd != None:
        res.append(cardd)

    # Try sending the data, and if it cant just throw an error
    try:
        await bot.answer_inline_query(message.id, results=res, cache_time=1)
    except:
        print("error\n\n")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)