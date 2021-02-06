for i in range(100):
    contents = "#!/bin/bash"
    contents = contents + "\n\n"
    contents = contents + "#SBATCH --time=6:00:00\n"
    contents = contents + "#SBATCH --ntasks=64\n"
    contents = contents + "#SBATCH --mem-per-cpu=2048M\n"
    contents = contents + "#SBATCH -C 'avx2'\n"
    contents = contents + '#SBATCH -J "Castep"\n\n'
    contents = contents + "export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE\n\n"
    contents = contents + "module load gcc openmpi\n\n"
    contents = contents + "mpiexec -n 64 /fslhome/starlwe/castep.mpi arginine.txt." + str(i) + '\n'
    file = "jobscript" + str(i) + ".sh"
    hOut = open(file, 'w')
    hOut.write(contents)
    hOut.close()
