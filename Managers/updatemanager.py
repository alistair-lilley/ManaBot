'''                                                 UPDATE MANAGER                                                   '''
'''
    This file is intended to run an update check every time the bot is started: it will check for two updates:
    1. Card database update
    2. Rules database update
    
    Once the basics are set up, it will also run the update check daily at 00:00 (in the running computer's timezone)
'''
import hashlib, json, os, aiohttp, asyncio
from helpers.simplifyjson import JSONSimplifier

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

    # Check to see if there are any updates for either rules or json
    async def checkUpdate(self):
        while True:
            if not open("hash"+self.jsonpath).read() == await self.session.get(self.jsonurl+'.sha256').text():
                await self._updateJSON()
            if not open("hash"+self.rulespath.read()) == hashlib.sha224(await self.session.get(self.rulesurl).read()).hexdigest():
                await self._updateRules()
            await asyncio.sleep(86400)

    # Update the json if necesasry
    async def _updateJSON(self):
        download = self.simplifier.simplify(json.loads(await self.session.get(self.jsonurl).json()))
        with open(self.jsonpath) as jsonfile:
            json.dump(download,jsonfile)
        await self._downloadPics(download)

    # Download pics one by one
    # This saves them into folders based on their set, kinna like cockatrice
    # Might want to try to reduce repeat card images?
    async def _downloadPics(self,download):
        try:
            setlevel = download['data']
            # s will be a dictionary key
            for s in setlevel:
                currpath = self.picspath+'/'+s+'/'
                if not os.path.isdir(currpath):
                    os.mkdir(currpath)
                # c will be a dictionary of the card itself
                for c in setlevel[s]['cards']:
                    with open(currpath+c+'.jpg','wb') as f:
                        downloadpic = await self.session.get(self.picURL1+c['name']+self.picURL2).read()
                        f.write(downloadpic)
        except aiohttp.ClientError:
            print("Wizards is down. Retrying later.")
            raise

    # This downloads the rules...
    async def _updateRules(self):
        newrules = self._simplifyRules([line.strip() for line in await self.session.get(self.rulesurl).text()])
        with open(self.rulespath,'w') as f:
            f.write(newrules)

    # ... and this is just to cut all the non-rules text out of the rules file, like the credits and stuff
    def _simplifyRules(self,rules):
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