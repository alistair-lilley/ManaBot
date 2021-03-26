import os, discord, requests
from dotenv import load_dotenv
from preftree import PrefNode
from CARDparser import parseCOD
from convertDecks import convert
from loadImages import loadAllImages, simplifyName

# Load all environment variables
load_dotenv()
TOKEN = os.getenv('DCTOKEN')
GUILD = os.getenv('GUILD')
path_to_cards = os.getenv('CARDPATH')
path_to_bot = os.getenv('BOTPATH')
imageDirs = os.getenv('IMAGEPATH')

client = discord.Client()

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Load name dicts and card prefix tree
images, names = loadAllImages(imageDirs)
cardTree = PrefNode({"Name": '', "Type": ''})
parseCOD(path_to_cards, cardTree)

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
            try:
                # get proper name
                propName = names[cardname]
                # get path
                path = imageDirs+'/'+images[propName]+'/'+propName+'.jpg'
                # send file
                with open(path,'rb') as f:
                    cardpic = discord.File(f)
                    await channel.send(file=cardpic)

            except:
                # don't send if it can't find it
                print("Image not found:",cardname)
                await channel.send("Image not found")

            # Try-except for card data
            try:
                # get card data
                cardData = cardTree.findAndPrint(cardname)
                # send if possible
                await channel.send(cardData)
                # if it couldn't find it, send similar data
                if cardData == "Card not found. Did you mean...\n":
                    await channel.send('\n'.join(cardTree.findAllSim(cardname)))
            except:
                print("Card not found. Did you mean...")

    # Convert .toparse and .decs to .txts
    if message.attachments:
        # get filename
        fullname = message.attachments[0].filename
        # get name w/o ext and ext w/o name
        ext = '.'+fullname.split(".")[-1]
        name = fullname[:-len(ext)]
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