# Set the variables for various options here
InputFileName = "arginine.txt"
UnitCellParam = "arginine.unitcell"
NMRExpFile = "arginine.shift"
InputFormat = "cart"
SimRadius_H = 0.04
SimRadius_C = 0.015
SimRadius_O = 0.015
SimRadius_N = 0.015
SimRadius_S = 0.0
SimRadius_Cl= 0.0
SimList = []
NumOfSteps = 100
TheMap = (-1.0459,242.36)

from MonteCarloSim import *
from FileIO import *
from Analysis import *

opcode = 2

if opcode == 1:
    unitcell_param = LoadUnitCellParameters(UnitCellParam)
    
    a = unitcell_param[0]
    b = unitcell_param[1]
    c = unitcell_param[2]
    alpha = unitcell_param[3]
    beta = unitcell_param[4]
    gamma = unitcell_param[5]
    SymOps = unitcell_param[6]
    
    cell = ('%BLOCK LATTICE_ABC\n',str(a) + ' ' + str(b) + ' ' + str(c) + '\n',str(alpha) + ' ' + str(beta) + ' ' + str(gamma) + '\n',
            '%ENDBLOCK LATTICE_ABC\n\n', 'fix_all_cell : true\n', "symmetry_generate\n", 'fix_com : false\n',
            "kpoints_mp_spacing : 0.05\n\n")
    param = ('xcfunctional : PW91\n','opt_strategy : speed\n','task : magres\n','fix_occupancy : true\n',
            'finite_basis_corr : 0\n','elec_energy_tol : 1.0e-8\n','basis_precision : precise\n', 'spin_polarized : false')
    
    OutputParams = (cell, param)
    SimRad = [SimRadius_H,SimRadius_C,SimRadius_O, SimRadius_N, SimRadius_S, SimRadius_Cl]
    parameters = (InputFileName,InputFormat,SimList,NumOfSteps,SimRad, unitcell_param)
    RunMonteCarlo(parameters, OutputParams, True)

# hook up to Castep if desired starting here
if opcode == 2:
    for i in range(NumOfSteps):
        NMRFiles = InputFileName + "." + str(i) + ".magres"
        NMROutput = InputFileName + "." + str(i) + ".nmr"
        ProcessNMROutputFile_Castep(NMRFiles, NMROutput)
    
    FileNum, R2 = FindBestFit(InputFileName, NMRExpFile, NumOfSteps, TheMap, True, True)
    print("Structure " + str(FileNum)+" has the best fit to the experimental data with R^2 value of " + str(R2) + ".")
    DisplayPoorFits(FileNum, InputFileName, NMRExpFile, TheMap)
