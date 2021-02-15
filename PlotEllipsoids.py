import TE as T
import matplotlib.pyplot as plt

InputFileName = "arginine.txt"
ellipsoid_atom = "H19"
fixed_atomtype = "N"


xset = []
yset = []
zset = []
stationary_atoms = []
empty = True

retained_structures = T.LoadRetainedStructures()

for i in retained_structures:
    NMRFile = InputFileName + "." + str(i) + ".nmr"
    coord = T.LoadCoordinates(NMRFile)
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
            
fig = plt.figure(figsize=(5,5), dpi=150, frameon=True)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("x-coordinates in Ang")
ax.set_ylabel("y-coordinates in Ang")
ax.set_zlabel("z-coordinates in Ang")
ax.set_title("Thermal Ellipsoid Plot")

for j in range(0, len(stationary_atoms), 3):
    ax.scatter(stationary_atoms[j], stationary_atoms[j+1], stationary_atoms[j+2], c='red')
ax.scatter(xset,yset,zset, c='blue')
plt.show()