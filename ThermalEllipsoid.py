InputFileName = "arginine.txt"
NMRExpFile = "arginine.shift"
NumOfSamples = 4000
TheMap = (-1.0281,243.01)
rms_ref = 2.3
FRef = 1.5

import FileIO as F
import Analysis as A
import TE as T

shift_data = A.LoadShiftData(NMRExpFile)
StructuresToRetain = []

for i in range(NumOfSamples):
    if i % (NumOfSamples/10) == 0:
        count = i/NumOfSamples * 100
        print(str(count) + "% complete.")
    NMRFiles = InputFileName + "." + str(i) + ".magres"
    NMROutput = InputFileName + "." + str(i) + ".nmr"
    NMROutNoDup = InputFileName + "." + str(i) + ".nnd"
    F.ProcessNMROutputFile_Castep(NMRFiles, NMROutput)
    if F.RemoveDuplicates(NMROutput, NMROutNoDup) == True:
    
        shielding_data = A.LoadShieldingData(NMROutNoDup)
        shift_copy = shift_data[:]
    
        shift, shielding = T.ProcessData(shift_copy, shielding_data, TheMap)
        msd = T.CalculateMSD(shift, shielding, TheMap)
        FValues = T.GetFValues(msd, rms_ref)
        retain = True
    
        while FValues != []:
            FVal = FValues.pop(0)
            if FVal > FRef:
                retain = False
    
        if retain:
            StructuresToRetain.append(i)

NumStructs = len(StructuresToRetain)
print("Number of Structures Retained: " + str(NumStructs))

Output = open("retained_structs.txt", "w")
lineout = ""
for item in StructuresToRetain:
    lineout = lineout + str(item) + "\n"
Output.write(lineout)
Output.close()

BL = []
BH = []

for j in range(NumStructs):
    k = StructuresToRetain[j]
    NMROutput = InputFileName + "." + str(k) + ".nnd"
    Coordinates = T.LoadCoordinates(NMROutput)
    T.FindBoundary(Coordinates, BL, BH)

T.OutputBoundary(BL, BH)
