'''                                                 RULES.TXT PARSER                                                 '''
'''
    This file is to parse the rules.txt file into a dictionary for easy lookup
    It parses to two dictionaries: keywords and rules
    The keyword dictionary is a keyworkd paired with a short rule description, which includes a numerical code for the
    full rules.
    The rules dictionary is numerical codes paired with full rules -- rules with children list the numbers for the 
    children.
    
    Quick note about the keyword dict:
    There isn't an easy way to distinguish keywords from the description text that Wizards put in (i.e. the credits), so
    unfortunately they're just gonna be part of the keywords. Won't affect much tho, they don't take up too much space &
    they don't interfere with seardching.
'''
import hashlib
from helpers import *
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle

# Some basic globals for quick lookup later on
NUMERALS = {str(i) for i in range(0,10)}
ALPH = set(list('abcdefghijklmnopqrstuvwxyz'))

# Read in rules file to get two dicts: a rules:rulecontent dict and a keyword:keywordcontent dict
# This was a pain
# Basically, the file will be formatted as such:
'''
    1. General
    
    100. Something
    
    100.1. Something else
    Example: things
    
    100.1a Another thing
    .
    .
    .
    Flying
    Flying rules with #
    
    Extort
    Extort rules with #
'''
# To parse it, we gotta account for how the file is constructed which is ANNOYING lol
def readRules(filename):
    with open(filename) as f:
        text = [line.strip() for line in f]

    rules = {}
    keywords = {}
    curRule = ''
    curKeyw = []
    for rule in text:
        # If the rule is empty, reset current rule and keyword, then keep goin
        if not rule:
            curRule = ''
            curKeyw = []
            continue
        # Get the rule as the first word of the rules
        r = rule.split()[0]
        # If there is a current rule, add this line to the rule
        if len(curRule) > 0:
            rules[curRule] += '\n'+rule
        # If there is a current keyword, add this line to the keywords
        elif len(curKeyw) > 0:
            for k in curKeyw:
                keywords[k] += '\n'+rule
        # If the first character is number, its a rule
        elif set(r[0]).issubset(NUMERALS):
            curRule, rules = addRule(rules, rule)
        # If the first character isn't a number, its a keyword
        else:
            # Add it to the keyword dict
            curKeyw = [k for k in rule.split(', ')]
            for k in curKeyw:
                keywords[k] = rule

    return rules, keywords


# Shit this was tricky
# Possible combinations:
# 1. --> ['1','']
# 100. --> ['100'.'']
# 100.2. --> ['100','2','']
# 100.2a --> ['100','2a']
def addRule(rules, rule):
    rname = rule.split()[0]
    rtext = ' '.join(rule.split()[1:])
    r = rname.split('.')
    if len(r) == 2: # 1. ; 100. ; 100.1a
        if len(r[0]) == 1: # 1.
            rules[rname] = rtext
        elif len(r[0]) == 3 and len(r[1]) == 0: # 100.
            rules[r[0][0]+'.'] += "\nSubrule: "+rule # Add as subrule to 1.
            rules[rname] = rtext
        else: # 100.1a
            rules[r[0]+'.'] += "\nSubrule: "+rule # Add as subrule to 100.
            rules[r[0]+'.'+r[1][:-1]+'.'] += "\nSubrule: "+rule # Add as subrule to 100.1.
            rules[rname] = rtext
    elif len(r) == 3: # 100.1.
        rules[r[0]+'.'] += "\nSubrule: "+rule # Add as subrule to 100.
        rules[rname] = rtext
    return rname, rules

# Chunkify it in case discord cant handle the LENGTH
def chunkMessage(data):
    r = [data]
    if len(data) > 2000:
        r = [data[:2000], data[2000:]]
        while len(r[-1]) > 2000:
            r = r[:-1] + [r[-1][:2000]] + [r[-1][2000:]]
    return r


class RulesMgr:
    def __init__(self,filename,bot=None):
        self.bot = bot
        self.rules, self.keywords = readRules(filename)
        # Simple string stuff to make sure it can handle irregular punctuation and capitalization
        self.simplerules = {simplifyString(rule):rule for rule in self.rules}
        self.simplekeywords = {simplifyString(keyword):keyword for keyword in self.keywords}
        self.kwlist = list(self.simplekeywords)
        mS(self.kwlist)

    def runCmd(self,query):
        title = "No match"
        FR = "No results"
        simplequery = simplifyString(query)
        # Keyword
        if simplequery in self.simplekeywords:
            print(simplequery)
            fullr = self.simplekeywords[simplequery]
            fullrule = self.keywords[fullr]
            FR = fullrule
            title = "Keyword: "+fullr
        # Rule
        elif simplequery in self.simplerules:
            fullr = self.simplerules[simplequery]
            fullrule = self.rules[fullr]
            FR = fullr + ' ' + fullrule
            title = "Rule: "+fullr
        # In case its neither
        elif simplequery[0] not in NUMERALS:
            similars = findSimilar(self.kwlist,simplequery)
            mostsim = similars[0]
            fullr = self.simplekeywords[mostsim]
            FR = "Closest match: "+self.keywords[fullr]+"\n\n Similar matches:\n"+\
                 '\n'.join([self.simplekeywords[sim] for sim in similars[1:]])
            title = "Closest match: "+fullr

        # Telegram
        if self.bot:
            # Get message id for sending
            data_result_id = hashlib.sha256((query).encode()).hexdigest()
            # Creates message content from card data
            input_content = InputTextMessageContent(FR)
            # Creates result article to send
            FR = InlineQueryResultArticle(
                id=data_result_id,
                title=f'{title}',
                input_message_content=input_content,
            )
            FR = [FR]
        # Discord
        else:
            FR = chunkMessage(FR)

        return FR
