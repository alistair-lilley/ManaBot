'''                                                     INIT                                                         '''
'''
    This file covers imports and envs, and setting up the managers and bots
'''


import os, discord, logging, asyncio
from aiogram.types import InlineQuery
from datetime import datetime

from dotenv import load_dotenv

# Bot-oriented imports
from aiogram import Bot, Dispatcher

from Managers.deckmanager import DeckMgr
from Managers.cardmanager import CardMgr
from Managers.rulesmanager import RulesMgr
from Managers.dicemanager import DiceMgr

from Managers.botmanager import BotMgr

from setupfiles.helpers import simplifyString

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

managers = [DeckManager, CardManager, RulesManager, DiceManager]

# Special manager -- manages sending the messages through the two bots, for cleanliness
BotManager = BotMgr(tgbot,open(clr).read(),metg)
