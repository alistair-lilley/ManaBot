from ctypes import *
pT = CDLL('./prefTree.so')

def wrap_function(lib, funcname, restype, argtypes):
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


class node(Structure):
    pass

node._fields_ = [("name",c_wchar_p), ("LChild", POINTER(node)), ("RChild",POINTER(node))]


newNode = wrap_function(pT,"newNode",node,[c_wchar_p])
readInFile = wrap_function(pT,"readInNodes",None,[c_wchar_p,node])


initnode = c_wchar_p("asdf")
print(initnode.value)
fpath = c_wchar_p("/home/akiahala/.local/share/Cockatrice/Cockatrice/.bot/allCards.txt")
root = pT.newNode(initnode)
#pT.readInNodes(fpath,root)
print("All cards read!")
#pT.findAndPrint(root,"Phyrexian Tower")
#a = pT.printAllChildren(root)
#type(a)
#print(type(a))