def ExtractCoord(hFile, OutFile):
    PosList = []
    IsPos = True
    
    while True:
        line = hFile.readline()
        line = line.split()
        if len(line) > 0:
            if line[0] != "_atom_site_label" and line[0] != "_atom_site_type_symbol" and IsPos:
                return True
            elif line[0] == "_atom_site_fract_z":
                PosList.append(line[0])
                break
            else:
                IsPos = False
                PosList.append(line[0])
    
    CoordList = []
    NumCol = len(PosList)
    hOut = open(OutFile, 'w')
    done = True
    
    while done:
        try:
            line = hFile.readline()
        except:
            break
        item = line.split()
        if len(item) >= NumCol:
            posidx = PosList.index('_atom_site_type_symbol')
            CoordList.append(item[posidx])
            posidx = PosList.index('_atom_site_fract_x')
            CoordList.append(item[posidx])
            posidx = PosList.index('_atom_site_fract_y')
            CoordList.append(item[posidx])
            posidx = PosList.index('_atom_site_fract_z')
            CoordList.append(item[posidx])
        elif len(item) == 0:
            done = False
    
    line = ""
    
    while len(CoordList) > 3:
        line = line + CoordList.pop(0) + " " + str(CoordList.pop(0)) + \
        " " + str(CoordList.pop(0)) + " " + str(CoordList.pop(0)) + "\n"
    
    hOut.write(line)
    hOut.close()
    
    return False

def LoadCellData(hFile):
    Data = []
    i = 1
    PS = ''
    
    while True:
        line = hFile.readline()
        item = line.split()
        
        if len(item) > 0:
            if item[0] != PS:
                i = 1
                PS = item[0]
            Data.append(item[0] + str(i))
            Data.append(item[0])
            Data.append(item[1])
            Data.append(item[2])
            Data.append(item[3])
            i = i + 1
        else:
            return Data

def GetAtomSiteFractX(row, Data):
    pos = row * 5 + 2
    return Data[pos]

def GetAtomSiteFractY(row, Data):
    pos = row * 5 + 3
    return Data[pos]

def GetAtomSiteFractZ(row, Data):
    pos = row * 5 + 4
    return Data[pos]

def GetAtomSiteLabel(row, Data):
    pos = row * 5
    return Data[pos]

def GetAtomSiteType(row, Data):
    pos = row * 5 + 1
    return Data[pos]
    
def UpdateCif(line, hInCif, hInFile, hOutCif):
    item = line.split()
    row = 0
    
    while True:
        if len(item) < 2:
            if item[0] == '_atom_site_label' or item[0] == '_atom_site_type_symbol' \
          or item[0] == '_atom_site_fract_x' or item[0] == '_atom_site_fract_y' or item[0] == '_atom_site_fract_z':
                hOutCif.write(line)
        else:
            break
        line = hInCif.readline()
        item = line.split()
    
    CellData = LoadCellData(hInFile)
    hInFile.close()
    
    while True:
        if len(item) < 3:
            row = int(len(CellData) / 5)
            for i in range(row):
                atomlabel = GetAtomSiteLabel(i, CellData)
                atomtype = GetAtomSiteType(i, CellData)
                atomx = GetAtomSiteFractX(i, CellData)
                atomy = GetAtomSiteFractY(i, CellData)
                atomz = GetAtomSiteFractZ(i, CellData)
                line = atomlabel + " " + atomtype + " " + str(atomx) + " " + str(atomy) + " " + str(atomz) + "\n"
                hOutCif.write(line)
            return
        else:
            line = hInCif.readline()
            item = line.split()