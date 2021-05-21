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
NUMERALS = set([str(i) for i in range(0,10)]+["."])
alph = 'abcdefghijklmnopqrstuvwxyz'
ALPH = set(list(alph+alph.upper()))

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

# Shit this was tricky
# Possible combinations:
# 1. --> ['1',''] --> len(2), [0] len(1) --> adds to 3
# 100. --> ['100',''] --> len(2), [0] len(3) --> adds to 5
# 100.2. --> ['100','1',''] --> len(3), [0] len(3), [1] len(1+) --> adds to 7+
# 100.2a --> ['100','1a'] --> len(2), [1].endswith(alpha)

# calculate: len(arr)+sum([len(a) for a in arr])





class RulesMgr:
    def __init__(self,filename,bot=None):
        self.bot = bot
        self.rules, self.keywords = self._readRules(filename)
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
            FR = self._chunkMessage(FR)

        return FR
    
    def _getRuleType(self,rule):
        if rule[-1] not in NUMERALS:
            return -1
        rulesplit = rule.split('.')
        return len(rulesplit)+sum([len(r) for r in rulesplit])
    
    
    # 0 = break, 1 = keep goin, 2 = skip (continue)
    def _checkBreakSkip(self,ruletype,rtext):
        if rtext == '': # gets out or keeps goin if theres a break
            return ((2,0)[ruletype in [3,-1]])
    
        subrulesplit = rtext.split()[0].split('.') # get the rule split on .
    
        if len(subrulesplit[0]) == 1:
            return 1
    
        elif ruletype == 5:
            newsubr = (subrulesplit+["1"],subrulesplit)[subrulesplit[-1] != ''] # get a new subrule if necessary
    
            # Big block
            return ((((int(newsubr[-1][-1] in ALPH) + 1, # gets the return val if has alpha (1 to keep goin, 2 to skip)
                       not len(subrulesplit) == 2)[not subrulesplit[-1]]), # gets val if theres no end
                     2)[rtext.split() == "Example:"]) # skips if example
    
        # otherwise check if its ["100","1",""]
        elif ruletype >= 7:
            return subrulesplit[-1]
    
    
    def _getRule(self,rule,rtext,rules):
        ruletype = self._getRuleType(rule)
        subrules = ""
        text = ' '.join(rtext.split()[1:])
        for sub in rules:
            bs = self._checkBreakSkip(ruletype,sub)
            if bs == 0:
                break
            elif bs == 2:
                continue
            subrules += "\nSubrule: "+sub
        return text+subrules
    
    
    def _readRules(self,filename):
        with open(filename) as f:
            text = [line.strip() for line in f]
    
        rules = {}
        keywords = {}
    
        # If the rule is empty, reset current rule and keyword, then keep goin
        for l in range(len(text)):
            line = text[l]
            if not line:
                continue
    
            # Get the rule as the first word of the rules
            first = line.split()[0]
    
            if set(first[0]).issubset(NUMERALS):
                rules[first] = self._getRule(first, line, text[l+1:])
    
            elif first != "Example:":
                keywords[first] = self._getRule(first, line, text[l+1:])
    
        return rules, keywords
    
    
    
    # Chunkify it in case discord cant handle the LENGTH
    def _chunkMessage(self,data):
        r = [data]
        if len(data) > 2000:
            r = [data[:2000], data[2000:]]
            while len(r[-1]) > 2000:
                r = r[:-1] + [r[-1][:2000]] + [r[-1][2000:]]
        return r