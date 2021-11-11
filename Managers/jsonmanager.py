'''                                                     JSON Manager                                                  '''
'''
    This manager will download new JSONs based on the updated card sets and download pictures as necessary
    
    Note: once this is fully operational, the rest of the bot will have to be changed so that it references
        the data downloaded by this part of the bot, not Cockatrice
'''
import os, requests
from dotenv import load_dotenv

'''
    with ZipFile(zipPath, 'w'):
        zipfile.write('name_of_file',zipContents)
'''

load_dotenv()

hash_path = os.getenv('HASHPATH')
json_path = os.getenv('JSONPATH')
image_path = os.getenv('JSONIMAGEPATH')

class JSONManager:
    def __init__(self):
        self.hashFile = hash_path
        self.dataFile = json_path
        self.imageDir = image_path
        self.dataUrl = "https://mtgjson.com/api/v5/AllPrintings.json"
        self.picURL1 = "https://gatherer.wizards.com/Handlers/Image.ashx?name="
        # insert cardname with spaces as %20 between these two strings;
        self.picURL2 = "&type=card"

    # Works
    # resets hash for testing purposes
    def resetHash(self):
        with open(self.hashFile,'w') as f:
            f.write("none")
        print("Hash reset")

    # works
    # updates hash to check for updates to deck
    def updateHash(self):
        hashreq = requests.get(self.dataUrl+'.sha256')
        if not os.path.isfile(self.hashFile):
            with open(self.hashFile,'w') as f:
                f.write("none")
        if hashreq.text == open(self.hashFile).read() and os.path.isfile(self.dataFile):
            print("No hash update, file found")
            return
        with open(self.hashFile,'w') as f:
            f.write(hashreq.text)
        print("Hash updated successfully")
        print("Updating JSON")
        self._updateJSON()

    # works
    # downloads the updated json
    def _updateJSON(self):
        JSONdata = requests.get(self.dataUrl)
        with open(self.dataFile,'wb') as f:
            f.write(JSONdata.content)
        print("JSON Downloaded")

    # HERE COMES THE HARD ONE
    def simplifyJSON(self):
        pass

    def updateImages(self):
        pass