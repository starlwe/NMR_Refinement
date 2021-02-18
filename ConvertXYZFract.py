InputFileName = "arginine2.txt"
UnitCellParam = "arginine.unitcell"
# 2: xyz to Fractional
# 1: Fractional to XYZ

ops = 1

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

def LoadUnitCellParameters(UnitCellParam):
    hIn = open(UnitCellParam, 'r')
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

def _FractalToXYZ(a,b,c,alpha,beta,gamma,x,y,z):
    import math
    alpha = alpha * (math.pi/180)
    beta = beta * (math.pi/180)
    gamma = gamma * (math.pi/180)
    X = x*a + y*b*math.cos(gamma) + z*c*math.cos(beta)
    Y = y*b*math.sin(gamma) + z*(c*(math.cos(alpha) \
        - math.cos(beta)*math.cos(gamma)) / math.sin(gamma))
    W = math.sqrt(1-(math.cos(alpha))**2-(math.cos(beta))**2 \
        -(math.cos(gamma))**2 + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
    Z = z*c*W/math.sin(gamma)
    return X,Y,Z

def ConvertFractToXYZ(input_data,a,b,c,alpha,beta,gamma):
    out_data = []
    
    while input_data != []:
        out_data.append(input_data.pop(0))
        x,y,z = _FractalToXYZ(a,b,c,alpha,beta,gamma,float(input_data.pop(0)),float(input_data.pop(0)),float(input_data.pop(0)))
        out_data.append(x)
        out_data.append(y)
        out_data.append(z)
    return out_data

def ConvertXYZToFrac(input_data, a, b, c, alpha, beta, gamma):
    out_data = []
    
    while input_data != []:
        out_data.append(input_data.pop(0))
        x,y,z = _XYZToFrac(a,b,c,alpha,beta,gamma,float(input_data.pop(0)),float(input_data.pop(0)),float(input_data.pop(0)))
        out_data.append(x)
        out_data.append(y)
        out_data.append(z)
    return out_data

def _XYZToFrac(a,b,c,alpha,beta,gamma,X,Y,Z):
    import math
    alpha = alpha * (math.pi/180)
    beta = beta * (math.pi/180)
    gamma = gamma * (math.pi/180)
    W = math.sqrt(1-(math.cos(alpha))**2-(math.cos(beta))**2 \
        -(math.cos(gamma))**2 + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
    x = X/a - (Y*math.cos(gamma))/(a*math.sin(gamma)) - (Z*(math.cos(beta)*math.cos(gamma)**2 + \
        math.cos(beta)*math.sin(gamma)**2 - math.cos(alpha)*math.cos(gamma)))/(W*a*math.sin(gamma))
    y = Y/(b*math.sin(gamma)) - (Z*(math.cos(alpha) - math.cos(beta)*math.cos(gamma)))/(W*b*math.sin(gamma))
    z = (Z*math.sin(gamma))/(W*c)
    return x,y,z

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
    line = "\n"
    hFile.write(line)
    hFile.close()
    return None

unitcell_param = LoadUnitCellParameters(UnitCellParam)
a = unitcell_param[0]
b = unitcell_param[1]
c = unitcell_param[2]
alpha = unitcell_param[3]
beta = unitcell_param[4]
gamma = unitcell_param[5]
SymOps = unitcell_param[6]
data = LoadInputFileContents(InputFileName)

if ops == 1:
    out_data = ConvertFractToXYZ(data, a, b, c, alpha, beta, gamma)
    WriteCell(out_data)
elif ops == 2:
    out_data = ConvertXYZToFrac(data, a, b, c, alpha, beta, gamma)
    WriteCell(out_data)
