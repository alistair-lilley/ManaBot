import os
from CARDparser import parseCOD
from preftree import PrefNode
from dotenv import load_dotenv


load_dotenv()

path_to_cards = os.getenv('CARDPATH')

cardTree = PrefNode({"Name": '', "Type": ''})
parseCOD(path_to_cards, cardTree)

cardlist = []
allCards = '\n'.join(cardTree.allCards(cardlist))

with open('allCards.txt','w') as wf:
    wf.write(allCards)