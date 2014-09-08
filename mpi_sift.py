from random import randint
from time import sleep
import itertools
from ORB_match import ShowStuff
from SIFT_distance import touch_sift, compare_descriptors
from TimeKeeper import TimeKeeper
from file_utils import find_files

__author__ = 'lostvisions'

# code combined from http://stackoverflow.com/a/22952258
# https://www.tacc.utexas.edu/c/document_library/get_file?uuid=be16db01-57d9-4422-b5d5-17625445f351
# http://materials.jeremybejarano.com/MPIwithPython/collectiveCom.html


from mpi4py import MPI
import sys

IMAGE_LOCATION = ['']
OPENCV_LOCATION = ""
MAX_FILES = 100
DESCRIPTORS = [
    {
        'name': 'sift',
        'ext': '.sift'
    }
]

try:
    from local_settings import *
except ImportError as ie:
    print ie

def s_print(t):
    try:
        sys.stdout.write(t + '\n')
    except Exception as e:
        print "*****failed to safe print"

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

print('Helloworld! I am process %d of %d on %s.\n' % (rank, size, name))

# python doesn't have enums
tags = {
    'READY': 1,
    'DONE': 2,
    'EXIT': 3,
    'START': 4,
    'START_2': 5,
    'DONE_2': 6,
    'WAIT': 7
}

status = MPI.Status()   # get MPI status object

if rank == 0:

    timekeeper = TimeKeeper()
    timekeeper.time_now('start', True)

    # tasks = []
    # # Master process executes code below
    # for desc in DESCRIPTORS:
    #     files = find_files(
    #         IMAGE_LOCATION,
    #         max_files=MAX_FILES,
    #         filter_descriptor=desc['ext'],
    #         folder_spread=True
    #     )
    #     for file in files:
    #         tasks.append({
    #             'ext': desc['ext'],
    #             'image': file
    #         })
    tasks = find_files(
        IMAGE_LOCATION,
        max_files=MAX_FILES,
        filter_descriptor = 'sift',
        folder_spread=True
    )


    print 'found ' + str(len(tasks)) + ' files'
    task_index = 0
    task_finished_index = 0

    descriptor_paths = []
    tasks2 = []
    task_index2 = 0
    task2_finished_index = 0

    # timekeeper.time_now('Found files', True)

    num_workers = size - 1
    closed_workers = 0
    s_print("Master starting with {} workers".format(num_workers))

    number_sifts_written = 0

    task1_done = False

    weights = []

    while closed_workers < num_workers:
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        tag = status.Get_tag()

        if tag == tags['READY']:
            s_print ("Worker {} requesting task.".format(source))
            # Worker is ready, so send it a task

            if task_index < len(tasks):
                print("Sending task {} to worker {}".format(task_index, source))
                comm.send(tasks[task_index], dest=source, tag=tags['START'])
                print("Sent task {} to worker {}".format(task_index, source))

                task_index += 1

            else:
                if task_finished_index == len(tasks):
                    if not task1_done:
                        task1_done = True
                        #all task_1s_done, prepare task 2s here
                        print 'number of sifts written : ' + str(number_sifts_written)

                        print '\n*** sift paths ***'
                        print descriptor_paths

                        tasks2 = [list(x) for x in itertools.combinations(descriptor_paths, 2)]
                        print '\n*** combinations ***'
                        print 'There will be ' + str(len(tasks2)) + ' combination task2 sift matches'

                    # All task1's complete, start sending task2's
                    if task_index2 < len(tasks2) and len(tasks2) > 0:
                        print("Sending task2 {} to worker {}".format(task_index2, source))
                        comm.send(tasks2[task_index2], dest=source, tag=tags['START_2'])
                        print("Sent task2 {} to worker {}".format(task_index2, source))

                        task_index2 += 1
                    else:
                        print 'task_2_complete'

                        # s_print("\nAll tasks finished\n")
                        comm.send(None, dest=source, tag=tags['EXIT'])
                else:
                    print("Worker {} will be told to sleep and try again").format(source)
                    comm.send({'wait': True}, dest=source, tag=tags['WAIT'])


        elif tag == tags['DONE']:
            results = data
            print("Got data from worker {} : {}".format(source, results))

            if 'descriptor_path' in results:
                # print '*-*-*' + str(results['descriptor_path'])
                descriptor_paths.append(results['descriptor_path'])

            if 'had_to_create' in results and results['had_to_create']:
                number_sifts_written += 1
            task_finished_index += 1

        elif tag == tags['DONE_2']:
            results = data
            print("Got data from worker {} : {}".format(source, results))
            task2_finished_index += 1

            weight = {
                'img_a': results['img_path'][0],
                'img_b': results['img_path'][1],
                'weight': results['matches']
            }

            weights.append(weight)

        elif tag == tags['EXIT']:
            # print("Worker {} exited.".format(source))
            closed_workers += 1
            # timekeeper.time_now('worker {} exit'.format(source), True)

    timekeeper.time_now('master finished', True)

    s_print("Master finishing")
    print "Weights : "
    sorted_weights = sorted(weights, key=lambda k: k['weight'])
    for w in sorted_weights:
        print "img_a {} \nimg_b {} \nWeight {}\n".format(w['img_a'], w['img_b'], w['weight'])

    print "Wrote " + str(number_sifts_written) + ' new SIFT files.'
    print "Completed " + str(len(tasks)) + ' Tasks.'
    print "Completed " + str(len(tasks2)) + ' Matches.'

    best_match = sorted_weights[-3:]
    for b in best_match:
        print b

        ss = ShowStuff()
        ss.show_ORB(b['img_a'].replace('.sift', ''), b['img_b'].replace('.sift', ''))

else:
    # Worker processes execute code below
    s_print("I am a worker with rank {} on {}.".format(rank, name))
    while True:
        comm.send(None, dest=0, tag=tags['READY'])
        task = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()

        if tag == tags['WAIT']:
            sleep(1)
            result = {'done_waiting': True}
            comm.send(result, dest=0, tag=tags['READY'])

        if tag == tags['START']:
            had_to_create = touch_sift(task)
            # had_to_create = False
            print "\nWorker {} performed task1 job here : ".format(rank) + str(task) + "\n"
            result = {
                'task_no': 1,
                'img_path': task,
                'had_to_create': had_to_create,
                'descriptor_path': task + '.sift'
            }
            comm.send(result, dest=0, tag=tags['DONE'])

        elif tag == tags['START_2']:
            print "\nWorker {} performed task2 job here : ".format(rank) + str(task) + "\n"
            matches = compare_descriptors(task[0], task[1], 1.5)
            result = {
                'task_no': 2,
                'img_path': task,
                'did_task_2': True,
                'matches': matches
            }
            comm.send(result, dest=0, tag=tags['DONE_2'])

        elif tag == tags['EXIT']:
            # print('leaving worker loop')
            break

    comm.send(None, dest=0, tag=tags['EXIT'])
    s_print("Worker {} exiting".format(rank))
    # comm.Barrier()



comm.Barrier()
print 'All done'
MPI.Finalize()
sys.exit(0)