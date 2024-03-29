import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

ZeroDetect = False
a2 = (5.0 + 5.0**(1/2)) / 10.0
b2 = (5.0 - 5.0**(1/2)) / 10.0
    
def DisplayPoorFits(Num, FileName, ShiftFile, TheMap):
    InputFile = FileName + '.' + str(Num) + ".nmr"
    shift_data = LoadShiftData(ShiftFile)
    shielding_data = LoadShieldingData(InputFile)
    shift = shift_data[:]
    shielding = shielding_data[:]
    R2, m, b, MaxDiff = LinearFit(shift, shielding, TheMap)
    shift = []
    shielding = []
    line = "Structure " + str(Num) + "\n"
    
    while True:
        if shift_data == [] or shielding_data == []:
            break
        elif shift_data[0] == shielding_data[0]:
            shift_data.pop(0)
            shielding_data.pop(0)
            
            XX = float(shift_data.pop(0))
            YY = float(shift_data.pop(0))
            ZZ = float(shift_data.pop(0))
            xx = float(shielding_data.pop(0))
            yy = float(shielding_data.pop(0))
            zz = float(shielding_data.pop(0))

            if(xx > zz):
                xx, zz = zz, xx
            if(XX < ZZ):
                XX, ZZ = ZZ, XX
                
            ixx = a2*xx + b2*yy
            iyy = a2*yy + b2*zz
            izz = a2*zz + b2*xx
            
            iXX = a2*XX + b2*YY
            iYY = a2*YY + b2*ZZ
            iZZ = a2*ZZ + b2*XX            
        
            shift.append(iXX)
            shift.append(iYY)
            shift.append(iZZ)
            shielding.append(ixx)
            shielding.append(iyy)
            shielding.append(izz)
        else:
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
        
        #if i % 3 == 0:
        #    diff = FindMinDiff(shielding[i], shielding[i+2], y)
        #elif i % 3 == 1:
        #    diff = float(shielding[i]) - y
        #elif i % 3 == 2:
        #    diff = FindMinDiff(shielding[i-2], shielding[i], y)
        #df2 = diff**2
        #Sum = Sum + df2
        #Num_Items = i
        #if i % 3 == 0:
        #    ANum = ANum + 1
        #line = line + "Atom " + str(ANum) + " difference^2: " + str(df2) + "\n"
        
    hFile = open("DiffFile.txt", 'a')
    line = line + "\nR^2: " + str(R2) + "\n"
    line = line + "Eqn: y = " + str(m) + "x + " + str(b) + "\n"

    RMS = CalculateRMSError(shift, shielding, TheMap, Num)
    line = line + "RMS Error: " + str(RMS) + " ppm\n\n"
    hFile.write(line)
    hFile.close()
    return None

def FindMinDiff(s1, s2, y):
    shielding1 = float(s1)
    shielding2 = float(s2)
    diff1 = s1 - y
    diff2 = s2 - y
    if diff1**2 > diff2**2:
        return diff2
    else:
        return diff1

def FindBestFit(NMRFileBase, NMRExpFile, NumOfPoints, TheMap, Debug = False, RMSD = False):
    shift_data = LoadShiftData(NMRExpFile)
    BestFit = []
    MinDiff = 1000000
    
    global ZeroDetect
    MinRMS = 1000000
    
    for i in range(NumOfPoints):
        NMRFile = NMRFileBase + "." + str(i) + ".nmr"
        shielding_data = LoadShieldingData(NMRFile)
        shift_copy = shift_data[:]
        shielding_copy = shielding_data[:]
        if shielding_data == []:
            R2 = 0.0
            ZeroDetect = True
            #continue
        else:
            R2, m, b, MaxDiff = LinearFit(shift_copy, shielding_copy, TheMap)
        if Debug == True:
            print(str(i) + " " + str(R2))
        if RMSD == False:
            if MaxDiff < MinDiff:
                MinDiff = MaxDiff
                if BestFit == []:
                    BestFit.append(i)
                    BestFit.append(R2)
                    BestFit.append(m)
                    BestFit.append(b)
                else:
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.append(i)
                    BestFit.append(R2)
                    BestFit.append(m)
                    BestFit.append(b)
        elif RMSD == True and shielding_data != []:
            shift_copy = shift_data[:]
            shielding_copy = shielding_data[:]
            shift_copy, shielding_copy = _ProcessData(shift_copy, shielding_copy, TheMap)
            RMS = CalculateRMSError(shift_copy, shielding_copy, TheMap)
            
            if MinRMS > RMS:
                MinRMS = RMS
                if BestFit == []:
                    BestFit.append(i)
                    BestFit.append(MinRMS)
                    BestFit.append(m)
                    BestFit.append(b)
                else:
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.append(i)
                    BestFit.append(MinRMS)
                    BestFit.append(m)
                    BestFit.append(b)
                    
    PlotBestFit(BestFit[0], NMRFileBase, NMRExpFile, TheMap)
    return BestFit[0], BestFit[1]
                        
