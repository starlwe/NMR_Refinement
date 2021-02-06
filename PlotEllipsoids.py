import random as rnd
import matplotlib.pyplot as plt

xmin = 0.37638
xmax = 1.0021
ymin = -1.79483
ymax = 1.4617
zmin = -1.16424
zmax = 2.3422

xset = []
yset = []
zset = []

atom1 = [0,0,1.3678]
atom2 = [2.1232,0,-0.58421]

for i in range(1500):
    xset.append(rnd.uniform(xmin, xmax))
    yset.append(rnd.uniform(ymin, ymax))
    zset.append(rnd.uniform(zmin, zmax))

fig = plt.figure(figsize=(5,5), dpi=150, frameon=True)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("x-coordinates in Ang")
ax.set_ylabel("y-coordinates in Ang")
ax.set_zlabel("z-coordinates in Ang")
ax.set_title("Thermal Ellipsoid Plot")
ax.scatter(atom1[0],atom1[1],atom1[2], c='red')
ax.scatter(atom2[0],atom2[1],atom2[2], c='red')
ax.scatter(xset,yset,zset, c='blue')
plt.show()
