
'''                                                  MANABOT FOR TELEGRAM                                            '''
'''
    Mana Bot main (telegram implementation)
''''''                                                  MANABOT FOR DISCORD                                             '''
'''
    Mana Bot main (discord implementation)
'''
import os, discord, asyncio, logging, hashlib

# Bot-oriented imports
from aiogram import Bot, Dispatcher
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from datetime import datetime

from dotenv import load_dotenv

from Managers.deckmanager import DeckMgr
from Managers.cardmanager import CardMgr
from Managers.rulesmanager import RulesMgr
from Managers.dicemanager import DiceMgr

from Managers.botmanager import BotMgr

from setupfiles.helpers import *

# Load all environment variables
load_dotenv()
#The bot tokens
DCTOKEN = os.getenv('DCTOKEN')
TGTOKEN = os.getenv('TGTOKEN')
# The discord guild
GUILD = os.getenv('GUILD')
# The data paths
path_to_cards = os.getenv('CARDPATH')
path_to_bot = os.getenv('BOTPATH')
path_to_images = os.getenv('IMAGEPATH')
path_to_decks = os.getenv('DECKSPATH')
# The help and rules files
dcbothelp = os.getenv('DCBOTHELP')
tgbothelp = os.getenv('TGBOTHELP')
rules = os.getenv('RULES')
# My ids
medc = os.getenv('KOKIDC')
metg = os.getenv('KOKITG')
# clear stuff idr
clr = path_to_bot+'/readintexts/clr.txt'
# Get dicord client
client = discord.Client()
# Start logging and initialize bot and dispatcher objects
logging.basicConfig(level=logging.INFO)
tgbot = Bot(token=TGTOKEN)
dp = Dispatcher(tgbot)



########################################################################################################################
########################################################################################################################
########################################################################################################################

# Load CardMgr object
# This will load image & name dicts, card list, exists set, searchable card list, and merge sort them
# It will also store found cards for searching/checking
CardManager = CardMgr(path_to_images,path_to_cards,path_to_bot,metg,tgbot)
RulesManager = RulesMgr(rules,dcbothelp)
DeckManager = DeckMgr(path_to_bot,["/data/toparse/","/data/txts/"], CardManager)
DiceManager = DiceMgr()

managers = [CardManager, RulesManager, DeckManager, DiceManager]

# Special manager -- manages sending the messages through the two bots, for cleanliness
BotManager = BotMgr(tgbot,open(clr).read(),metg)

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Startups

# Send startup message
async def startAlert():
    dt = datetime.now().strftime("%d-%m-%Y %H:%M")
    upmsg = f"Bot has started: {dt}"
    await tgbot.send_message(metg,upmsg)

# Startup
async def on_startup(d: Dispatcher):
    asyncio.create_task(startAlert())


# Connect to server
@client.event
async def on_ready():
    # Start the telegram bot WITHIN the discord bot
    await on_startup(dp)
    await dp.skip_updates()
    asyncio.ensure_future(dp.start_polling())

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    dt = datetime.now().strftime("%d-%m-%Y %H:%M") # get online time

    # Send me uptime log
    user = await client.fetch_user(medc)
    await user.send(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n{dt})')
    asyncio.create_task(DeckManager.scheduledClear())

########################################################################################################################
########################################################################################################################
########################################################################################################################

# TELEGRAM

# Inline handler
# This was one hell of a mess, so lets clean it up!
@dp.inline_handler()
async def on_inline(message: InlineQuery):
    tosend = open(tgbothelp).read()

    # get commands and queries
    cmd = simplifyString(message.query.split()[0]) # Since you can search *either* card or rule, we use command
    query = ' '.join(simplifyString(message.query.split()[1:])) # Then the whole string query
    for mgr in managers:
        if '!'+cmd in mgr.cmds:
            tosend = await mgr.handle('!'+cmd,query)

    await BotManager.send(tosend,message=message)


########################################################################################################################
########################################################################################################################
########################################################################################################################

# DISCORD

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


    # if it's a command
    if len(contParsed):
        cmd = contParsed[0].lower()
        query = simplifyString(' '.join(contParsed[1:]))
        for mgr in managers:
            if cmd in mgr.cmds:
                if message.attachments:
                    msgatt = message.attachments[0]
                    tosend = await mgr.handle(cmd,query,attached=[msgatt.filename,msgatt.url])
                else:
                    tosend = await mgr.handle(cmd,query)

                await BotManager.send(tosend,channel=channel)

    ''' These too
    
    # work with deck files
    elif message.attachments:
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
                await channel.send(open(clr).read())'''



if __name__ == "__main__":
    loop = asyncio.get_event_loop() # Make an event loop
    loop.create_task(client.run(DCTOKEN)) # Add the discord client
    loop.run_forever() # Run forever