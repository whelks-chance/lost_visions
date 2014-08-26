__author__ = 'lostvisions'

# code combined from http://stackoverflow.com/a/22952258
# https://www.tacc.utexas.edu/c/document_library/get_file?uuid=be16db01-57d9-4422-b5d5-17625445f351
# http://materials.jeremybejarano.com/MPIwithPython/collectiveCom.html


from mpi4py import MPI
import sys

def s_print(t):
    sys.stdout.write(t + '\n')

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

print('Helloworld! I am process %d of %d on %s.\n' % (rank, size, name))

def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START')

status = MPI.Status()   # get MPI status object

if rank == 0:
    # Master process executes code below
    # tasks = range(2*size)

    tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']

    task_index = 0
    num_workers = size - 1
    closed_workers = 0
    s_print("Master starting with {} workers".format(num_workers))
    while closed_workers < num_workers:
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        tag = status.Get_tag()
        if tag == tags.READY:
            # Worker is ready, so send it a task
            if task_index < len(tasks):
                comm.send(tasks[task_index], dest=source, tag=tags.START)
                print("Sending task {} to worker {}".format(task_index, source))
                task_index += 1
            else:
                comm.send(None, dest=source, tag=tags.EXIT)
        elif tag == tags.DONE:
            results = data
            print("Got data from worker {} : {}".format(source, results))
        elif tag == tags.EXIT:
            print("Worker {} exited.".format(source))
            closed_workers += 1

    print("Master finishing")
else:
    # Worker processes execute code below
    s_print("I am a worker with rank {} on {}.".format(rank, name))
    while True:
        comm.send(None, dest=0, tag=tags.READY)
        task = comm.recv(source=0, tag=MPI.ANY_SOURCE, status=status)
        tag = status.Get_tag()

        if tag == tags.START:
            # Do the work here
            # result = task**2
            # a = 0
            # b = 0
            # c = 0
            # while a < 10000:
            #     a += 1
            #     while b < 10000:
            #         b += 1
            #         c = a + b
            result = task + "-ok-"
            comm.send(result, dest=0, tag=tags.DONE)
        elif tag == tags.EXIT:
            break

    comm.send(None, dest=0, tag=tags.EXIT)

