import Analysis as A

def ProcessData(shift_tmp, shielding_tmp, TheMap):
    shift = []
    shielding = []
    i = 0
    while True:
        if shift_tmp == [] or shielding_tmp == []:
            break
        elif shift_tmp[0] == shielding_tmp[0]:
            shift_tmp.pop(0)
            shielding_tmp.pop(0)
            shift.append(shift_tmp.pop(0))
            shift.append(shift_tmp.pop(0))
            shift.append(shift_tmp.pop(0))
            xx = shielding_tmp.pop(0)
            yy = shielding_tmp.pop(0)
            zz = shielding_tmp.pop(0)
            y = TheMap[0] * float(shift[i]) + TheMap[1]
            xx, zz = A.FindMatch(xx, zz, y)
            shielding.append(xx)
            shielding.append(yy)
            shielding.append(zz)
            i = i + 3
        else:
            shielding_tmp.pop(0)
            shielding_tmp.pop(0)
            shielding_tmp.pop(0)
            shielding_tmp.pop(0)
    return shift, shielding

def CalculateMSD(shift, shielding, Map):
    a2 = (5.0 + 5**(1/2)) / 10
    b2 = (5.0 - 5**(1/2)) / 10
    
    i = 0
    
    while i < len(shift):
        xx = a2*float(shift[i]) + b2*float(shift[i+1])
        yy = a2*float(shift[i+1]) + b2*float(shift[i+2])
        zz = a2*float(shift[i+2]) + b2*float(shift[i])
        
        sxx = a2*float(shielding[i]) + b2*float(shielding[i+1])
        syy = a2*float(shielding[i+1]) + b2*float(shielding[i+2])
        szz = a2*float(shielding[i+2]) + b2*float(shielding[i])
        
        shift[i] = xx
        shift[i+1] = yy
        shift[i+2] = zz
        
        shielding[i] = sxx
        shielding[i+1] = syy
        shielding[i+2] = szz
        
        i = i + 3
    msd = []
    
    while shift != [] or shielding != []:
        y = Map[0] * float(shift[0]) + Map[1]
        diff1 = float(shielding[0]) - y
        
        y = Map[0] * float(shift[1]) + Map[1]
        diff2 = float(shielding[1]) - y
        
        y = Map[0] * float(shift[2]) + Map[1]
        diff3 = float(shielding[2]) - y
        
        df1 = diff1**2
        df2 = diff2**2
        df3 = diff3**2
        
        Sum = df1 + df2 + df3
        df4 = Sum / 2.0
        
        msd.append(df1)
        msd.append(df2)
        msd.append(df3)
        msd.append(df4)
        
        shift.pop(0)
        shift.pop(0)
        shift.pop(0)
        shielding.pop(0)
        shielding.pop(0)
        shielding.pop(0)
    
    return msd

def GetFValues(msd, rms_ref):
    FValues = []
    
    while msd != []:
        FV1 = msd[0] / (rms_ref**2)
        FV2 = msd[1] / (rms_ref**2)
        FV3 = msd[2] / (rms_ref**2)
        FV4 = msd[3] / (rms_ref**2)
        
        FValues.append(FV1)
        FValues.append(FV2)
        FValues.append(FV3)
        FValues.append(FV4)
        
        msd.pop(0)
        msd.pop(0)
        msd.pop(0)
        msd.pop(0)
        
    return FValues

def LoadCoordinates(NMRFile):
    data = []
    
    hFile = open(NMRFile, 'r')
    line="not empty"
    
    while True:
        line = hFile.readline()
        if not line:
            break;
        item = line.split()
        data.append(item[0])
        data.append(float(item[4]))
        data.append(float(item[5]))
        data.append(float(item[6]))
    hFile.close()
    
    return data

def FindBoundary(Coordinates, BL, BH):
    i = 0
    empty = False
    
    if len(BL) < len(Coordinates):
        empty = True
        
    if len(BH) < len(Coordinates):
        empty = True
        
    while Coordinates != []:
        if empty:
            BL.append(Coordinates[0])
            BL.append(Coordinates[1])
            BL.append(Coordinates[2])
            BL.append(Coordinates[3])
        else:
            if BL[i+1] > Coordinates[1]:
                BL[i+1] = Coordinates[1]
            if BL[i+2] > Coordinates[2]:
                BL[i+2] = Coordinates[2]
            if BL[i+3] > Coordinates[3]:
                BL[i+3] = Coordinates[3]
            
        if empty:
            BH.append(Coordinates[0])
            BH.append(Coordinates[1])
            BH.append(Coordinates[2])
            BH.append(Coordinates[3])
        else:
            if BH[i+1] < Coordinates[1]:
                BH[i+1] = Coordinates[1]
            if BH[i+2] < Coordinates[2]:
                BH[i+2] = Coordinates[2]
            if BH[i+3] < Coordinates[3]:
                BH[i+3] = Coordinates[3]
        
        i = i + 4
        Coordinates.pop(0)
        Coordinates.pop(0)
        Coordinates.pop(0)
        Coordinates.pop(0)
        
    return None

def OutputBoundary(BL, BH):
    lineout = ""
    
    while BL != [] or BH != []:
        lineout = lineout + BL.pop(0) + " " + str(BL.pop(0)) + " " + str(BL.pop(0)) + " " + str(BL.pop(0)) + "\n"
        lineout = lineout + BH.pop(0) + " " + str(BH.pop(0)) + " " + str(BH.pop(0)) + " " + str(BH.pop(0)) + "\n"
        lineout = lineout + "\n"
        
    hFile = open("ErrorBars.txt", 'w')
    hFile.write(lineout)
    hFile.close()
    
    return None

def LoadRetainedStructures():
    try:
        hFile = open("retained_structs.txt", "r")
    except:
        return False
    rs = []

    while True:
        line = hFile.readline()
        if not line:
            hFile.close()
            return rs
        try:
            rs.append(int(line))
        except:
            hFile.close()
            return rs
