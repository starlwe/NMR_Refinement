import FileIO as F
import Analysis as A

NMRFile = "arginine.magres"
NMROutput = "arginine.nmr"
ShiftFile = "arginine.shift"
TheMap = (-1.0459, 242.36)
AtomToAssign = 'N'

F.ProcessNMROutputFile_Castep(NMRFile, NMROutput)
F.RemoveDuplicates(NMROutput)

shift_data = A.LoadShiftDataA(ShiftFile)
shielding_data = A.LoadShieldingData(NMROutput)

size = int(len(shielding_data) / 4)
idx = 0
for i in range(size):
    if shielding_data[idx][0] != AtomToAssign:
        shielding_data.pop(idx)
        shielding_data.pop(idx)
        shielding_data.pop(idx)
        shielding_data.pop(idx)
    else:
        idx = idx + 4

ShiftList = A.AssignShifts(shift_data, shielding_data, TheMap)
output = "Format: row x col where row is the list of shifts, "
output = output + "col is the list of shieldings\n"

size = int(len(ShiftList) / 2)

for i in range(size):
    output = output + str(ShiftList.pop(0)+1) + "x" + str(ShiftList.pop(0)+1) + "\n"
    
hFile = open('ShiftAssignment.txt', 'w')
hFile.write(output)
hFile.close()
