'''                                                 UPDATE MANAGER                                                   '''
'''
    This file is intended to run an update check every time the bot is started: it will check for two updates:
    1. Card database update
    2. Rules database update
    
    Once the basics are set up, it will also run the update check daily at 00:00 (in the running computer's timezone)
'''
import hashlib, json, os, requests, asyncio, filetype, sys, aiohttp
from helpers.simplifyjson import JSONSimplifier
from helpers.helpers import simplifyString

DAY = 86400
HOUR = 3600

class Updater:

    def __init__(self,jsonpath,rulespath,blacklist,picspath):
        self.session = aiohttp.ClientSession()
        self.jsonpath = jsonpath
        self.rulespath = rulespath
        self.rulesurl = "https://media.wizards.com/2021/downloads/MagicCompRules%20202109224.txt"
        self.simplifier = JSONSimplifier(blacklist)
        self.picspath = picspath
        self.jsonurl = "https://mtgjson.com/api/v5/AllPrintings.json"
        self.picURL1 = "https://gatherer.wizards.com/Handlers/Image.ashx?name="
        # insert cardname with spaces as %20 between these two strings
        self.picURL2 = "&type=card"

    def clearHash(self):
        with open(self.jsonpath+".hash.txt",'w') as f:
            f.write("None")
        print("Hash cleared")

    # Check to see if there are any updates for either rules or json
    # Also, download pics indendently from updating json in case there were any issues with the pics files
    async def checkUpdate(self,CardManager):
        while True:
            try:
                # Section for getting json updates
                resp = await self.session.get(self.jsonurl+'.sha256')
                urlhash = await resp.text()
                if not os.path.isfile(self.jsonpath+".hash.txt") or \
                        not open(self.jsonpath+".hash.txt").read() == urlhash:
                    print("New JSON hash found. updating.")
                    await self._updateJSON()
                else:
                    print("JSON hash not updated")
                # updaitng card images
                await self._downloadPics()
                # section for getting rules updates
                resp = await self.session.get(self.rulesurl)
                urlhash = await resp.read()
                if not os.path.isfile(self.rulespath+".hash.txt") or \
                        not open(self.rulespath+".hash.txt").read() == hashlib.sha224(urlhash).hexdigest():
                    print("New rules hash found. updating.")
                    await self._updateRules()
                CardManager.update()
                await asyncio.sleep(DAY)
            except:
                print("Wizards offline, waiting one hours")
                await asyncio.sleep(HOUR)

    # Update the json if necesasry
    async def _updateJSON(self):
        try:
            print("Downloading full json")
            resp = await self.session.get(self.jsonurl)
            download = self.simplifier.simplify(await resp.json())
        except:
            print("Problem in downloading JSON file.")
            raise
        with open(self.jsonpath,'w') as jsonfile:
            print("Saving modified JSON")
            json.dump(download,jsonfile)
        with open(self.jsonpath + ".hash.txt", 'w') as f:
            resp = await self.session.get(self.jsonurl + '.sha256')
            f.write(await resp.text())
            print("Updated JSON hash")

    # Download pics one by one
    # Saves them all in one dir so there are no duplicates
    async def _downloadPics(self):
        print("Loading JSON file")
        download = json.load(open(self.jsonpath))
        newcards = 0
        existingcards = 0
        if not os.path.isdir(self.picspath):
            os.mkdir(self.picspath)
        print("Downloading sets:",end=" ")
        try:
            setlevel = download['data']
            # s will be a dictionary key
            for s in setlevel:
                print(s,end=" ")
                sys.stdout.flush()
                # c will be a dictionary of the card itself
                for c in setlevel[s]['cards']:
                    cardpath = self.picspath+'/'+simplifyString(c['name'])
                    if os.path.isfile(cardpath+'.jpg') or os.path.isfile(cardpath+'.png'):
                        existingcards += 1
                        continue
                    newcards += 1
                    resp = await self.session.get(self.picURL1+c['name']+self.picURL2)
                    downfile = await resp.read()
                    with open(cardpath+'.'+filetype.guess(downfile).extension,'wb') as f:
                        f.write(downfile)
        except:
            print("Wizards is down. Retrying later.")
            raise
        print(f"\nCards downloaded. New cards: {newcards}. Existing cards: {existingcards}")

    # This downloads the rules...
    async def _updateRules(self):
        print("Saving new rules")
        resp = await self.session.get(self.rulesurl)
        newrules = self._simplifyRules([line.strip() for line in await resp.text()])
        with open(self.rulespath,'w') as f:
            f.write(newrules)
            print("New rules saved")
        with open(self.rulespath+".hash.txt",'w') as f:
            resp = await self.session.get(self.rulesurl)
            f.write(hashlib.sha224(await resp.read()).hexdigest())
            print("Rules hash updatd")

    # ... and this is just to cut all the non-rules text out of the rules file, like the credits and stuff
    def _simplifyRules(self,rules):
        print("Simplifying rules")
        newrules = ""
        creditscount = 0
        for rule in rules:
            if rule[0] != '1' and not newrules:
                continue
            elif rule.split()[0] == 'Credits':
                creditscount += 1
            elif rule.split()[0] == 'Glossary':
                continue
            elif creditscount == 2:
                break
            else:
                newrules += rules + '\n'
        return newrules