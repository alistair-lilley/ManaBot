'''                                                  MANABOT FOR DISCORD                                             '''
'''
    Mana Bot main (discord implementation)
'''
import os, discord, asyncio
from datetime import datetime
from dotenv import load_dotenv

from deckmanager import DeckMgr
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
bothelp = os.getenv('BOTHELP')
rules = os.getenv('RULES')
me = os.getenv('KOKIDC')

clr = path_to_bot+'/clr.txt'

client = discord.Client()

########################################################################################################################
########################################################################################################################
########################################################################################################################


CardManager = CardMgr(path_to_images,path_to_cards,path_to_bot,me)
RulesManager = RulesMgr(rules)
DeckManager = DeckMgr(path_to_bot,["/toparse/", "/txts/"])

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

    dt = datetime.now().strftime("%d-%m-%Y %H:%M") # get online time

    # Send me uptime log
    user = await client.fetch_user(me)
    await user.send(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n{dt})')
    asyncio.create_task(DeckManager.scheduledClear())

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
    # Get the command

    # work with deck files
    if message.attachments:
        msgatt = message.attachments[0]

        if len(contParsed):  # gets command
            cmd = contParsed[0].lower()
        else:
            cmd = None


        # converts decks and gets list of deck file names *or* baned card lists
        decks = DeckManager.handle(attached=[msgatt.filename, msgatt.url], cmd=cmd)

        for f in decks:
            if f == None:
                continue
            #elif cmd == "!checkban" or type(decks[0]) == str:  # sends cardban lists
            #    await channel.send(f)
            else:  # send txt files of decks
                if type(f) == str:
                    await channel.send(f)
                    continue
                with open(f[0], 'rb') as upload:
                    await channel.send(f"**{f[1]}**")
                    await channel.send(file=discord.File(upload, f[1]))
                await channel.send(open(clr).read())

    # if it's a command
    elif len(contParsed):
        cmd = contParsed[0].lower()
        if cmd == "!card":
            cardname = simplifyString(' '.join(contParsed[1:]))
            carddata = await CardManager.getCard(cardname) # format [discordfile, cardtext]
            await channel.send(file=carddata[0])
            await channel.send(carddata[1])

        if cmd == "!rule":
            query = ' '.join(contParsed[1:])
            ruledata = RulesManager.runCmd(query)
            for r in ruledata:
                await channel.send(r)

        if cmd == "!cleardecks" and not message.guild:
            DeckManager.handle(attached=None,cmd=cmd)
            await channel.send("Decks cleared")

        if cmd == "!help":
            await channel.send(open(bothelp).read())










client.run(TOKEN)