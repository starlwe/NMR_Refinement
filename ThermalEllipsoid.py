InputFileName = "arginine.txt"
NMRExpFile = "arginine.shift"
NumOfSamples = 1000
#TheMap = (-1.0459,242.36)
TheMap = (-1.0281,243.01)
rms_ref = 2.3
FRef = 2.0

import FileIO as F
import Analysis as A
import TE as T

shift_data = A.LoadShiftData(NMRExpFile)
StructuresToRetain = []

for i in range(NumOfSamples):
    NMRFiles = InputFileName + "." + str(i) + ".magres"
    NMROutput = InputFileName + "." + str(i) + ".nmr"
    F.ProcessNMROutputFile_Castep(NMRFiles, NMROutput)
    if F.RemoveDuplicates(NMROutput) == True:
    
        shielding_data = A.LoadShieldingData(NMROutput)
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
print("Structures retained: ")
for item in StructuresToRetain:
    print(item)

BL = []
BH = []

for j in range(NumStructs):
    k = StructuresToRetain[j]
    NMROutput = InputFileName + "." + str(k) + ".nmr"
    Coordinates = T.LoadCoordinates(NMROutput)
    T.FindBoundary(Coordinates, BL, BH)

T.OutputBoundary(BL, BH)
