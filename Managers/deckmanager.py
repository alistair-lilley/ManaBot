'''                             COD to TXT converter                            '''
'''
        This file converts .cod files to .txt files; .cod files are an .xml format file
        Specifically, it will take a filepath for a .cod and write a new file as a .txt with the same name
'''
import os, shutil, asyncio, requests, re
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from setupfiles.helpers import stripExt, simplifyString

NUMERALS = {str(i) for i in range(0, 9)}

class DeckMgr:
    def __init__(self, path_to_bot, deckDirs, CardManager):
        self.cmds = ['!cleardecks','!checkban','!checkbans','!analyze']
        self.ptb = path_to_bot
        self.dirs = deckDirs
        self.cm = CardManager

    # Generic command handler. It processing attachments and/or commands as needed
    async def handle(self,cmd,query,attached=None):
        # Might not be working?
        if cmd and cmd == "!cleardecks":
            self._cleardecks()
            return ["Decks cleared.",None,None]
        if attached:
            # Get file data stuff; name, url, raw data
            fullname = attached[0]
            furl = attached[1]
            r = requests.get(furl)
            # Save the file data
            srcpath = self.ptb+"/data/toparse/"+fullname
            open(srcpath, 'wb').write(r.content)
            # Convert!
            decks = self._convert(fullname)
            # Checks for command and throws error if wrong cmd
            if cmd:
                if cmd in ["!checkban","!checkbans"]:
                    return ['\n'.join([self._checkbanned(d[0]) for d in decks]),None,None]
                elif cmd == "!analyze":
                    return ['\n'.join([self._analyze(d[0]) for d in decks]),None,None]
                else:
                    return [f"Command {cmd} not found. Did you mean '!checkban' or '!analyze'?",None,None]
            # otherwise just spit out the decklists as txt's
            else:
                return [None,None,decks]

    ###############################################################
    ###############################################################
    ###############################################################

    # Convert overall

    # Main convert function
    def _convert(self, f):
        # parse name and get paths
        name, ext = stripExt(f)
        srcpath = self.ptb + "/data/toparse/"
        textpath = self.ptb + "/data/txts/"
    
        # flist is a list of tuples of (path, filename) so that it uploads the file and a palatable name for it
        # Collect it dynamically
        if ext in ['.cod', '.mwDeck', '.txt']:
            self._convertDeck(srcpath, textpath, name, ext)
            flist = [(textpath + name + '.txt', name + '.txt')]
        elif ext == '.mwDeck':
            self._convertDeck(srcpath, textpath, name, ext)
            flist = [(textpath + name + '.txt', name + '.txt')]
        elif ext == '.zip':
            flist = self._convertZip(f)
        else:
            flist = [None]
        # return list of file paths
        return flist

    ###############################################################
    ###############################################################
    ###############################################################

    # Convert the zips
    
    # Converts a whole zip by unzipping it, then converting each file within the unzipped dir
    # There may be filename collisions but... that's a later project
    def _convertZip(self, Z):
        zipname, zext = stripExt(Z)
        # mkdir with same name as zip
        subparse = self.ptb + "/data/toparse/" + zipname
        subtext = self.ptb + "/data/txts/" + zipname
        # Make sure there aren't any of these dirs, then make them
        # Baseically ensure they exist and are empty
        if os.path.exists(subparse):
            shutil.rmtree(subparse)
        if os.path.exists(subtext):
            shutil.rmtree(subtext)
        os.mkdir(subparse)
        os.mkdir(subtext)
        # extract all to that dir
        with ZipFile(self.ptb + "/data/toparse/" + Z) as zf:
            zf.extractall(subparse)
        # Convert all the files and collect their paths,names
        flist = []
        return self._convertDir(subparse, subtext, flist)
    
    
    # Converts a directory recursively
    def _convertDir(self, dirpath, textpath, flist):
        for df in os.listdir(dirpath):
            # Recurse if theres a dir
            if os.path.isdir(dirpath + '/' + df):
                flist = self._convertDir(dirpath + '/' + df, textpath, flist)
            # Convert if it's a cod or mwDeck
            else:
                fname, fext = stripExt(df)
                if fext in ['.cod']:
                    self._convertDeck(dirpath + '/', textpath + '/', fname, fext)
                    flist.append((textpath + '/' + fname + '.txt', fname + '.txt'))
                elif fext == '.mwDeck':
                    flist.append("Currently .mwDecks are not supported.")
        # return list of file paths
        return flist

    ###############################################################
    ###############################################################
    ###############################################################

    # Convert individual decks
    
    # Convert a deck
    # Basically goes through each possible extension and runs convert on it
    def _convertDeck(self, srcpath, textpath, name, ext):
        # -elif ext == '.mwDeck':
        # cards = self._convertmwDeck(srcpath + name + ext)
        if ext == '.cod':
            cards = self._convertCod(srcpath, name + ext)
        elif ext in ['.txt','.mwDeck']:
            cards = [line for line in open(srcpath + name + ext)]
        elif ext in ['.mwDeck',".txt"]:
            cards = self._convertmwDeckTxt(srcpath + name + ext)
        # Just in case, so it doesn't completely crash
        else:
            cards = ['error']
        # Write joined list of cards
        with open(textpath + name + '.txt', 'w') as wf:
            wf.write('\n'.join(cards))


    # Converts a .cod file, which is basically an .xml file
    def _convertCod(self, filepath, namefull):
        fullpath = filepath + namefull
        CODtree = ET.parse(fullpath)  # Get the cod file as an xml tree
        root = CODtree.getroot()  # get root
        cards = []  # initialize cards list
        # Loop through etree
        for child in root:
            if child.tag in ['deckname','comments'] and child.text:
                for t in child.text.split('\n'):
                    cards.append("//"+t)
            # Loop through children of a card zone
            if child.tag == 'zone':
                for c in child:
                    # Get the number of a type of card along with what the card is (e.g. '1 Sol Ring' or '10 Plains')
                    cardline = c.attrib['number'] + " " + c.attrib['name']
                    # If it's sideboarded, add 'SB: '
                    if child.attrib['name'] != 'main':
                        cardline = 'SB: ' + cardline
                    # append to all cards
                    cards.append(cardline)
        # return as list of cards
        return cards

    # Converts .mwDeck, which is basically a .txt file formatted differently from how Cockatrice likes them pasted in
    def _convertmwDeckTxt(self, filepath):
        # Process it like a .txt
        deckFile = [line.split() for line in open(filepath)]
        cards = []
        for line in deckFile:
            # ignores comment lines
            if line[0] == '//':
                cards.append(" ".join(line)+'\n')
            # Adjusts SB lines since its a little different
            else:
                cards.append(self._cutBrackets(line))
        # return as list of cards
        return cards

    def _cutBrackets(self,line):
        return ' '.join([l for l in line if l[0] != '['])

    ###############################################################
    ###############################################################
    ###############################################################

    # Bans

    # Checks cards against a banlist; only works for EDH
    def _checkbanned(self, f):
        # load banlists and decklist
        singlebanned = [line for line in open(self.ptb + "/data/bans/EDHsingleban.txt")]
        multibanned = [line for line in open(self.ptb + "/data/bans/EDHmultiban.txt")]
        deck = [line[2:] for line in open(f)]
        # go through sp bans
        sbans = [f"**Deck: {f.split('/')[-1]}**\n*Single player EDH bans:*\n"]
        check = list(set(deck).intersection(set(singlebanned))) # check the intersection of the two things
        if not check:
            sbans.append("None\n")
        else:
            sbans += check
        # repeat with mp
        sbans = ''.join(sbans)
        mbans = ["*Multiplayer EDH bans:*\n"]
        check = list(set(deck).intersection(set(multibanned)))
        if not check:
            mbans.append("None")
        else:
            mbans += check
        mbans = ''.join(mbans)
        allbans = sbans + mbans + '\n\n'
        # return as string
        return allbans

    ###############################################################
    ###############################################################
    ###############################################################

    # analyze

    def _colorID(self,carddata,data):
        if "Color ID" in carddata:
            if "Land" in carddata["Type"]:
                data["lands"][carddata["Color ID"]] = data["lands"].get(carddata["Color ID"],0)+1
            for col in carddata["Color ID"]:
                data["color"][col] = data["color"].get(col,0)+1
        else:
            data["color"]["C"] = data["color"].get("C",0)+1
        return data["color"]

    def _manaCost(self,carddata,data):
        if "Mana Cost" in carddata:
            for cos in carddata["Mana Cost"]:
                if cos in NUMERALS:
                    data["costs"]["N"] = data["costs"].get("N", 0)
                    data["costs"]["N"] = data["costs"]["N"] + int(cos)
                elif cos in "{/}":
                    continue
                else:
                    data["costs"][cos] = data["costs"].get(cos, 0) + 1
        return data["costs"]

    def _parseData(self,data):
        for d in data:
            if type(data[d]) == dict:
                data[d] = d + ": " + ', '.join([f"**{subd}**: {str(data[d][subd])}" for subd in data[d]])
            else:
                data[d] = d + ": " + str(data[d])
        return data

    def _getColornCost(self,c,data):
        basictypes = ["Artifact","Instant","Sorcery","Creature","Land","Enchantment","Planeswalker"]
        card = c.split()[1:]
        card = simplifyString(' '.join(card))
        carddata = self.cm.getRaw(card)
        # get color IDs
        data["color"] = self._colorID(carddata,data)
        # get costs
        data["costs"] = self._manaCost(carddata,data)
        found = False
        for t in basictypes:
            if re.search(t,carddata["Type"]):
                data["cardtypes"][t] = data["cardtypes"].get(t,0)+1
                found = True
        if not found:
            data["cardtypes"][carddata["Type"]] = data["cardtypes"].get(carddata["Type"],0)+1
        return data, found

    def _analyze(self, f):
        # get decklist
        deck = [line.strip() for line in open(f)]
        datatypes = ["color","costs","converted","avgcost","lands","cardtypes"]
        data = {dat:dict() for dat in datatypes}
        for c in deck:
            # Make this a fn - A
            if c[0] not in NUMERALS:
                continue
            data, found = self._getColornCost(c,data)
            if not found:
                return False
        data["converted"] = sum([data["costs"][t] for t in data["costs"]])
        data["avgcost"] = round(data["converted"] / (sum([int(c[0]) for c in deck if c[0] in NUMERALS]) - sum([data["lands"][t] for t in data["lands"]])), 2)
        data = self._parseData(data)
        return '\n'.join([data[d] for d in data])


    def _combineCost(self,mana):
        ttl = 0
        i = 0
        while i < len(mana):
            if i in NUMERALS:
                ttl += int(i)
            elif i != "{":
                while i != "}":
                    i += 1
            ttl += 1
            i += 1
        return ttl




    ###############################################################
    ###############################################################
    ###############################################################

    # clear
    
    # Clears all decks from parse and text dirs
    def _cleardecks(self):
        for p in self.dirs:
            for d in os.listdir(self.ptb+p):
                if os.path.isdir(self.ptb+p+d):
                    shutil.rmtree(self.ptb+p+d)
                else:
                    os.remove(self.ptb+p+d)
    
    async def scheduledClear(self):
        while True:
            await asyncio.sleep(10800)
            self._cleardecks()
