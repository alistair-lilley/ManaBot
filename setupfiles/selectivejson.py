'''                                                 SELECTIVE JSON                                                   '''
'''
    This object is designed to selectively parse a JSON file based on a whitelist and a blacklist  
    It takes in a whitelist, a blacklist, and a JSON file and parses it into a JSON object by 
        1. checking if there is a whitelisted term on a given level, the including only that
        2. checking if there are any blacklisted terms on the same level and adding words that aren't blacklisted
                ***IF AND ONLY IF THERE IS NO WHITELIST ON THAT LEVEL***
'''
import json, sys
from setupfiles.jsontokenizer import *


class SelectiveJSON:

    def __init__(self, whitelist, blacklist, filename):
        self.WL = whitelist
        self.BL = blacklist
        self.tokenizer = Tokenizer(filename,268435455)
        self.mainObj = dict()

    def parseMain(self):
        token = self.tokenizer.readToken()
        while type(token) != End:
            #print("hoi!")
            self.mainObj = self.parseObj()
            token = self.tokenizer.readToken()

    def parseObj(self):
        #print("\n\nstarting parseObj")
        token = self.tokenizer.readToken()
        currObj = dict()
        key = None
        while type(token) != EndObject:
            #print("In parseObj")
            if type(token) == End:
                #print("Fucked up! Ended before it could end. Ended in parseObj")
                sys.exit()
            elif type(token) == Null:
                pass
            elif type(token) == Literal:
                if not key:
                    key = token.val
                    #print("found key!",key)
                else:
                    currObj[key] = token.val
                    #print("found val!",token.val)
                    key = None
            elif type(token) == BeginObject:
                if not key:
                    #print("OBject without key")
                    currObj = self.parseObj()
                else:
                    #print("Making object, key",key)
                    currObj[key] = self.parseObj()
                    key = None
            elif type(token) == BeginArr:
                if not key:
                    #print("Fucked up! There's an array without a key")
                    sys.exit()
                #print("Makey arr, key",key)
                currObj[key] = self.parseArr()
                key = None
            token = self.tokenizer.readToken()
            #print("Token val",token.val)
        #print("Ended obj\n\n")
        return currObj


    def parseArr(self):
        #print("Made it to arr")
        token = self.tokenizer.readToken()
        currArr = []
        while type(token) != EndArr:
            if type(token) == End:
                #print("Fucked up! Ended before it could end. Ended in parseArr")
                sys.exit()
            elif type(token) == Null:
                pass
            elif type(token) == Literal:
                currArr.append(token.val)
            elif type(token) == BeginObject:
                currArr.append(self.parseObj())
            elif type(token) == BeginArr:
                currArr.append(self.parseArr())
            token = self.tokenizer.readToken()
        return currArr