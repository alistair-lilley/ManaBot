'''                                                 SELECTIVE JSON                                                   '''
'''
    FUCK
'''
import sys
from setupfiles.jsontokenizer import *

MAX = 10000

class TokenPrinter:

    def __init__(self, filename):
        self.tokenizer = Tokenizer(filename,268435455)
        self.filedata = open("data/json/test.txt",'w')

    def parseAndPrint(self):
        token = self.tokenizer.readToken()
        i = 0
        while type(token) != End and i < MAX:
            print(type(token),token.val)
            self.filedata.write(type(token).__name__+': '+token.val+'\n')
            token = self.tokenizer.readToken()
            i += 1
        print(type(token),token.val)
        self.filedata.write(type(token).__name__+': '+token.val+'\n')
