'''                                                  MANABOT FOR TELEGRAM                                            '''
'''
    Mana Bot main (telegram implementation)
'''
# Bot-oriented imports
import asyncio, os, logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery

from datetime import datetime

from helpers import *
from cardmanager import CardMgr
from rulesmanager import RulesMgr

# Load all environment variables
load_dotenv()
TOKEN = os.getenv('TGTOKEN')
path_to_cards = os.getenv('CARDPATH')
path_to_bot = os.getenv('BOTPATH')
path_to_images = os.getenv('IMAGEPATH')
rules = os.getenv("RULES")
me = os.getenv('KOKITG')

# Start logging and initialize bot and dispatcher objects
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


########################################################################################################################
########################################################################################################################
########################################################################################################################

# Load CardMgr object
# This will load image & name dicts, card list, exists set, searchable card list, and merge sort them
# It will also store found cards for searching/checking
CardManager = CardMgr(path_to_images,path_to_cards,path_to_bot,me,bot=bot)
RulesManager = RulesMgr(rules,bot)

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Send startup message
async def startAlert():
    dt = datetime.now().strftime("%d-%m-%Y %H:%M")
    upmsg = f"Bot has started: {dt}"
    await bot.send_message(me,upmsg)

# Startup
async def on_startup(d: Dispatcher):
    asyncio.create_task(startAlert())

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Inline handler
# This was one hell of a mess, so lets clean it up!
@dp.inline_handler()
async def on_inline(message: InlineQuery):
    # Ends on_inline if there's no query or if there's only 1 word query (i.e. card or rule)
    if message.query == '' or len(message.query.split()) == 1:
        return
    cmd = simplifyString(message.query.split()[0]) # Since you can search *either* card or rule, we use command
    query = ' '.join(simplifyString(message.query.split()[1:])) # Then the whole string query

    # temp down while rules are being fixed
    '''if cmd == "rule":
        ruledata = RulesManager.runCmd(query)
        await bot.answer_inline_query(message.id,results=ruledata,cache_time=1)'''

    #elif cmd == "card":
    if cmd == "card":

        data = await CardManager.getCard(query)

        # Results array
        # Store cardpic and cardd if they are found; if they failed, ignore them
        res = [d for d in data if d]

        # Try sending the data, and if it cant just throw an error
        if len(res) > 0:
            await bot.answer_inline_query(message.id, results=res, cache_time=1)
        else:
            await bot.send_message(me, f"There was an issue with sending a response to this query: {message}.\n"
                                       f"EVERYTHING went wrong, bro. Everything.")



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)