def LoadShiftData(InputFile):
    hFile = open(InputFile, "r")
    Shift_data = []
    
    while True:
        line = hFile.readline()
        item = line.split()
        if not line:
            hFile.close()
            return Shift_data
        elif len(item) > 1:
            Shift_data.append(item[0])
            xx = float(item[1])
            yy = float(item[2])
            zz = float(item[3])
            Shift_data.append(xx)
            Shift_data.append(yy)
            Shift_data.append(zz)

def LoadShiftDataA(InputFile):
    hFile = open(InputFile, "r")
    Shift_data = []
    
    while True:
        line = hFile.readline()
        item = line.split()
        if not line:
            hFile.close()
            return Shift_data
        elif len(item) > 1:
            xx = float(item[0])
            yy = float(item[1])
            zz = float(item[2])
            Shift_data.append(xx)
            Shift_data.append(yy)
            Shift_data.append(zz)
            
def LoadShieldingData(InputFile):
    try:
        hFile = open(InputFile, 'r')
    except:
        return []
    shielding_data = []
    while True:
        line = hFile.readline()
        item = line.split()
        if not line:
            hFile.close()
            return shielding_data
        elif len(item) > 1:
            shielding_data.append(item[0])
            xx = float(item[1])
            yy = float(item[2])
            zz = float(item[3])
            shielding_data.append(xx)
            shielding_data.append(yy)
            shielding_data.append(zz)

def LinearFit(shift_data, shielding_data, TheMap):    
    shift = []
    shielding = []

    while True:
        if shift_data == [] or shielding_data == []:
            break
        elif shift_data[0] == shielding_data[0]:
            shift_data.pop(0)
            shielding_data.pop(0)
            XX = shift_data.pop(0)
            YY = shift_data.pop(0)
            ZZ = shift_data.pop(0)
            xx = shielding_data.pop(0)
            yy = shielding_data.pop(0)
            zz = shielding_data.pop(0)

            cXX = (float(xx) - TheMap[1]) / TheMap[0]
            
            XX, ZZ = FindMatch(XX, ZZ, cXX)
            
            # Convert to Icosahedral
            ixx = a2*xx + b2*yy
            iyy = a2*yy + b2*zz
            izz = a2*zz + b2*xx
            
            iXX = a2*XX + b2*YY
            iYY = a2*YY + b2*ZZ
            iZZ = a2*ZZ + b2*XX
            
            shielding.append(ixx)
            shielding.append(iyy)
            shielding.append(izz)
            shift.append(iXX)
            shift.append(iYY)
            shift.append(iZZ)

        else:
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
    x = np.array(shift, dtype = np.float64)
    y = np.array(shielding, dtype = np.float64)
    m, b, r, p, stderr = stats.linregress(x,y)
    MaxDiff = FindMaxDiff(m, b, shift, shielding)
    r2 = r**2
    return r2, m, b, MaxDiff

