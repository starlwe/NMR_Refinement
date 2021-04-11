import CifCellLib as cc

CifFile = "1211709.cif"
OutFile = "mglucp.txt"

hFile = open(CifFile, 'r')
PosExt = True

while PosExt:
    line = hFile.readline()
    item = line.split()
    if len(item) > 0 and item[0] == "loop_":
        PosExt = cc.ExtractCoord(hFile, OutFile)

hFile.close()
