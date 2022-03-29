import pyximport
pyximport.install()
from helpers.eDist import edist
import string, os
from PIL import Image


NUMERALS = set([str(i) for i in range(0,10)]+["."])

def makeNum(numstr,idx):
    nombor = ''
    while numstr[idx] in NUMERALS:
        nombor += numstr[idx]
        idx += 1
        if idx == len(numstr):
            break
    return int(nombor), idx

def stripExt(filename):
    split = filename.split('.')
    ext = '.'+split[-1]
    name = '.'.join(split[:-1])
    return name, ext

def simplifyString(name):
    newname = ""
    for l in name:
        if l not in string.punctuation+" " or l == "_":
            newname += l
    newname = newname.lower()
    return newname

# Catches the "first difference" in strings to judge which is "higher" or "lower" based on the alphabet and word length
def firstdiff(nameL, nameR):
    maxLen = min(len(nameL),len(nameR))
    for i in range(maxLen):
        if nameL[i] < nameR[i]:
            return True
        elif nameL[i] > nameR[i]:
            return False
    if(len(nameL) < len(nameR)):
        return True
    return False

# I would have combined the two merge sort algorithms, but it ended up being WAY too slow to check datatypes on the fly

# number merge
def nmerge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [""] * (n1)
    R = [""] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] < R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def nmergeSort(arr, l, r):
    if l < r:
        m = (l + (r - 1)) // 2
        nmergeSort(arr, l, m)
        nmergeSort(arr, m + 1, r)
        nmerge(arr, l, m, r)

def nmS(arr):
    nmergeSort(arr, 0, len(arr)-1)

# string merge
def smerge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [""] * (n1)
    R = [""] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if firstdiff(L[i],R[j]):
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def smergeSort(arr, l, r):
    if l < r:
        m = (l + (r - 1)) // 2
        smergeSort(arr, l, m)
        smergeSort(arr, m + 1, r)
        smerge(arr, l, m, r)

def smS(arr):
    smergeSort(arr, 0, len(arr)-1)


def findSimilar(L, name, N=5):
    top = {}
    tops = {}
    for l in L:
        try:
            dist = edist(l, name, len(l)-1, len(name)-1, [[-1 for i in range(len(name))] for j in range(len(l))])
            tops[l] = dist
        except:
            pass
    while len(top) < N:
        maxCard = min(tops, key=tops.get)
        top[maxCard] = tops[maxCard]
        del (tops[maxCard])
    return list(sorted(top, key=top.get))

def ensureFileDir(pathDicts,key,v,currPath):
    if type(pathDicts[key][v]) == dict:
        val = list(pathDicts[key][v])[0]
    else:
        val = pathDicts[key][v]
    if '.' in val:
        val = '.'.join(val.split('.')[:-1])
    if not os.path.exists(currPath + '/' + val):
        os.mkdir(currPath + '/' + val)
    if type(pathDicts[key][v]) == dict:
        ensureFiles(pathDicts[key][v], currPath)

def ensureFileTxt(pathDicts,key,v,currPath):
    val = pathDicts[key][v]
    pathToTxt = currPath + '/' + val + '.txt'
    if not os.path.exists(pathToTxt):
        with open(pathToTxt, 'w') as f:
            f.write("Empty")

def ensureFileJpg(pathDicts,key,v,currPath):
    val = pathDicts[key][v]
    pathToJpg = currPath + "/" + val + ".jpg"
    if not os.path.exists(pathToJpg):
        img = Image.new("RGB", (361, 500))
        img.save(pathToJpg)

def ensureFileJson(pathDicts,key,v,currPath):
    val = pathDicts[key][v]
    pathToJson = currPath + "/" + val + ".json"
    if not os.path.exists(pathToJson):
        with open(pathToJson, 'w') as f:
            f.write("{}")

def ensureFileEach(pathDicts,currPath,mode,key,v):
    if mode == 'dir':
        ensureFileDir(pathDicts,key,v,currPath)
    if mode == 'txt':
        ensureFileTxt(pathDicts,key,v,currPath)
    if mode == "jpg":
        ensureFileJpg(pathDicts,key,v,currPath)
    if mode == "json":
        ensureFileJson(pathDicts,key,v,currPath)

def ensureFiles(pathDicts, prevPath=os.getcwd()):
    for key in list(pathDicts.keys()):
        mode = key.split('.')[-1]
        keyPath = '.'.join(key.split('.')[:-1])
        currPath = prevPath + '/' + keyPath
        if not os.path.exists(currPath):
            os.mkdir(currPath)
        for v in range(len(pathDicts[key])):
            ensureFileEach(pathDicts,currPath,mode,key,v)

