'''                                                     INIT                                                         '''
'''
    This file covers imports and envs, and setting up the managers and bots
'''

__all__ = [
    "asyncio",
    "sys",
    "datetime",
    "simplifyString",
    "tgbothelp",
    "tgbot",
    "DCTOKEN",
    "metg",
    "medc",
    "GUILD",
    "Dispatcher",
    "client",
    "dp",
    "InlineQuery",
    "managers",
    "BotManager",
    "UpdateManager"]

import os, discord, logging, asyncio, sys
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

from Managers.updatemanager import Updater

from helpers.helpers import simplifyString

# Load all environment variables
load_dotenv()
#The bot tokens
DCTOKEN = os.getenv('DCTOKEN')
TGTOKEN = os.getenv('TGTOKEN')
# The discord guild
GUILD = os.getenv('GUILD')
# The data paths
path_to_cards = "data/json/AllCardsJSON.json"
path_to_images = "data/images"
# The help and rules files
dcbothelp = "data/readintexts/dchelp.txt"
tgbothelp = "data/readintexts/tghelp.txt"
path_to_rules = "data/readintexts/rules.txt"
# My ids
medc = os.getenv('KOKIDC')
metg = os.getenv('KOKITG')
# Updater stuff
path_to_json = "data/json/AllCardsJSON.json"
path_to_json_hash = "data/json/hash.txt"
path_to_blacklist = "data/json/blacklist.txt"
# clear stuff idr
clr = 'data/readintexts/clr.txt'
# Get dicord client
client = discord.Client()
# Start logging and initialize bot and dispatcher objects
logging.basicConfig(level=logging.INFO)
tgbot = Bot(token=TGTOKEN)
dp = Dispatcher(tgbot)
# Make sure you're in the right dir
os.chdir(os.path.dirname(__file__))

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Check that all the required directories exist and make them if not
    
paths = [d for d in ["data/"+r for r in ["toparse/","txts/","json/","bans/","resizedpics/"]]]
for p in paths:
    if not os.path.isdir(p):
        os.mkdir(p)

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Load CardMgr object
# This will load image & name dicts, card list, exists set, searchable card list, and merge sort them
# It will also store found cards for searching/checking
CardManager = CardMgr(path_to_images,path_to_cards,metg,tgbot)
RulesManager = RulesMgr(path_to_rules,dcbothelp)
DeckManager = DeckMgr(["data/toparse/","data/txts/"], CardManager)
DiceManager = DiceMgr()

managers = [DeckManager, CardManager, RulesManager, DiceManager]

# Special manager -- manages sending the messages through the two bots, for cleanliness
BotManager = BotMgr(tgbot,open(clr).read(),metg)

# Special manager -- updates the database very 24hr
UpdateManager = Updater(path_to_json,path_to_rules,path_to_blacklist,path_to_images)
