'''                                                    DICE                                                          '''
'''
    Dice roller
    
    Sample:
    XdY[dk][hl]Z+N
    
    Needs work
'''
from random import randint
from helpers.helperfns import *


# Manage dicies!!
class DiceMgr:

    def __init__(self):
        #self.cmds = ['!roll','!r']
        self.cmds = []
        pass

    async def handle(self,cmd,query):
        '''if cmd in ['!roll','!r']:
            return [self._roll(query),None,None]'''
        pass

    # Dropping system
    def _drop(self,nums,dklh,dropnum):
        nmS(nums)
        maxtomin = nums[:dropnum]
        mintomax = nums[dropnum:]
        revmaxtomin = nums[:len(nums)-dropnum]
        revmintomax = nums[len(nums)-dropnum:]
        if dklh in ["dl","d"]:
            return mintomax, maxtomin
        elif dklh == "dh":
            return maxtomin, mintomax
        elif dklh == "kl":
            return revmaxtomin, revmintomax
        elif dklh == "kh":
            return revmintomax, revmaxtomin
        elif dklh == "nd":
            return nums, []

    # Redo this in a bit: parse it!
    # gonna leave it as the mess it is for a bit tho
    def _parse(self,query):
        # Set defaults
        num, dtype, dklh, dropnum, mod = 1, 20, 'nd', -1, 0
        allres = [num, dtype, dklh, dropnum, mod]

        if query[0] in NUMERALS:
            allres[0], query = int(query.split('d')[0]), 'd'+'d'.join(query.split('d')[1:])
        idx = 1
        if query[idx] not in NUMERALS:
            return 'error'
        # Start looping
        # Get Y of dY
        allres[1] = ''
        allres[1], idx = makeNum(query,idx)
        # Return if it's at the end
        if idx == len(query):
            return allres
        if query[idx] not in 'dk+-':
            return 'error'
        # If its dk,
        if query[idx] in 'dk':
            # Get the dk
            allres[2] = query[idx]
            idx += 1
            # If its not lh, jump
            if query[idx] not in 'lh' and query[idx-1] != 'd':
                return 'error'
            if query[idx] in 'lh':
                # Get the lh
                allres[2] += query[idx]
                # If it ends, give error
                idx += 1
            if idx == len(query):
                return 'error'
            # otherwise get drop num
            allres[3] = ""
            allres[3], idx = makeNum(query, idx)
            # get out if it's end
            if idx == len(query):
                return allres
        # If its invalid, break
        if query[idx] not in '+-':
            return 'error'
        if query[idx] == '+':
            neg = False
        elif query[idx] == '-':
            neg = True
        idx += 1
        # get num
        allres[4] = ""
        allres[4], idx = makeNum(query, idx)
        if neg:
            allres[4] = -allres[4]
        # Woohoo!!
        return allres

    # Actually calculate the roll stuff
    def _roll(self,query):
        result = self._parse(query)
        if result == 'error':
            return "Incorrect format. Please enter `XdY[dk|lh]Z+N`"
        num, dtype, dklh, dropnum, mod = result
        rolled = [randint(1,dtype) for _ in range(num)]
        r = ', '.join([str(roll) for roll in rolled])
        kept, dropped = self._drop(rolled,dklh,dropnum)
        ttl = sum(kept) + mod
        k = ', '.join([str(keep) for keep in kept])
        d = ', '.join([str(drop) for drop in dropped])
        if not k:
            k = "None"
        if not d:
            d = "None"
        return f"Rolled `{query}`\nRoll results: `{r}`\nKept `{k}`\nDropped `{d}`\nTotal `{ttl}`."