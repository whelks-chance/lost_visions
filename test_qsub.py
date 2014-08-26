__author__ = 'lostvisions'

from mpi4py import MPI
import sys

def s_print(t):
    sys.stdout.write(t + '\n')

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

print('Helloworld! I am process %d of %d on %s.\n' % (rank, size, name))

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    comm.bcast(data, root=0)
    s_print("Message sent, data is: " + str(data))
else:
    data = comm.recv(source=0)
    s_print("Rank " + str(rank) + " Received data : " + str(data))


