__author__ = 'lostvisions'

from mpi4py import MPI
import sys
try:
    client_script = 'test_qsub.py'
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=[client_script], maxprocs=4)
except Exception as e:
    print e