def FindMaxDiff(m, b, shift, shielding):
    MaxDiff = 0
    
    x=3.14
    y = m*x + b
    m = -1.0
    b = y - (m*x)
    
    for i in range(0,len(shift),3):
        XX = float(shift[i])
        YY = float(shift[i+1])
        ZZ = float(shift[i+2])
        xx = float(shielding[i])
        yy = float(shielding[i+1])
        zz = float(shielding[i+2])
        
        cXX = (xx - b) / m
        cYY = (yy - b) / m
        cZZ = (zz - b) / m
        
        cXX, cZZ = FindMatch(cXX,cZZ,XX)
        
        _errx = (XX - cXX)**2
        _erry = (YY - cYY)**2
        _errz = (ZZ - cZZ)**2
        
        if _errx > MaxDiff:
            MaxDiff = _errx
        if _erry > MaxDiff:
            MaxDiff = _erry
        if _errz > MaxDiff:
            MaxDiff = _errz
    
    return MaxDiff
        

def _ProcessData(shift_data, shielding_data, TheMap):
    shift = []
    shielding = []
    i = 0
    
    while True:
        if shift_data == [] or shielding_data == []:
            break
        elif shift_data[0] == shielding_data[0]:
            shift_data.pop(0)
            shielding_data.pop(0)
            shift.append(shift_data.pop(0))
            shift.append(shift_data.pop(0))
            shift.append(shift_data.pop(0))
            xx = shielding_data.pop(0)
            yy = shielding_data.pop(0)
            zz = shielding_data.pop(0)
            y = TheMap[0] * float(shift[i]) + TheMap[1]
            xx, zz = FindMatch(xx, zz, y)
            shielding.append(xx)
            shielding.append(yy)
            shielding.append(zz)
            i = i + 3
        else:
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
            
    return shift, shielding

def FindMatch(xx, zz, y):
    xx = float(xx)
    zz = float(zz)
    d1 = xx - y
    d2 = zz - y
    if d1**2 > d2**2:
        return zz, xx
    else:
        return xx, zz
    
def CalcRMSDPair(xx, yy, zz, sxx, syy, szz, TheMap):
    xx = float(xx)
    yy = float(yy)
    zz = float(zz)
    sxx = float(sxx)
    syy = float(syy)
    szz = float(szz)
    XX = xx * TheMap[0] + TheMap[1]
    YY = yy * TheMap[0] + TheMap[1]
    ZZ = zz * TheMap[0] + TheMap[1]
    
    sxx, szz = FindMatch(sxx,szz,XX)
    
    _err1 = 3*((XX-sxx)**2) + 3*((YY-syy)**2) + 3*((ZZ-szz)**2)
    _err2 = 2*(XX-sxx)*(YY-syy) + 2*(XX-sxx)*(ZZ-szz) + 2*(YY-syy)*(ZZ-szz)
    _err3 = _err1 + _err2
    _err4 = (1/15) * _err3
    d = _err4**(1/2)
    return d

def CalculateRMSError(shift_o, shielding_o, TheMap, Num):
    debug = False
    sum = 0
    Num_Items = 0
    shift = shift_o[:]
    shielding = shielding_o[:]
    
    while shift != [] or shielding != []:
        XX = float(shift.pop(0))
        YY = float(shift.pop(0))
        ZZ = float(shift.pop(0))
        xx = float(shielding.pop(0))
        yy = float(shielding.pop(0))
        zz = float(shielding.pop(0))
        if debug:
            print("Shift XX = ", XX)
            print("Shielding xx = ", xx)
            print("Shift ZZ = ", ZZ)
            print("Shielding zz = ", zz)
            
        
        cXX = (float(xx) - TheMap[1]) / TheMap[0]
        cYY = (float(yy) - TheMap[1]) / TheMap[0]
        cZZ = (float(zz) - TheMap[1]) / TheMap[0]

        if debug:
            print("Calc Shift cxx = ", cXX)
            print("Calc Shift czz = ", cZZ)
        
        cXX, cZZ = FindMatch(cXX,cZZ,XX)

        if debug:
            print("After match")
            print("Calc Shift cxx = ", cXX)
            print("Calc Shift czz = ", cZZ)
            
        _errx = (XX - cXX)**2
        _erry = (YY - cYY)**2
        _errz = (ZZ - cZZ)**2
        _sum = _errx + _erry + _errz

        if debug:
            print("Error in x = ", _errx)
            print("Sum of three = ", _sum)
        
        sum = sum + _sum
        Num_Items = Num_Items + 3
    
    _rms = sum / Num_Items
    RMS = _rms**(1/2)
    #print("debug: num_items = " + str(Num_Items))
    #print("debug: sum = " + str(sum))
    #print("debug: rms^2 = " + str(_rms))
    #print("debug: rms = " + str(RMS))
         
    return RMS

