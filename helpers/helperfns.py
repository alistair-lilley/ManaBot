import string
from helpers import eDistC

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


def findSimilar(L, name, N=7):
    top = {}
    tops = {}
    for l in L:
        try:
            dist = eDistC.edist(l, name, len(l), len(name))
            tops[l] = dist
        except:
            print(f"Uh-oh! {l} had an error")
    while len(top) < N:
        maxCard = min(tops, key=tops.get)
        top[maxCard] = tops[maxCard]
        del (tops[maxCard])
    return list(sorted(top, key=top.get))
