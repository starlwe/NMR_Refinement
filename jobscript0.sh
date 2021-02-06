#!/bin/bash

#SBATCH --time=6:00:00
#SBATCH --ntasks=64
#SBATCH --mem-per-cpu=2048M
#SBATCH -C 'avx2'
#SBATCH -J "Castep"

export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

module load gcc openmpi

mpiexec -n 64 /fslhome/starlwe/castep.mpi arginine.txt.0
