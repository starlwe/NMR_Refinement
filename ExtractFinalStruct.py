InputFileName = "naphta06_geo.castep"
OutputFile = "naphta06_geo.txt"

def LoadInputFileContents(InputFile):
    data = []
    hFile = open(InputFile, 'r')

    while True:
        line = hFile.readline()
        item = line.split()

        if len(item) > 2 and item[0] == "BFGS:":
            if item[1] == "Final" and item[2] == "Configuration:":
                break

    for i in range(10):
        line = hFile.readline()
        
    line="not empty"
    while True:
        line = hFile.readline()
        if not line:
            break;
        item = line.split()
        if len(item) < 5:
            break
        data.append(item[1])
        data.append(item[3])
        data.append(item[4])
        data.append(item[5])
    hFile.close()
    return data

def WriteCell(data):    
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
    line = "\n"
    hFile.write(line)
    hFile.close()
    return None

data = LoadInputFileContents(InputFileName)
WriteCell(data)
