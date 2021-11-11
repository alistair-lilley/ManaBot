import Managers.jsonmanager
import json, time
import os, requests
from setupfiles.selectivejson import SelectiveJSON
from setupfiles.tokenprint import TokenPrinter
from dotenv import load_dotenv

'''
    with ZipFile(zipPath, 'w'):
        zipfile.write('name_of_file',zipContents)
'''

load_dotenv()

hash_path = os.getenv('HASHPATH')
json_path = os.getenv('JSONPATH')
sample_json = os.getenv('JSONSAMPLE')
image_path = os.getenv('JSONIMAGEPATH')

if __name__ == "__main__":
    '''mgr = Managers.jsonmanager.JSONManager()
    mgr.updateHash()
    mgr.resetHash()'''
    # Test tokens first
    myjsonreader = SelectiveJSON(None,None,json_path)
    time_0 = time.time()
    print("Parsing my stuff")
    myjsonreader.parseMain()
    time_1 = time.time() - time_0
    print("Parsing done, in seconds",time_1)
    print("Json itself")
    with open(json_path) as f:
        data = json.load(f)
    time_2 = time.time() - time_1
    print("Json libraryu done, in seconds",time_2)
    print("Processing mine into a json")
    compare = json.dumps(myjsonreader.mainObj)
    time_3 = time.time() - time_2
    print("Processing done, in seconds",time_3)
    print("Comparing")
    assert data == compare
    print("Compare compleete!")
    #myprinter = TokenPrinter(json_path)
    #myprinter.parseAndPrint()