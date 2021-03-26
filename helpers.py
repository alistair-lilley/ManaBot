
# strips extensions
def stripExt(filename):
    split = filename.split('.')
    ext = '.'+split[-1]
    name = ' '.join(split[:-1])
    return name, ext

# Function to remove punctuation from names
def simplifyName(name):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    newname = ""
    for l in name:
        if l not in punctuations:
            newname += l
    newname = newname.lower()
    return newname