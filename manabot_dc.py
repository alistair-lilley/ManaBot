import os, discord, requests
from datetime import datetime
from dotenv import load_dotenv

from readInCards import parseCOD
from convertDecks import convert
from loadImages import loadAllImages

from helpers import *

# Load all environment variables
load_dotenv()
TOKEN = os.getenv('DCTOKEN')
GUILD = os.getenv('GUILD')
path_to_cards = os.getenv('CARDPATH')
path_to_bot = os.getenv('BOTPATH')
imageDirs = os.getenv('IMAGEPATH')
me = os.getenv('KOKIDC')

client = discord.Client()

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Load name dicts and card prefix tree
images, names, loadingErrors = loadAllImages(imageDirs)
cards = parseCOD(path_to_cards)
mS(cards)

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Connect to server
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


    dt = datetime.now().strftime("%d-%m-%Y %H:%M ")
    errs = dt+loadingErrors

    user=await client.fetch_user(me)
    await user.send(f'{client.user} is connected to the following guild:')
    await user.send(f'{guild.name}(id: {guild.id})')
    await user.send(errs)

# React to messages
@client.event
async def on_message(message):
    # get channel and content data
    channel = message.channel
    content = message.content

    # don't reply to self
    if message.author == client.user:
        return

    # parse content of message
    contParsed = content.split()
    # if it contains anything:
    if len(contParsed):
        # Get the command
        cmd = contParsed[0].lower()
        if cmd == "!card":
            # Get the cardname
            cardname = simplifyName(' '.join(contParsed[1:]))
            # try-except for getting card pic
            # get proper name
            similars = findSimilar(cards, cardname)
            if cardname in names:
                propName = names[cardname]
            else:
                propName = similars[0]
            # get path
            path = imageDirs+'/'+images[propName]+'/'+propName+'.jpg'
            # send file
            with open(path,'rb') as f:
                cardpic = discord.File(f)
                await channel.send(file=cardpic)
            try:
                # get card data
                cardData = binarySearch(cards, cardname)
                # send if possible
                await channel.send(cardData.printData())
            # if it couldn't find it, send similar data
            except:
                similars = '\n'.join(similars[1:])
                cardData = binarySearch(cards, propName).printData()
                await channel.send(f"Card not found. Most similar is:\n{cardData}\n\nDid you mean...\n{similars}")

    # Convert .toparse and .decs to .txts
    if message.attachments:
        # get filename
        fullname = message.attachments[0].filename
        # get name w/o ext and ext w/o name
        name, ext = stripExt(fullname)
        # if the ext is .cod, convert it
        if ext in ['.cod','.mwDeck']:
            # get url
            furl = message.attachments[0].url
            # download file
            r = requests.get(furl)
            open(path_to_bot+"/toparse/"+fullname, 'wb').write(r.content)
            # convert file
            convert(path_to_bot,name,ext)
            # reupload file
            with open(path_to_bot+"/txts/"+name+".txt",'rb') as upload:
                await channel.send(file=discord.File(upload,name+".txt"))




client.run(TOKEN)