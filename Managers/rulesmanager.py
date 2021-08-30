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
import re
from setupfiles.helpers import *

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
# 1. --> ['1','']
# 100. --> ['100','']
# 100.2. --> ['100','1','']
# 100.2a --> ['100','1a']



class RulesMgr:
    def __init__(self,filename,bothelp):
        self.cmds = ['!rule','!rules','!help']
        self.bothelp = open(bothelp).read()
        # get rules and kws
        self.rules, self.kws = self._readRules(filename)
        # make a list for edit dist
        self.kwlist = list(self.kws)
        # merge sort list
        mS(self.kwlist)

    async def handle(self,cmd,query):
        if cmd in ['!rule','!rules']:
            # If in rules, return rule
            if query in self.rules:
                r = self.rules[query]
            # If in kws, return kw
            elif query in self.kws:
                r = self.kws[query]
            # If it's a number but not a rule, say rule not found
            elif query[0] in NUMERALS:
                r = "Rule not found"
            # If it's clearly a keyword mistype, return similar keywords
            else:
                r = "Keyword not found... Did you mean:\n"+"\n".join(findSimilar(self.kwlist,query))
            return [r,None,None]
        elif cmd in ['!help']:
            return [self.bothelp,None,None]


    # Read in rules as list, then get the stuff from _addAllRules
    def _readRules(self,filename):
        lines = [line.strip() for line in open(filename)]
        return self._addAllRules(lines)

    # Get the rule type
    def _ruleType(self,line):
        # Skip line if its empty or if its "example"
        if not line or line.split()[0] == "Example:":
            return "SKIP"
        rule = line.split()[0].split('.')
        # catch if keyword, not rule
        if rule[0][0] not in NUMERALS:
            return "KW"
        # catch if there are 3 periods
        elif len(rule) == 3:
            return "###.#."
        # catch if it only has 1
        elif len(rule[0]) == 1:
            return "#."
        # catch if theres a letter
        elif len(rule) > 1 and re.search("[a-z]", rule[1]):
            return "###.#A"
        # else just 3
        elif len(rule[0]) == 3:
            return "###."

    # Get all of the rules and keywords as 2 dicts
    def _addAllRules(self,rules):
        # initilaize dicts
        allRules = dict()
        allKWs = dict()
        r = 0
        # For each line
        while r < len(rules):
            # get rule and rule type
            rule = rules[r]
            rtype = self._ruleType(rule)
            # If it's a newline or if it's "Example:", skip
            if rtype == "SKIP":
                pass
            # If it's a keyword, add keyword
            elif rtype == "KW":
                allKWs.update(self._addRule(rule.lower(), rtype, r, rules))
                # Once you're in KW section, skip lines until you pass a newline
                while r+1 < len(rules):
                    if not rules[r+1]:
                        r += 1
                        break
                    r += 1
            # otherwise, add the rule
            else:
                allRules.update(self._addRule(simplifyString(rule.split()[0]), rtype, r, rules))
                #print(allRules)
            r += 1
        # gib bacc
        return allRules, allKWs

    # Add a single rule/kw
    def _addRule(self, rule, rtype, idx, allrules):
        # setup: start dict, get rule type of original rule, and get ruletype of curr line
        d = dict()
        currt = self._ruleType(allrules[idx])
        # Do while simulation
        while True:
            # If it's not a keyword, or if its a ###.#A, a newline, or a SKIP in a ###. rule, skip this line
            if (rtype == "###." and currt in ["###.#A","SKIP"]) or not allrules[idx]:
                idx += 1
                currt = self._ruleType(allrules[idx])
                # Break out if it hath found the same rule
                if (rtype != "KW" and currt == rtype) or allrules[idx] == "Glossary":
                    break
                continue
            # Otherwise, add the rule
            else:
                d[rule] = d.get(rule, "") + allrules[idx] + '\n'
            # Increment and get the next rule
            idx += 1
            # Break out if you're at the end of the rules
            if idx == len(allrules):
                break
            # If its a kewyord, end on newline
            if not allrules[idx] and rtype == "KW":
                break
            # Skip newlines
            while not allrules[idx]:
                idx += 1
            # Get the new rule (aka first word of line)
            currt = self._ruleType(allrules[idx])
            # Break if the new rule is the same as the current rule
            if (rtype != "KW" and currt == rtype) or allrules[idx] == "Glossary":
                break
        # Return the dict
        return d



    # Chunkify it in case discord cant handle the LENGTH
    def _chunkMessage(self,data):
        msgmax = 1999
        chunk = [data]
        # If the data is more than 2000 characters,
        if len(data) > msgmax:
            # break it into two
            chunk = [data[:msgmax], data[msgmax:]]
            # Then break it until it's in chunks of 2000 characters
            while len(chunk[-1]) > msgmax:
                chunk = chunk[:-1] + [chunk[-1][:msgmax]] + [chunk[-1][msgmax:]]
        return chunk