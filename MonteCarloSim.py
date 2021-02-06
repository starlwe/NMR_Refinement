from Atoms import *
from FractToXYZ import *
from FileIO import *
from SymmetryTable import *
import random as rnd
import matplotlib.pyplot as plt

def RunMonteCarlo(parameters, OutputParams, Debug=False):
    InputFileName = parameters[0]
    InputFormat = parameters[1]
    SimList = parameters[2]
    NumOfSteps = parameters[3]
    SimRad = parameters[4]
    unitcell_param = parameters[5]
    a = unitcell_param[0]
    b = unitcell_param[1]
    c = unitcell_param[2]
    alpha = unitcell_param[3]
    beta = unitcell_param[4]
    gamma = unitcell_param[5]
    SymOps = unitcell_param[6]
    
    if Debug == True:
        xp=[]
        yp=[]
        zp=[]
        
    if InputFormat == "fractional":
        data = LoadInputFileContents(InputFileName)
        data = ConvertFractToXYZ(data,a,b,c,alpha,beta,gamma)
    else:
        data = LoadInputFileContents(InputFileName)

    for i in range(NumOfSteps):
        datacopy = data[:]
        OutputContent = RunSimulation(SimList, SimRad, datacopy)
        if Debug == True:
            j = 0
            size = len(OutputContent)
            while size > 0:
                idx = j*4 + 1
                idy = j*4 + 2
                idz = j*4 + 3
                xp.append(OutputContent[idx])
                yp.append(OutputContent[idy])
                zp.append(OutputContent[idz])
                j = j + 1
                size = size - 4
        Output_Data = OutputContent[:]
        WriteCastepFiles(InputFileName, i, Output_Data, OutputParams)
        OutputContent = ConvertXYZToFrac(OutputContent, a, b, c, alpha, beta, gamma)
        FullUnitCell = ConvertToFullUnitCell(OutputContent, SymOps)
        WriteCastepFullUnitCell(InputFileName, i, FullUnitCell, OutputParams)
        
    if Debug == True:
        fig = plt.figure(figsize=(5,5), dpi=150, frameon=True)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel("x-coordinates in Ang")
        ax.set_ylabel("y-coordinates in Ang")
        ax.set_zlabel("z-coordinates in Ang")
        ax.set_title("Monte Carlo Sampling of Atom Positions")
        ax.scatter(xp,yp,zp)
        plt.show()
    return None

def RunSimulation(SimList, SimRad, data):
    H = SimRad[0]
    C = SimRad[1]
    O = SimRad[2]
    N = SimRad[3]
    S = SimRad[4]
    Cl = SimRad[5]
    
    size = len(data)
    List_of_Atoms = []
    
    while True:
        if size <= 0:
            break
        else:
            if SimList == []:
                atomtype = data.pop(0)
                x = float(data.pop(0))
                y = float(data.pop(0))
                z = float(data.pop(0))
                atom = Atoms(atomtype,x,y,z,True)
                List_of_Atoms.append(atom)
            else:
                if data[0] in SimList:
                    atomtype = data.pop(0)
                    x = float(data.pop(0))
                    y = float(data.pop(0))
                    z = float(data.pop(0))
                    atom = Atoms(atomtype,x,y,z,True)
                    List_of_Atoms.append(atom)
                else:
                    atomtype = data.pop(0)
                    x = float(data.pop(0))
                    y = float(data.pop(0))
                    z = float(data.pop(0))
                    atom = Atoms(atomtype,x,y,z,False)
                    List_of_Atoms.append(atom)
        size = size - 4
    
    contents = []
    for item in List_of_Atoms:
        ToSim = item.Sim
        if ToSim:
            x,y,z = SimFunc(item,H,C,O,N,S,Cl)
            contents.append(item._type)
            contents.append(x)
            contents.append(y)
            contents.append(z)
        else:
            contents.append(item._type)
            contents.append(item.x)
            contents.append(item.y)
            contents.append(item.z)
    return contents

def SimFunc(item,H,C,O,N,S,Cl):
    if len(item._type) > 1:
        twoletter = True
    else:
        twoletter = False
    while True:
        if item._type[0] == 'H':
            dx = rnd.uniform(-1,1) * H
            dy = rnd.uniform(-1,1) * H
            dz = rnd.uniform(-1,1) * H
        elif item._type[0] == 'C' and twoletter:
            if item._type[1].isnumeric() == True:
                dx = rnd.uniform(-1,1) * C
                dy = rnd.uniform(-1,1) * C
                dz = rnd.uniform(-1,1) * C
            elif item._type[1].isnumeric() == False and item._type[1] == 'l':
                dx = rnd.uniform(-1,1) * Cl
                dy = rnd.uniform(-1,1) * Cl
                dz = rnd.uniform(-1,1) * Cl
        elif item._type[0] == 'C' and not twoletter:
            dx = rnd.uniform(-1,1) * C
            dy = rnd.uniform(-1,1) * C
            dz = rnd.uniform(-1,1) * C
        elif item._type[0] == 'O':
            dx = rnd.uniform(-1,1) * O
            dy = rnd.uniform(-1,1) * O
            dz = rnd.uniform(-1,1) * O
        elif item._type[0] == 'N':
            dx = rnd.uniform(-1,1) * N
            dy = rnd.uniform(-1,1) * N
            dz = rnd.uniform(-1,1) * N
        elif item._type[0] == 'S':
            dx = rnd.uniform(-1,1) * S
            dy = rnd.uniform(-1,1) * S
            dz = rnd.uniform(-1,1) * S
        dr2 = dx**2 + dy**2 + dz**2
        dr = dr2**(1/2)
        if item._type[0] == 'H':
            if dr <= H:
                 x = item.x + dx
                 y = item.y + dy
                 z = item.z + dz
                 return x,y,z
        elif item._type[0] == 'C':
            if dr <= C:
                 x = item.x + dx
                 y = item.y + dy
                 z = item.z + dz
                 return x,y,z
        elif item._type[0] == 'O':
            if dr <= O:
                 x = item.x + dx
                 y = item.y + dy
                 z = item.z + dz
                 return x,y,z
        elif item._type[0] == 'N':
            if dr <= N:
                 x = item.x + dx
                 y = item.y + dy
                 z = item.z + dz
                 return x,y,z
        elif item._type[0] == 'S':
            if dr <= S:
                 x = item.x + dx
                 y = item.y + dy
                 z = item.z + dz
                 return x,y,z
        elif len(item._type) > 1 and item._type[0] == 'C' and item._type[1] == 'l':
            if dr <= Cl:
                 x = item.x + dx
                 y = item.y + dy
                 z = item.z + dz
                 return x,y,z

def ConvertToFullUnitCell(OutputContent, SymOps):
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
