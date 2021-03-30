import eDistC

# strips extensions
def stripExt(filename):
    split = filename.split('.')
    ext = '.'+split[-1]
    name = ' '.join(split[:-1])
    return name, ext

# Function to remove punctuation from names
def simplifyName(name):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*~ '''
    newname = ""
    for l in name:
        if l not in punctuations:
            newname += l
    newname = newname.lower()
    return newname

# Finds which one is considered "leser":
# If the first letter that's different is...
#    lesser on the left, return True
#    lesser on the right, return False
# if all the letters are the same to maxLen...
#    if the left name is shorter, return True
#    if the right name is shorter (aka else), return False
def firstdiff(cardL, cardR):
    nameL = simplifyName(cardL)
    nameR = simplifyName(cardR)
    maxLen = min(len(nameL),len(nameR))
    for i in range(maxLen):
        if nameL[i] < nameR[i]:
            return True
        elif nameL[i] > nameR[i]:
            return False
    if(len(nameL) < len(nameR)):
        return True
    return False



def binarySearch(cardlist, name):
    if len(cardlist) == 1:
        if simplifyName(cardlist[0].name) == simplifyName(name):
            return cardlist[0]
        return None
    m = len(cardlist) // 2
    if simplifyName(cardlist[m].name) == simplifyName(name):
        return cardlist[m]
    elif firstdiff(name, cardlist[m].name):
        return binarySearch(cardlist[:m], name)
    return binarySearch(cardlist[m+1:], name)




def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray

    while i < n1 and j < n2:
        if firstdiff(L[i].name,R[j].name):
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


# l is for left index and r is right index of the
# sub-array of arr to be sorted
def mergeSort(arr, l, r):
    if l < r:
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = (l + (r - 1)) // 2

        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)


def mS(arr):
    mergeSort(arr, 0, len(arr)-1)


def findSimilar(cards, name, N=7):
    top = {}
    for card in cards:
        try:
            # get the two names to lowercase no punctuation
            c = simplifyName(card.name)
            n = simplifyName(name)
            # Gets edit distance
            dist = eDistC.edist(c, n, len(c), len(n))
            # Adds edit distance to top
            top[card.name] = dist
            # If there are more than N names in top, remove the one with the highest edit distance
            if len(top) > N:
                maxCard = max(top, key=top.get)
                del (top[maxCard])
        except:
            print(f"Uh-oh! {card.name} had an error")
    toplist = list(sorted(top,key=top.get))
    return toplist

def findMostSimilar(cards, name):
    similars = findSimilar(cards, name)
    return similars[0]

