'''                                                 RULES.TXT PARSER                                                 '''
'''
    This file is to parse the rules.txt file into a dictionary for easy lookup
    It parses to two dictionaries: keywords and rules
    The keyword dictionary is a keyworkd paired with a short rule description, which includes a numerical code for the
    full rules.
    The rules dictionary is numerical codes paired with full rules -- rules with children list the numbers for the 
    children.
'''
from helpers import simplifyString

numerals = {str(i) for i in range(0,10)}
alph = set(list('abcdefghijklmnopqrstuvwxyz'))

def readRules(filename):
    with open(filename) as f:
        text = [line.strip() for line in f]
    print(text[0])

    rules = {}
    keywords = {}
    curRule = ''
    curKeyw = ''
    for rule in text:
        if not rule:
            curRule = ''
            curKeyw = ''
            continue
        r = rule.split()[0]
        if len(curRule) > 0:
            rules[curRule] += '\n'+rule
        elif len(curKeyw) > 0:
            keywords[curKeyw] += '\n'+rule
        elif set(r[0].lower()).issubset(alph):
            curKeyw = rule
            keywords[curKeyw] = rule
        elif set(r[0]).issubset(numerals):
            curRule, rules = addRule(rules, curRule, rule)

    return rules, keywords


# Shit this was tricky
# Possible combinations:
# 1. --> ['1','']
# 100. --> ['100'.'']
# 100.2. --> ['100','2','']
# 100.2a --> ['100','2a']
def addRule(rules, curRule, rule):
    #print("ru",rules)
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



class RulesMgr:
    def __init__(self,filename):
        self.rules, self.keywords = readRules(filename)
        self.simplerules = {simplifyString(rule):rule for rule in self.rules}
        self.simplekeywords = {simplifyString(keyword):keyword for keyword in self.keywords}

    def runCmd(self,query):
        simplequery = simplifyString(query)
        if simplequery in self.simplekeywords:
            fullkw = self.simplekeywords[simplequery]
            fullrule = self.keywords[fullkw]
            return fullrule
        elif simplequery in self.simplerules:
            fullr = self.simplerules[simplequery]
            fullrule = self.rules[fullr]
            return fullr+' '+fullrule
        else:
            return "No results"


if __name__ == "__main__":
    RulesManager = RulesMgr("rules.txt")
    #print(RulesManager.rules)
    keyws = [keyw for keyw in RulesManager.keywords]
    '''for keyw in keyws:
        print(keyw)'''
    #simplekeys = RulesManager.
    b=RulesManager.getKeyword("Flying")
    a=RulesManager.getKeyword("ashas")

    print(a)
    print(b)

    C = RulesManager.getRule("702.9.")
    print(C)
    d = RulesManager.getRule("702.9a")
    print(d)