def PlotBestFit(i, NMRFileBase, NMRExpFile, TheMap):
    NMRFile = NMRFileBase + "." + str(i) + ".nmr"
    shift_data = LoadShiftData(NMRExpFile)
    shielding_data = LoadShieldingData(NMRFile)
    shift = []
    shielding = []
    #i = 0
    while True:
        if shift_data == [] or shielding_data == []:
            break
        elif shift_data[0] == shielding_data[0]:
            shift_data.pop(0)
            shielding_data.pop(0)
            
            XX = shift_data.pop(0)
            YY = shift_data.pop(0)
            ZZ = shift_data.pop(0)
            xx = shielding_data.pop(0)
            yy = shielding_data.pop(0)
            zz = shielding_data.pop(0)

            cXX = (float(xx) - TheMap[1]) / TheMap[0]
            
            XX, ZZ = FindMatch(XX, ZZ, cXX)
            
            # Convert to Icosahedral
            ixx = a2*xx + b2*yy
            iyy = a2*yy + b2*zz
            izz = a2*zz + b2*xx
            
            iXX = a2*XX + b2*YY
            iYY = a2*YY + b2*ZZ
            iZZ = a2*ZZ + b2*XX
            
            shielding.append(ixx)
            shielding.append(iyy)
            shielding.append(izz)
            shift.append(iXX)
            shift.append(iYY)
            shift.append(iZZ)
            
            #shift.append(shift_data.pop(0))
            #shift.append(shift_data.pop(0))
            #shift.append(shift_data.pop(0))
            #xx = shielding_data.pop(0)
            #yy = shielding_data.pop(0)
            #zz = shielding_data.pop(0)
            #y = TheMap[0] * float(shift[i]) + TheMap[1]
            #xx, zz = FindMatch(xx, zz, y)
            #shielding.append(xx)
            #shielding.append(yy)
            #shielding.append(zz)
            #i = i + 3
        else:
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
            
    x = np.array(shift, dtype = np.float64)
    y = np.array(shielding, dtype = np.float64)
    m, b, r, p, stderr = stats.linregress(x,y)
    print("Equation: y = " + str(m) + "x + " + str(b))
    print("R^2 = " + str(r**2))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y,'o')
    ax.set_xlabel("Experimental Shift")
    ax.set_ylabel("Theoretical Shielding")
    ax.plot(x, m*x + b)
    ax.text(0.2, 0.1, 'R^2 = %0.8f' % r**2, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    plt.show()
    global ZeroDetect
    if ZeroDetect:
        print("Some magres file(s) are empty!")

def AssignShifts(shift_data, shielding_data, TheMap):
    shiftlist = []
    error_matrix = []
    i = 0
    j = 0
    size1 = int(len(shift_data) / 3)
    size2 = int(len(shielding_data) / 4)
    
    for a in range(size1):
        for b in range(size2):
            xx = shift_data[i]
            yy = shift_data[i+1]
            zz = shift_data[i+2]
            sxx = shielding_data[j+1]
            syy = shielding_data[j+2]
            szz = shielding_data[j+3]
            _error = CalcRMSDPair(xx,yy,zz,sxx,syy,szz,TheMap)
            error_matrix.append(_error)
            j = j + 4
        i = i + 3
        j = 0
    
    hFile = open("errormatrix.txt", 'w')
    lineout = ""
    
    for k in range(len(error_matrix)):
        if k % size2 == 0 and k != 0:
            lineout = lineout + "\n"
        lineout = lineout + str(error_matrix[k]) + " "
            
    hFile.write(lineout)
    hFile.close()
    
    left = size1
    
    while left > 0:
        _err = 1000000
        inx = 0
        
        for c in range(len(error_matrix)):
            if error_matrix[c] < _err:
                _err = error_matrix[c]
                inx = c
                
        shf = inx // size2
        shd = inx % size2
        shiftlist.append(shf)
        shiftlist.append(shd)
        left = left - 1
        error_matrix[inx] = 1000000
        
    return shiftlist
