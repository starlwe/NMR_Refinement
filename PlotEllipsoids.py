import TE as T
import matplotlib.pyplot as plt

InputFileName = "arginine.txt"
PlotAllAtoms = True
ColorList = []
ellipsoid_atom = "H19"
fixed_atomtype = "N"

xset = []
yset = []
zset = []

retained_structures = T.LoadRetainedStructures()

for i in retained_structures:
    NMRFile = InputFileName + "." + str(i) + ".nmr"
    coord = T.LoadCoordinates(NMRFile)

    if PlotAllAtoms:
        for j in range(0, len(coord), 4):
            if len(coord[j]) > 1 and coord[j][0] == 'H':
                ColorList.append('grey')
            elif len(coord[j]) > 1 and coord[j][0] == 'C' and coord[j][0:2] != 'Cl':
                ColorList.append('black')
            elif len(coord[j]) > 1 and coord[j][0] == 'O':
                ColorList.append('red')
            elif len(coord[j]) > 1 and coord[j][0] == 'N':
                ColorList.append('blue')
            xset.append(coord[j+1])
            yset.append(coord[j+2])
            zset.append(coord[j+3])
    else:
        stationary_atoms = []
        empty = True
    
        if len(stationary_atoms) == 0:
            empty = True
        else:
            empty = False
        for j in range(0, len(coord), 4):
            if coord[j] == ellipsoid_atom:
                xset.append(coord[j+1])
                yset.append(coord[j+2])
                zset.append(coord[j+3])
            if empty and coord[j][0] == fixed_atomtype:
                stationary_atoms.append(coord[j+1])
                stationary_atoms.append(coord[j+2])
                stationary_atoms.append(coord[j+3])

if PlotAllAtoms:
    fig = plt.figure(figsize=(5,5), dpi=150, frameon=True)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("x-coordinates in Ang")
    ax.set_ylabel("y-coordinates in Ang")
    ax.set_zlabel("z-coordinates in Ang")
    ax.set_title("Thermal Ellipsoid Plot")
    
    for k in range(len(ColorList)):
        fig = ax.scatter(xset[k],yset[k],zset[k], c=ColorList[k])
    plt.show()
else:
    fig = plt.figure(figsize=(5,5), dpi=150, frameon=True)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("x-coordinates in Ang")
    ax.set_ylabel("y-coordinates in Ang")
    ax.set_zlabel("z-coordinates in Ang")
    ax.set_title("Thermal Ellipsoid Plot")

    for k in range(0, len(stationary_atoms), 3):
        ax.scatter(stationary_atoms[k], stationary_atoms[k+1], stationary_atoms[k+2], c='blue')
    ax.scatter(xset,yset,zset, c='grey')
    plt.show()
