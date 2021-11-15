'''                                               JSON SIMPLIFIER                                                    '''
'''
    This program will simplify the JSON file downloaded by the updater into a smaller JSON so that it loads faster
        and requires less space 
    (It simplifies based on a blacklist fed into it)
'''
import json

class JSONSimplifier:

    def __init__(self,blacklist):
        self.blacklist = set(blacklist)

    # Start the program!
    def simplify(self,jsonfile):
        fullobj = json.loads(open(jsonfile).read())
        return self._parseObj(fullobj)

    # Parses dict-like objects
    def _parseObj(self,obj):
        makeObj = dict()
        key = None
        for item in obj:
            if item in self.blacklist:
                continue
            if key:
                if type(obj[item]) == dict:
                    makeObj[key] = self._parseObj(obj[item])
                elif type(obj[item]) == list:
                    makeObj[key] = self._parseList(obj[item])
                else:
                    makeObj[key] = item
            else:
                key = item
        return makeObj

    # Parses list-like objects
    def _parseList(self,L):
        makeList = []
        for item in L:
            if item in self.blacklist:
                continue
            if type(item) == dict:
                makeList.append(self._parseObj(L[item]))
            if type(item) == list:
                makeList.append(self._parseList(L[item]))
        return makeList