
'''                                                  MANABOT FOR TELEGRAM                                            '''
'''
    Mana Bot main (telegram implementation)
''''''                                                  MANABOT FOR DISCORD                                             '''
'''
    Mana Bot main (discord implementation)
'''
import os, discord, asyncio, logging

# Bot-oriented imports
from aiogram import Bot, Dispatcher
from aiogram.types import InlineQuery

from datetime import datetime

from dotenv import load_dotenv

from deckmanager import DeckMgr
from cardmanager import CardMgr
from rulesmanager import RulesMgr

from helpers import *

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
# The help and rules files
bothelp = os.getenv('BOTHELP')
rules = os.getenv('RULES')
# My ids
medc = os.getenv('KOKIDC')
metg = os.getenv('KOKITG')
# clear stuff idr
clr = path_to_bot+'/clr.txt'
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
RulesManager = RulesMgr(rules)
DeckManager = DeckMgr(path_to_bot,["/toparse/", "/txts/"], CardManager)

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
    # If there's no correct command query or no query info, show an "instructional" result
    if len(message.query.split()) < 2:
        info = CardManager.cmdInfo(message.id)
        await tgbot.answer_inline_query(message.id,results=info,cache_time=1)
        return

    # get commands and queries
    cmd = simplifyString(message.query.split()[0]) # Since you can search *either* card or rule, we use command
    query = ' '.join(simplifyString(message.query.split()[1:])) # Then the whole string query
    # temp down while rules are being fixed
    '''if cmd == "rule":
        ruledata = RulesManager.runCmd(query)
        await bot.answer_inline_query(message.id,results=ruledata,cache_time=1)'''

    if cmd == "card":

        data = await CardManager.getCard(query,metg)

        # Results array
        # Store cardpic and cardd if they are found; if they failed, ignore them
        res = [d for d in data if d]

        # Try sending the data, and if it cant just throw an error
        if len(res) > 0:
            await tgbot.answer_inline_query(message.id, results=res, cache_time=1)
        else:
            await tgbot.send_message(metg, f"There was an issue with sending a response to this query: {message}.\n"
                                       f"EVERYTHING went wrong, bro. Everything.")
        return

    # If there's no correct command query or no query info, show an "instructional" result
    info = CardManager.cmdInfo(message.id)
    await tgbot.answer_inline_query(message.id,results=info,cache_time=1)


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
            carddata = await CardManager.getCard(cardname,medc) # format [discordfile, cardtext]
            await channel.send(file=carddata[0])
            await channel.send(carddata[1])

        if cmd == "!rule":
            query = ' '.join(contParsed[1:])
            ruledata = RulesManager.handle(query)
            for r in ruledata:
                await channel.send(r)
            #await channel.send("Rules down")

        if cmd == "!cleardecks" and not message.guild:
            DeckManager.handle(attached=None,cmd=cmd)
            await channel.send("Decks cleared")

        if cmd == "!help":
            await channel.send(open(bothelp).read())



if __name__ == "__main__":
    loop = asyncio.get_event_loop() # Make an event loop
    loop.create_task(client.run(DCTOKEN)) # Add the discord client
    loop.run_forever() # Run forever