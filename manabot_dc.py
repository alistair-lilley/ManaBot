'''                                                  MANABOT FOR DISCORD                                             '''
'''
    Mana Bot main (discord implementation)
'''
import os, discord, requests
from datetime import datetime
from dotenv import load_dotenv

from convertDecks import convert, getDecks

from cardmanager import CardMgr
from rulesmanager import RulesMgr

from helpers import *

# Load all environment variables
load_dotenv()
TOKEN = os.getenv('DCTOKEN')
GUILD = os.getenv('GUILD')
path_to_cards = os.getenv('CARDPATH')
path_to_bot = os.getenv('BOTPATH')
path_to_images = os.getenv('IMAGEPATH')
me = os.getenv('KOKIDC')

client = discord.Client()

########################################################################################################################
########################################################################################################################
########################################################################################################################


CardManager = CardMgr(path_to_images,path_to_cards,path_to_bot,me)
RulesManager = RulesMgr("rules.txt")

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


    dt = datetime.now().strftime("%d-%m-%Y %H:%M")
    errs = dt#+loadingErrors

    user = await client.fetch_user(me)
    await user.send(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n{errs})')

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
            cardname = simplifyString(' '.join(contParsed[1:]))
            cardpic = await CardManager.searchImage(cardname)
            await channel.send(file=cardpic)
            cardData = await CardManager.searchDescription(cardname)
            await channel.send(cardData)

        if cmd == "!rule":
            query = ' '.join(contParsed[1:])
            ruledata = RulesManager.runCmd(query)
            for r in ruledata:
                await channel.send(r)



    # Convert .toparse and .decs to .txts
    if message.attachments:
        fullname = message.attachments[0].filename
        furl = message.attachments[0].url
        r = requests.get(furl)
        srcpath = path_to_bot+"/toparse/"+fullname
        open(srcpath, 'wb').write(r.content)
        decks = convert(path_to_bot,fullname)
        for f in decks:
            if f == None:
                continue
            with open(f[0],'rb') as upload:
                await channel.send(file=discord.File(upload,f[1]))






client.run(TOKEN)