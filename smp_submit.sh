#!/bin/bash
#PBS -l select=1:ncpus=4:mpiprocs=4
#PBS -l place=scatter:excl
#PBS -q SMP_queue
#PBS -o output.txt
#PBS -e error.txt
#PBS -N lv_hello_world
#PBS -l walltime=1:00:00

module load intel/intel
module load compiler/gnu-4.6.2

module load mpfr/3.1.0
module load gmp/5.0.2
module load mpc/0.9
module load mpi/openmpi
module load mpi4py/1.3

mpirun -np 4 $HOME/c_test/myenv/bin/python $HOME/sift_creation/lost_visions/mpi_sift.py
