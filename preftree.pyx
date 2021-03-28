'''                         Prefix tree                         '''
'''
    this file contains the class for the prefix tree
    Overview: Each node is a card object that contains the following attributes:
        - Name
        - text
        - colors
        - color ID
        - mana cost
        - type
        - power/toughness
        - related cards
    as well as two meta attributes:
        - children
        - level (of tree)
    The class has 6 methods:
        - printData - Prints the attribute data of a single node (minus level and children attributes)
        - searchChildren - recursively searches through children to find a card
        - addChild - recursively searches for a place to add a new node; throws error if it exists
        - findAndPrint - recursively searches for a card and prints its data
        - findAllSim - initiates a search for lowest edit distance cards
        - findSimilar - recursively looks through nodes and records which card names have the lowest edit dist
'''


cdef class PrefNode:
    def __init__(self, featDict):
        cdef