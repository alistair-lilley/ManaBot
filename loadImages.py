# loadImages file
# This file has the function that loads all the image paths to a dictionary
#       As well as records each name in a dictionary where each key is the name all lowercase with no punctuation
#       and the value is the proper, full name
# In addition, this file has a function to remove punctuation from a string
import os
from helpers import stripExt, simplifyString



# Get a dictionary of name:path and a dictionary of simplename:propername by looping through the entire image
# directory and subdirectories
def loadAllImages(imageDir):
    paths, names = {}, {}
    for d in os.listdir(imageDir):
        for c in os.listdir(imageDir+'/'+d):
            propName, ext = stripExt(c)
            paths[propName] = d+'/'+c
            simpleName = simplifyString(propName)
            names[simpleName] = propName
    return paths, names


