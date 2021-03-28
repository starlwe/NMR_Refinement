import TE as T
import matplotlib.pyplot as plt

InputFileName = "arginine.txt"
Colors = {'C' : 'black', 'N' : 'blue', 'O' : 'red', 'H' : 'grey'}
ellipsoid_atom = "H19"

xset = []
yset = []
zset = []

retained_structures = T.LoadRetainedStructures()

for i in retained_structures:
    NMRFile = InputFileName + "." + str(i) + ".nmr"
    coord = T.LoadCoordinates(NMRFile)

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
        elif empty and coord[j][0] != ellipsoid_atom and coord[j][0] != 'H':
            stationary_atoms.append(coord[j][0])
            stationary_atoms.append(coord[j+1])
            stationary_atoms.append(coord[j+2])
            stationary_atoms.append(coord[j+3])


fig = plt.figure(figsize=(5,5), dpi=150, frameon=True)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("x-coordinates in Ang")
ax.set_ylabel("y-coordinates in Ang")
ax.set_zlabel("z-coordinates in Ang")
ax.set_title("Thermal Ellipsoid Plot")

for k in range(0, len(stationary_atoms), 4):
    ax.scatter(stationary_atoms[k+1], stationary_atoms[k+2], stationary_atoms[k+3], c=Colors[stationary_atoms[k]])
ax.scatter(xset,yset,zset, c='grey')
plt.show()
