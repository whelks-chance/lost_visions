from random import randint
from time import sleep
from SIFT_distance import touch_sift
from file_utils import find_files

__author__ = 'lostvisions'

# code combined from http://stackoverflow.com/a/22952258
# https://www.tacc.utexas.edu/c/document_library/get_file?uuid=be16db01-57d9-4422-b5d5-17625445f351
# http://materials.jeremybejarano.com/MPIwithPython/collectiveCom.html


from mpi4py import MPI
import sys



def s_print(t):
    # try/:
    sys.stdout.write(t + '\n')
    # except Exception as e:
    #     print "*****failed to safe print"

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

print('Helloworld! I am process %d of %d on %s.\n' % (rank, size, name))

tags = {
    'READY': 0,
    'DONE': 1,
    'EXIT': 2,
    'START': 3
}

status = MPI.Status()   # get MPI status object
try:
    if rank == 0:
        # Master process executes code below
        # tasks = range(2*size)

        # tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']

        tasks = find_files(['./image_link/bl_images'], max_files=1000)

        task_index = 0
        num_workers = size - 1
        closed_workers = 0
        s_print("Master starting with {} workers".format(num_workers))

        number_sifts_written = 0

        while closed_workers < num_workers:
            data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            source = status.Get_source()
            tag = status.Get_tag()
            if tag == tags['READY']:
                s_print ("Worker {} requesting task.".format(source))
                # Worker is ready, so send it a task
                if task_index < len(tasks):
                    comm.send(tasks[task_index], dest=source, tag=tags['START'])
                    print("Sending task {} to worker {}".format(task_index, source))
                    task_index += 1
                else:
                    # s_print("\nAll tasks finished\n")
                    comm.send(None, dest=source, tag=tags['EXIT'])
            elif tag == tags['DONE']:
                results = data
                print("Got data from worker {} : {}".format(source, results))
                if results['had_to_create']:
                    number_sifts_written += 1
            elif tag == tags['EXIT']:
                # print("Worker {} exited.".format(source))
                closed_workers += 1
        s_print("Master finishing")
        print "Wrote " + str(number_sifts_written) + ' new SIFT files.'
        print "Completed " + str(len(tasks)) + ' Tasks.'
    else:
        # Worker processes execute code below
        s_print("I am a worker with rank {} on {}.".format(rank, name))
        while True:
            comm.send(None, dest=0, tag=tags['READY'])
            task = comm.recv(source=0, tag=MPI.ANY_SOURCE, status=status)
            tag = status.Get_tag()

            if tag == tags['START']:
                # sleep(randint(0, 5))
                # Do the work here
                # result = task**2
                # a = 0
                # b = 0
                # c = 0
                # for a in range(1000):
                #     for b in range(1000):
                #         c += a + b
                # result = task + "-ok-" + str(c)

                had_to_create = touch_sift(task)
                result = {
                    'img_path': task,
                    'had_to_create': had_to_create
                }
                comm.send(result, dest=0, tag=tags['DONE'])
            elif tag == tags['EXIT']:
                # print('leaving worker loop')
                break

        comm.send(None, dest=0, tag=tags['EXIT'])
        s_print("Worker {} exiting".format(rank))
        # comm.Barrier()
except Exception as e:
    s_print(str(e))


comm.Barrier()
print 'All done'
MPI.Finalize()
sys.exit(0)