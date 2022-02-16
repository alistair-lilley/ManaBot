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
    "UpdateManager"
]

import os, discord, logging, asyncio, sys
from aiogram import Bot, Dispatcher
from aiogram.types import InlineQuery
from datetime import datetime
from dotenv import load_dotenv

from Managers.deckmanager import DeckMgr
from Managers.cardmanager import CardMgr
from Managers.rulesmanager import RulesMgr
from Managers.dicemanager import DiceMgr
from Managers.botmanager import BotMgr
from Managers.updatemanager import Updater
from helpers.helperfns import simplifyString

# Load all environment variables
load_dotenv()
DCTOKEN = os.getenv('DCTOKEN')
TGTOKEN = os.getenv('TGTOKEN')
GUILD = os.getenv('GUILD')

path_to_cards = "data/json/AllCardsJSON.json"
path_to_images = "data/images"
path_to_json = "data/json/AllCardsJSON.json"
path_to_json_hash = "data/json/hash.txt"
path_to_blacklist = "data/json/blacklist.txt"

dcbothelp = "data/readintexts/dchelp.txt"
tgbothelp = "data/readintexts/tghelp.txt"
path_to_rules = "data/readintexts/rules.txt"
# My IDs are so it can send me errors directly
medc = os.getenv('KOKIDC')
metg = os.getenv('KOKITG')

clr = 'data/readintexts/clr.txt'

client = discord.Client()
logging.basicConfig(level=logging.INFO)
tgbot = Bot(token=TGTOKEN)
dp = Dispatcher(tgbot)
os.chdir(os.path.dirname(__file__))

########################################################################################################################
########################################################################################################################
########################################################################################################################
    
paths = [d for d in ["data/"+r for r in ["toparse/","txts/","json/","bans/","resizedpics/"]]]
for p in paths:
    if not os.path.isdir(p):
        os.mkdir(p)

########################################################################################################################
########################################################################################################################
########################################################################################################################

CardManager = CardMgr(path_to_images,path_to_cards,metg,tgbot)
RulesManager = RulesMgr(path_to_rules,dcbothelp)
DeckManager = DeckMgr(["data/toparse/","data/txts/"], CardManager)
DiceManager = DiceMgr()

managers = [DeckManager, CardManager, RulesManager, DiceManager]

BotManager = BotMgr(tgbot,open(clr).read(),metg)

UpdateManager = Updater(path_to_json,path_to_rules,path_to_blacklist,path_to_images)
