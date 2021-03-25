# loadImages file
# This file has the function that loads all the image paths to a dictionary
#       As well as records each name in a dictionary where each key is the name all lowercase with no punctuation
#       and the value is the proper, full name
# In addition, this file has a function to remove punctuation from a string
import os

# Function to remove punctuation from names
def simplifyName(name):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    newname = ""
    for l in name:
        if l not in punctuations:
            newname += l
    newname = newname.lower()
    return newname

# Creates two dictionaries recording the path and names of all files given a directory
def loadAllImages(imageDir):
    # Initialize dicts
    imageDict = {} # cardname : path
    nameDict = {} # lowercase+nopunct cardname : proper cardname
    # Loop through subdirs in main dir
    for d in os.listdir(imageDir):
        # Loop through files in subdir
        for c in os.listdir(imageDir+"/"+d):
            propName = c[:-4] # Gets the name of the card without the extension
            imageDict[propName] = d # Corresponds card name with subdir
            lowerName = simplifyName(propName.lower()) # Gets the simplified name
            nameDict[lowerName] = propName # Corresponds simplified name with proper name
    return imageDict, nameDict # returns both dictionaries
