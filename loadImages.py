# loadImages file
# This file has the function that loads all the image paths to a dictionary
#       As well as records each name in a dictionary where each key is the name all lowercase with no punctuation
#       and the value is the proper, full name
# In addition, this file has a function to remove punctuation from a string
import os
from helpers import stripExt, simplifyName

# Creates two dictionaries recording the path and names of all files given a directory
# Also includes error logs that are sent in direct messages to me
def loadAllImages(imageDir):
    cardsfile = open('logs/cardLog.txt','w')
    countfile = open('logs/countLog.txt','w')
    # Some debugging stuff -- variables to keep track of what cards have been added and what cards have been counted
    cardsToWrite = []
    countToWrite = []
    imageDict = {} # cardname : path
    nameDict = {} # lowercase+nopunct cardname : proper cardname
    dircount = len(os.listdir(imageDir)) # Count the number of directories for debugging
    countToWrite.append(f'Total dirs: {dircount}') # debugging
    dirscounted = 0 # initialize counting dirs
    failedDirs = [] # set up what directories didn't load everything
    for d in os.listdir(imageDir):
        dirscounted += 1 # count the dir
        # Loop through files in subdir
        numFiles = len(os.listdir(imageDir+"/"+d))
        # Debugging stuff -- count files in dir for counting files debugging
        countToWrite.append(f'Cards in {d}: {numFiles}')
        count = 0 # count cards
        for c in os.listdir(imageDir+"/"+d):
            propName, ext = stripExt(c) # Gets the name of the card without the extension
            imageDict[propName] = d # Corresponds card name with subdir
            lowerName = simplifyName(propName) # Gets the simplified name
            nameDict[lowerName] = propName # Corresponds simplified name with proper name
            cardsToWrite.append(f'Card: {d}/{propName}{ext}')
            count += 1
        countToWrite.append(f'Loaded: {count}')
        # Checks if the directory didn't get all the files, and adds to error logging if it didn't
        if numFiles != count:
            countToWrite.append("Failed to load all files")
            failedDirs.append(d)
        cardsToWrite.append('\n')
        countToWrite.append('\n')
    print(f'Counted dirs: {dirscounted}')
    ee = "\nFailed directories: "
    for line in failedDirs:
        ee += line+', '
    if not failedDirs:
        ee += 'None -- all loaded\n'
    if dircount != dirscounted:
        ee += f'Error: {dircount - dirscounted} directories missing'
    else:
        ee += f'All dirs loaded ({dircount} of {dirscounted})'
    countToWrite.append(ee)
    countToWrite.append(f'Cards loaded: {len(imageDict)}')
    cardsfile.write('\n'.join(cardsToWrite))
    countfile.write('\n'.join(countToWrite))
    cardsfile.close(), countfile.close()
    return imageDict, nameDict, ee # returns both dictionaries
