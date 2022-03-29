import cython

def edist(sone, stwo, i, j, table):
    if table[i][j] >= 0:
        return table[i][j]
    comp = (1,0)[sone[i] == stwo[j]]
    if i == 0 and j == 0:
        table[0][0] = comp
        return table[0][0]
    elif i == 0:
        table[i][j] = comp + edist(sone, stwo, i, j-1, table)
        return table[i][j]
    elif j == 0:
        table[i][j] = comp + edist(sone, stwo, i-1, j, table)
        return table[i][j]
    else:
        table[i][j] = comp + \
                      min(edist(sone, stwo, i, j-1, table),
                            edist(sone, stwo, i-1, j, table),
                            edist(sone, stwo, i-1, j-1, table))
        return table[i][j]