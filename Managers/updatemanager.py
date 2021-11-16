'''                                                 UPDATE MANAGER                                                   '''
'''
    This file is intended to run an update check every time the bot is started: it will check for two updates:
    1. Card database update
    2. Rules database update
    
    Once the basics are set up, it will also run the update check daily at 00:00 (in the running computer's timezone)
'''
import hashlib, json, os, requests, asyncio, filetype
from helpers.simplifyjson import JSONSimplifier
from helpers.helpers import simplifyString

DAY = 86400
HOUR = 3600

class Updater:

    def __init__(self,jsonpath,rulespath,blacklist,picspath):
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
    async def checkUpdate(self):
        while True:
            try:
                if not os.path.isfile(self.jsonpath+".hash.txt") or \
                        not open(self.jsonpath+".hash.txt").read() ==  requests.get(self.jsonurl+'.sha256').text:
                    print("New JSON hash found. updating.")
                    self._updateJSON()
                else:
                    print("JSON hash not updated")
                if not os.path.isfile(self.rulespath+".hash.txt") or \
                        not open(self.rulespath+".hash.txt").read() == hashlib.sha224( requests.get(self.rulesurl).content).hexdigest():
                    print("New rules hash found. updating.")
                    self._updateRules()
                await asyncio.sleep(DAY)
            except requests.exceptions.RequestException:
                print("Wizards offline, waiting one hours")
                await asyncio.sleep(HOUR)

    # Update the json if necesasry
    def _updateJSON(self):
        with open(self.jsonpath+".hash.txt",'w') as f:
            f.write( requests.get(self.jsonurl+'.sha256').text)
            print("Updated JSON hash")
        try:
            print("Downloading full json")
            download = self.simplifier.simplify(requests.get(self.jsonurl).json())
        except requests.exceptions.RequestException:
            print("Problem in downloading JSON file.")
            raise
        with open(self.jsonpath,'w') as jsonfile:
            print("Saving modified JSON")
            json.dump(download,jsonfile)
        self._downloadPics(download)

    # Download pics one by one
    # This saves them into folders based on their set, kinna like cockatrice
    # Might want to try to reduce repeat card images?
    def _downloadPics(self,download):
        print("Downloading all pics")
        newcards = 0
        existingcards = 0
        if not os.path.isdir(self.picspath):
            os.mkdir(self.picspath)
        try:
            setlevel = download['data']
            # s will be a dictionary key
            for s in setlevel:
                print(f"Downloading set: {s}")
                #currpath = self.picspath+'/'+s+'/'
                currpath = self.picspath+'/ALLPICS/'
                if not os.path.isdir(currpath):
                    os.mkdir(currpath)
                # c will be a dictionary of the card itself
                for c in setlevel[s]['cards']:
                    cardpath = currpath+simplifyString(c['name'])
                    if os.path.isfile(cardpath+'.jpg') or os.path.isfile(cardpath+'.png'):
                        existingcards += 1
                        continue
                    newcards += 1
                    downfile = requests.get(self.picURL1+c['name']+self.picURL2).content
                    with open(cardpath+'.'+filetype.guess(downfile).extension,'wb') as f:
                        f.write(downfile)
        except requests.exceptions.RequestException:
            print("Wizards is down. Retrying later.")
            raise
        print(f"Cards downloaded. New cards: {newcards}. Existing cards: {existingcards}")

    # This downloads the rules...
    def _updateRules(self):
        with open(self.rulespath+".hash.txt",'w') as f:
            f.write(hashlib.sha224( requests.get(self.rulesurl).content).hexdigest())
            print("Rules hash updatd")
        print("Saving new rules")
        newrules = self._simplifyRules([line.strip() for line in  requests.get(self.rulesurl).text])
        with open(self.rulespath,'w') as f:
            f.write(newrules)
            print("New rules saved")

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