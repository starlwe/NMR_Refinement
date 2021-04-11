import CifCellLib as cc
import os

CifFile = "1211709.cif"
InputFile = "mglucp.txt"
OutFile = "mglucp.cif"

hInCif = open(CifFile, 'r')
hInFile = open(InputFile, 'r')
hOutCif = open(OutFile, 'w')

size = os.path.getsize(CifFile)

while True:
    hPos = hInCif.tell()
    if hPos >= size:
        break
    line = hInCif.readline()
    item = line.split()
    
    if len(item) > 0 and item[0] == "_atom_site_label":
        cc.UpdateCif(line, hInCif, hInFile, hOutCif)
    else:
        hOutCif.write(line)

hInCif.close()
hOutCif.close()
