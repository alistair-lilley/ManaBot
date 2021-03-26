# loadImages file
# This file has the function that loads all the image paths to a dictionary
#       As well as records each name in a dictionary where each key is the name all lowercase with no punctuation
#       and the value is the proper, full name
# In addition, this file has a function to remove punctuation from a string
import os
from helpers import stripExt, simplifyName

# Creates two dictionaries recording the path and names of all files given a directory
def loadAllImages(imageDir):
    cardsfile = open('logs/cardLog.txt','w')
    countfile = open('logs/countLog.txt','w')
    cardsToWrite = []
    countToWrite = []
    # Initialize dicts
    imageDict = {} # cardname : path
    nameDict = {} # lowercase+nopunct cardname : proper cardname
    # Loop through subdirs in main dir
    failedDirs = []
    for d in os.listdir(imageDir):
        # Loop through files in subdir
        numFiles = len(os.listdir(imageDir+"/"+d))
        aa = f'Cards in {d}: {numFiles}'
        countToWrite.append(aa)
        count = 0
        for c in os.listdir(imageDir+"/"+d):
            propName, ext = stripExt(c) # Gets the name of the card without the extension
            imageDict[propName] = d # Corresponds card name with subdir
            lowerName = simplifyName(propName.lower()) # Gets the simplified name
            nameDict[lowerName] = propName # Corresponds simplified name with proper name
            bb = f'Card: {d}/{propName}{ext}'
            cardsToWrite.append(bb)
            count += 1
        cc = f'Loaded: {count}'
        countToWrite.append(cc)
        if numFiles != count:
            dd = "Failed to load all files"
            countToWrite.append(dd)
            failedDirs.append(d)
        cardsToWrite.append('\n')
        countToWrite.append('\n')
    ee = "Failed directories:"
    for line in failedDirs:
        ee += ', '+line
    countToWrite.append(ee)
    countToWrite.append(f'Cards loaded: {len(imageDict)}')
    cardsfile.write('\n'.join(cardsToWrite))
    countfile.write('\n'.join(countToWrite))
    cardsfile.close(), countfile.close()
    return imageDict, nameDict, ee # returns both dictionaries
