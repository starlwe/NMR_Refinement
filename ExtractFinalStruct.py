InputFileName = "test.txt"

def LoadInputFileContents(InputFile):
    data = []
    hFile = open(InputFile, 'r')
    line="not empty"
    while True:
        line = hFile.readline()
        if not line:
            break;
        item = line.split()
        data.append(item[1])
        data.append(item[3])
        data.append(item[4])
        data.append(item[5])
    hFile.close()
    return data

def WriteCell(data):
    OutputFile = InputFileName
    
    hFile = open(OutputFile,'w')
    line = ""
    size = len(data)
    while True:
        if size <= 0:
            break
        else:
            line = data.pop(0) + " " + str(data.pop(0)) + " " + str(data.pop(0)) \
                + " " + str(data.pop(0)) + "\n"
            size = size - 4
            hFile.write(line)
    hFile.close()
    return None

data = LoadInputFileContents(InputFileName)
WriteCell(data)
