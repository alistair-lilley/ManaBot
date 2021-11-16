'''                                               JSON SIMPLIFIER                                                    '''
'''
    This program will simplify the JSON file downloaded by the updater into a smaller JSON so that it loads faster
        and requires less space 
    (It simplifies based on a blacklist fed into it)
'''

class JSONSimplifier:

    def __init__(self,blacklist):
        self.blacklist = set([line.strip() for line in open(blacklist)])

    # Start the program!
    def simplify(self,jsonobj):
        print("Simplifying JSON")
        return self._parseObj(jsonobj)

    # Parses dict-like objects
    def _parseObj(self,obj):
        makeObj = dict()
        for item in obj:
            if type(item) not in [list,dict] and item in self.blacklist:
                continue
            elif type(obj[item]) == dict:
                makeObj[item] = self._parseObj(obj[item])
            elif type(obj[item]) == list:
                makeObj[item] = self._parseList(obj[item])
            else:
                makeObj[item] = obj[item]
        return makeObj

    # Parses list-like objects
    def _parseList(self,L):
        makeList = []
        for item in L:
            if type(item) not in [list,dict] and item in self.blacklist:
                continue
            elif type(item) == dict:
                makeList.append(self._parseObj(item))
            elif type(item) == list:
                makeList.append(self._parseList(item))
            else:
                makeList.append(item)
        return makeList