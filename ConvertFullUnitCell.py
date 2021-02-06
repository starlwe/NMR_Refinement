from SymmetryTable import *

def ConvertToFullUnitCell(OutputContent, SymTable, SymOps):
    out_data = []
    _symops = SymTable[SymOps]
    _numops = _symops[0]
    
    while OutputContent != []:
        element = OutputContent.pop(0)
        x = float(OutputContent.pop(0))
        y = float(OutputContent.pop(0))
        z = float(OutputContent.pop(0))
        
        for i in range(_numops):
            fx = _symops[3*i+1]
            fy = _symops[3*i+2]
            fz = _symops[3*i+3]
            nx = fx(x,y,z)
            ny = fy(x,y,z)
            nz = fz(x,y,z)
            out_data.append(element)
            out_data.append(nx)
            out_data.append(ny)
            out_data.append(nz)
            
    return out_data

def LoadInputFileContents(InputFile):
    data = []
    hFile = open(InputFile, 'r')
    line="not empty"
    while True:
        line = hFile.readline()
        if not line:
            break;
        item = line.split()
        data.append(item[0])
        data.append(item[1])
        data.append(item[2])
        data.append(item[3])
    hFile.close()
    return data

def WriteFullUnitCell(InputFileName, data):
    OutputFile = InputFileName + ".cell"
    
    hFile = open(OutputFile,'w')
    line = "%BLOCK POSITIONS_FRAC\n"
    hFile.write(line)
    size = len(data)
    while True:
        if size <= 0:
            break
        else:
            line = data.pop(0) + " " + str(data.pop(0)) + " " + str(data.pop(0)) \
                + " " + str(data.pop(0)) + "\n"
            size = size - 4
            hFile.write(line)
    line = "%ENDBLOCK POSITIONS_FRAC"
    hFile.write(line)
    hFile.close()
    return None
