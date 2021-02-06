def ProcessNMROutputFile_Castep(NMRFile, NMROut):
    try:
        hFile = open(NMRFile, 'r')
    except:
        return None
    while True:
        line = hFile.readline()
        line = line.split()
        if line != [] and line[0] == "[magres_old]":
            ExtractNMRShielding(hFile, NMROut)
            return None
        elif not line:
            return None

def ExtractNMRShielding(hFile, NMROut):
    hOut = open(NMROut, 'w')
    tensors = []
    coord = []
    while True:
        line = hFile.readline()
        item = line.split()
        if len(item) > 2 and item[2] == "Eigenvalue":
            tensors.append(item[4])
        elif len(item) > 2 and item[2] == "Coordinates":
            coord.append(item[0])
            coord.append(item[1])
            coord.append(item[3])
            coord.append(item[4])
            coord.append(item[5])
        elif item != [] and item[0] == "[/magres_old]":
            while True:
                lineout = str(coord.pop(0)) + str(coord.pop(0)) + " "
                lineout = lineout + str(tensors.pop(0)) + " " + str(tensors.pop(0)) + " " + str(tensors.pop(0)) + " "
                lineout = lineout + coord.pop(0) + " " + coord.pop(0) + " " + coord.pop(0) + "\n"
                hOut.write(lineout)
                if tensors == [] or coord == []:
                    hOut.close()
                    hFile.close()
                    return None
        elif not line:
            hOut.close()
            hFile.close()
            return None

def LoadUnitCellParameters(InputFile):
    hIn = open(InputFile, 'r')
    line = hIn.readline()
    item = line.split()
    a = float(item[0])
    b = float(item[1])
    c = float(item[2])
    alpha = float(item[3])
    beta = float(item[4])
    gamma = float(item[5])
    SymOps = item[6]
    hIn.close()
    return (a,b,c,alpha,beta,gamma,SymOps)

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

def WriteCastepFiles(InputFile, i, data, OutputParams):
    OutputFileCell = InputFile + "." + str(i) + ".asy_unit_cell"
    cell = OutputParams[0]
    param = OutputParams[1]
    
    hFile = open(OutputFileCell,'w')
    line = "%BLOCK POSITIONS_ABS\n"
    hFile.write(line)
    size = len(data)
    while True:
        if size <= 0:
            break
        else:
            element = data.pop(0)
            if len(element) > 1:
                if element[1].isnumeric() == False:
                    element = element[0:2]
                else:
                    element = element[0:1]
            line = element + " " + str(data.pop(0)) + " " + str(data.pop(0)) \
                + " " + str(data.pop(0)) + "\n"
            size = size - 4
            hFile.write(line)
    line = "%ENDBLOCK POSITIONS_ABS\n\n"
    hFile.write(line)
    for lineitem in cell:
        hFile.write(lineitem)
    hFile.close()
    return None

def WriteCastepFullUnitCell(InputFile, i, data, OutputParams):
    OutputFileCell = InputFile + "." + str(i) + ".cell"
    OutputFileParam = InputFile + "." + str(i) + ".param"
    cell = OutputParams[0]
    param = OutputParams[1]
    
    hFile = open(OutputFileCell,'w')
    line = "%BLOCK POSITIONS_FRAC\n"
    hFile.write(line)
    size = len(data)
    while True:
        if size <= 0:
            break
        else:
            element = data.pop(0)
            if len(element) > 1:
                if element[1].isnumeric() == False:
                    element = element[0:2]
                else:
                    element = element[0:1]
            line = element + " " + str(data.pop(0)) + " " + str(data.pop(0)) \
                + " " + str(data.pop(0)) + "\n"
            size = size - 4
            hFile.write(line)
    line = "%ENDBLOCK POSITIONS_FRAC\n\n"
    hFile.write(line)
    for lineitem in cell:
        hFile.write(lineitem)
    hFile.close()
    
    hFile = open(OutputFileParam, 'w')
    for lineitem in param:
        hFile.write(lineitem)
    hFile.close()
    return None

def RemoveDuplicates(NMRFile):
    data = []
    try:
        hFile = open(NMRFile, 'r')
    except:
        return False
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
        data.append(item[4])
        data.append(item[5])
        data.append(item[6])
    hFile.close()
    
    udata = []
    
    while data != []:
        if udata == []:
            udata.append(data.pop(0))
            udata.append(data.pop(0))
            udata.append(data.pop(0))
            udata.append(data.pop(0))
            udata.append(data.pop(0))
            udata.append(data.pop(0))
            udata.append(data.pop(0))
        else:
            if udata[-6] == data[1] and udata[-5] == data[2] and udata[-4] == data[3]:
                data.pop(0)
                data.pop(0)
                data.pop(0)
                data.pop(0)
                data.pop(0)
                data.pop(0)
                data.pop(0)
            else:
                udata.append(data.pop(0))
                udata.append(data.pop(0))
                udata.append(data.pop(0))
                udata.append(data.pop(0))
                udata.append(data.pop(0))
                udata.append(data.pop(0))
                udata.append(data.pop(0))
    
    lineout = ""
    
    while udata != []:
        lineout = lineout + udata.pop(0) + " " + udata.pop(0) + " " + udata.pop(0) + " " + udata.pop(0) + \
        " " + udata.pop(0) + " " + udata.pop(0) + " " + udata.pop(0) + "\n"
    
    hFile  = open(NMRFile, 'w')
    hFile.write(lineout)
    hFile.close()
    return True
