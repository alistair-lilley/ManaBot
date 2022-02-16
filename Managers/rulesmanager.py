'''                                                 RULES.TXT PARSER                                                 '''
'''
    This file is to parse the rules.txt file into a dictionary for easy lookup
    It parses to two dictionaries: keywords and rules
    The keyword dictionary is a keyword paired with a short rule description, which usually includes a numerical code 
    for the full rules about that keyword.
    The rules dictionary is numerical codes paired with full rules -- rules with children list the numbers for the 
    children.

    The file will be formatted as such:
    
    ```
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
    ```
    
    There are 4 types of rules and keywords, which can be broken up into lists, and subsequently tokens, as such:
    value       list                token
    1.          ['1','']            #.
    100.        ['100','']          ###.
    100.1.      ['100','1','']      ###.#.
    100.1a      ['100','1a']        ###.#A
    Keyword     []                  KW
'''
import re
from helpers.helperfns import *


class RulesMgr:
    def __init__(self,filename,bothelp):
        self.cmds = ['!rule','!rules','!help']
        self.bothelp = open(bothelp).read()
        self.rules, self.kws = self._readRules(filename)
        self.kwlist = list(self.kws)
        smS(self.kwlist)

    async def handle(self,cmd,query):
        if cmd in ['!rule','!rules']:
            # determines and retrieves if the query is a rule or keyword
            if query in self.rules:
                r = self.rules[query]
            elif query in self.kws:
                r = self.kws[query]
            # this specifically catches if the user inputs a number, which would correspond to a number rules, but it is
            #   not a real rule; if it's a keyword we can find the closest match, but if its a number it just fails
            elif query[0] in NUMERALS:
                r = "Rule not found"
            else:
                r = "Keyword not found... Did you mean:\n"+"\n".join(findSimilar(self.kwlist,query))
            return [r,None,None]
        elif cmd in ['!help']:
            return [self.bothelp,None,None]

    def _readRules(self,filename):
        lines = [line.strip() for line in open(filename)]
        return self._addAllRules(lines)

    # Get the rule type, kind of a mini-tokenizer
    def _ruleType(self,line):
        if not line or line.split()[0] == "Example:":
            return "SKIP"
        rule = line.split()[0].split('.')
        if rule[0][0] not in NUMERALS:
            return "KW"
        elif len(rule) == 3:
            return "###.#."
        elif len(rule[0]) == 1:
            return "#."
        elif len(rule) > 1 and re.search("[a-z]", rule[1]):
            return "###.#A"
        elif len(rule[0]) == 3:
            return "###."

    def _addAllRules(self,rules):
        allRules = dict()
        allKWs = dict()
        r = 0
        while r < len(rules):
            rule = rules[r]
            rtype = self._ruleType(rule)
            if rtype == "SKIP":
                pass
            elif rtype == "KW":
                allKWs.update(self._addRule(rule.lower(), rtype, r, rules))
                # Once you're in KW section, skip lines until you pass a newline
                while r+1 < len(rules):
                    if not rules[r+1]:
                        r += 1
                        break
                    r += 1
            else:
                allRules.update(self._addRule(simplifyString(rule.split()[0]), rtype, r, rules))
            r += 1
        return allRules, allKWs

    # Notes: We want to catch values at most until the next identical key type (e.g. catch all values between 100.
    #       and 200.); we want to break on newlines for KW and we want to skip ###.#A when catching ###.
    #       This means: #. will have #. and ###.; ###. will have ###.#.; ###.#. will have ###.#A; and KW will have non-
    #       KW text values (anything before a newline)
    def _addRule(self, rule, rtype, idx, allrules):
        d = dict()
        currt = self._ruleType(allrules[idx])
        while True:
            if (rtype == "###." and currt in ["###.#A","SKIP"]) or not allrules[idx]:
                idx += 1
                currt = self._ruleType(allrules[idx])
                if rtype != "KW" and currt == rtype:
                    break
                continue
            else:
                d[rule] = d.get(rule, "") + allrules[idx] + '\n'
            idx += 1
            if idx == len(allrules):
                break
            if not allrules[idx] and rtype == "KW":
                break
            while not allrules[idx]:
                idx += 1
            currt = self._ruleType(allrules[idx])
            if rtype != "KW" and currt == rtype:
                break
        return d
