import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

ZeroDetect = False

def DisplayPoorFits(Num, FileName, ShiftFile, TheMap):
    InputFile = FileName + '.' + str(Num) + ".nmr"
    shift_data = LoadShiftData(ShiftFile)
    shielding_data = LoadShieldingData(InputFile)
    shift = shift_data[:]
    shielding = shielding_data[:]
    R2, m, b = LinearFit(shift, shielding, TheMap)
    shift = []
    shielding = []
    line = "Structure " + str(Num) + "\n\n"
    ANum = 0
    Sum = 0
    Num_Items = 0
    while True:
        if shift_data == [] or shielding_data == []:
            break
        elif shift_data[0] == shielding_data[0]:
            shift_data.pop(0)
            shielding_data.pop(0)
            shift.append(shift_data.pop(0))
            shift.append(shift_data.pop(0))
            shift.append(shift_data.pop(0))
            shielding.append(shielding_data.pop(0))
            shielding.append(shielding_data.pop(0))
            shielding.append(shielding_data.pop(0))
        else:
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
            shielding_data.pop(0)
    for i in range(len(shift)):
        y = m * float(shift[i]) + b
        if i % 3 == 0:
            diff = FindMinDiff(shielding[i], shielding[i+2], y)
        elif i % 3 == 1:
            diff = float(shielding[i]) - y
        elif i % 3 == 2:
            diff = FindMinDiff(shielding[i-2], shielding[i], y)
        df2 = diff**2
        Sum = Sum + df2
        Num_Items = i
        if i % 3 == 0:
            ANum = ANum + 1
        line = line + "Atom " + str(ANum) + " difference^2: " + str(df2) + "\n"
    hFile = open("DiffFile.txt", 'w')
    line = line + "\nR^2: " + str(R2) + "\n"
    line = line + "Eqn: y = " + str(m) + "x + " + str(b) + "\n"
    Num_Items = Num_Items + 1
    RMS = CalculateRMSError(shift, shielding, TheMap)
    line = line + "RMS Error: " + str(RMS) + "\n"
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
    MaxR2 = 0.0
    Num_Items = 0
    Sum = 0
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
        else:
            R2, m, b = LinearFit(shift_copy, shielding_copy, TheMap)
        if Debug == True:
            print(str(i) + " " + str(R2))
        if RMSD == False:
            if R2 > MaxR2:
                MaxR2 = R2
                if BestFit == []:
                    BestFit.append(i)
                    BestFit.append(MaxR2)
                    BestFit.append(m)
                    BestFit.append(b)
                else:
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.pop(0)
                    BestFit.append(i)
                    BestFit.append(MaxR2)
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
    x = np.array(shift, dtype = np.float64)
    y = np.array(shielding, dtype = np.float64)
    m, b, r, p, stderr = stats.linregress(x,y)
    r2 = r**2
    return r2, m, b

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

def CalculateRMSError(shift_o, shielding_o, TheMap):
    sum = 0
    Num_Items = 0
    shift = shift_o[:]
    shielding = shielding_o[:]
    
    while shift != [] or shielding != []:
        xx = float(shift.pop(0))
        yy = float(shift.pop(0))
        zz = float(shift.pop(0))
        sxx = float(shielding.pop(0))
        syy = float(shielding.pop(0))
        szz = float(shielding.pop(0))
        
        XX = xx * TheMap[0] + TheMap[1]
        YY = yy * TheMap[0] + TheMap[1]
        ZZ = zz * TheMap[0] + TheMap[1]
        
        sxx, szz = FindMatch(sxx,szz,XX)
        
        _err1 = 3*((XX-sxx)**2) + 3*((YY-syy)**2) + 3*((ZZ-szz)**2)
        _err2 = 2*(XX-sxx)*(YY-syy) + 2*(XX-sxx)*(ZZ-szz) + 2*(YY-syy)*(ZZ-szz)
        _err3 = _err1 + _err2
        d2 = (1/15) * _err3
        
        sum = sum + d2
        Num_Items = Num_Items + 1
    
    _rms = sum / Num_Items
    RMS = _rms**(1/2)
         
    return RMS

def PlotBestFit(i, NMRFileBase, NMRExpFile, TheMap):
    NMRFile = NMRFileBase + "." + str(i) + ".nmr"
    shift_data = LoadShiftData(NMRExpFile)
    shielding_data = LoadShieldingData(NMRFile)
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