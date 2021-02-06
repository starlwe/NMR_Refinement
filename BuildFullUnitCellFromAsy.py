from SymmetryTable import *
from ConvertFullUnitCell import *
from FileIO import *

InputFileName = "fudgiu.txt"
UnitCellParam = "fudgiu.unitcell"

unitcell_param = LoadUnitCellParameters(UnitCellParam)  
a = unitcell_param[0]
b = unitcell_param[1]
c = unitcell_param[2]
alpha = unitcell_param[3]
beta = unitcell_param[4]
gamma = unitcell_param[5]
SymOps = unitcell_param[6]

data = LoadInputFileContents(InputFileName)
out_data = ConvertToFullUnitCell(data, SymTable, SymOps)
WriteFullUnitCell(InputFileName, out_data)
