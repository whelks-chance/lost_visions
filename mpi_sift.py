import os
import pprint
from time import sleep
import itertools
# from ORB_match import ShowStuff
from ORB_processor import ORB_processor
from SIFT_processor import SIFT_processor
from TimeKeeper import TimeKeeper
from file_utils import find_files
from graphs import create_graph

__author__ = 'lostvisions'

# code combined from http://stackoverflow.com/a/22952258
# https://www.tacc.utexas.edu/c/document_library/get_file?uuid=be16db01-57d9-4422-b5d5-17625445f351
# http://materials.jeremybejarano.com/MPIwithPython/collectiveCom.html

#now so heavily messed with, the above cannot be held responsible for its current form


from mpi4py import MPI
import sys

#  All these willbe overwritten with locat settings
IMAGE_LOCATIONS = ['']
OUTPUT_PATH = ''
OPENCV_LOCATION = ""
MAX_FILES = 100
DESCRIPTORS = [
    {
        'name': 'sift',
        'ext': '.sift',
        'path': './outputs/sift/'
    }
]

DO_TASKS = {
    'create_descriptors': True,
    'save_descriptor_paths': True,
    'match_descriptors': True,
    'save_matches': True,
    'create_graphs': True
}

# Ignore all above, placeholders only

try:
    from local_settings import *
except ImportError as ie:
    print ie


def s_print(t):
    try:
        sys.stdout.write(t + '\n')
    except Exception as e:
        print "*****failed to safe print"


def get_descriptor_processor(ext):
    if ext in '.sift':
        return SIFT_processor()
    if ext in '.orb':
        return ORB_processor()

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

    tasks = []
    # Master process executes code below


    # Find files
    # For the moment skip any clever filtering of existing descriptor existance
    # TODO come back and add this in

    files = find_files(
        IMAGE_LOCATIONS,
        max_files=MAX_FILES,
        filter_descriptor=None,
        folder_spread=True
    )
    tasks = []

    for fi in files:
        f = files[fi]

        for parent_path in IMAGE_LOCATIONS:
            if parent_path in f:

                # TODO yeah....
                rel_path = os.path.relpath(f, os.path.join(parent_path, '..'))
        # root_dir = os.path.dirname(os.path.realpath(f))
                new_path = os.path.join(OUTPUT_PATH, rel_path)
        try:
            os.makedirs(new_path)
        except:
            pass

        if DO_TASKS['create_descriptors']:
            for desc in DESCRIPTORS:
                tasks.append({
                    'img_path': f,
                    'descriptor': desc['ext'],
                    'output_path': new_path
                })

    print 'Created ' + str(len(tasks)) + ' tasks; ' \
          + str(len(files)) + ' files and ' + str(len(DESCRIPTORS)) + ' descriptors'

    for t in tasks:
        print pprint.pformat(t, indent=1, width=80, depth=None)

    task_index = 0
    task_finished_index = 0

    descriptor_paths = dict()
    tasks2 = []
    task_index2 = 0
    task2_finished_index = 0

    timekeeper.time_now('Found files', True)

    num_workers = size - 1
    closed_workers = 0
    s_print("Master starting with {} workers".format(num_workers))

    number_descriptors_written = 0

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
                        timekeeper.time_now('descriptors written', True)

                        print 'number of descriptors written : ' + str(number_descriptors_written)

                        print '\n*** descriptor paths ***'
                        print pprint.pformat(descriptor_paths, indent=1, width=80, depth=None)

                        # For each descriptor in the paths returned, calculate all the pairs for comparisons
                        # These become the "task2"s which return similarities between images.
                        if DO_TASKS['match_descriptors']:
                            for descriptor_key in descriptor_paths:
                                for pair in (list(x) for x in itertools.combinations(descriptor_paths[descriptor_key], 2)):
                                    tasks2.append({
                                        'descriptor':descriptor_key,
                                        'd1': pair[0],
                                        'd2': pair[1]
                                    })

                        # tasks2 = [list(x) for x in itertools.combinations(descriptor_paths, 2)]
                        print '\n*** combinations ***'
                        print 'There will be ' + str(len(tasks2)) + ' combination task2 descriptor matches'
                        print pprint.pformat(tasks2, indent=1, width=80, depth=None)

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
                    print("Worker {} will be told to sleep and try again".format(source))
                    comm.send({'wait': True}, dest=source, tag=tags['WAIT'])

        elif tag == tags['DONE']:
            results = data
            print("Got data from worker {} : {}\n".format(source, pprint.pformat(
                results, indent=1, width=80, depth=None
            )))

            if results['success']:
                # if 'descriptor_path' in results:
                    # print '*-*-*' + str(results['descriptor_path'])
                    # descriptor_paths.append({
                    #     'descriptor_path': results['descriptor_path'],
                    #     'descriptor': results['descriptor']
                    # })
                if not results['descriptor'] in descriptor_paths:
                    descriptor_paths[results['descriptor']] = []
                descriptor_paths.get(results['descriptor']).append({
                    'descriptor_path': results['descriptor_path'],
                    'image': results['img_path']
                })

                # print pprint.pformat(descriptor_paths, indent=1, width=80, depth=None)

                if 'had_to_create' in results and results['had_to_create']:
                    number_descriptors_written += 1
            task_finished_index += 1

        elif tag == tags['DONE_2']:
            results = data
            print("Got data from worker {} : {}\n".format(source, pprint.pformat(
                results, indent=1, width=80, depth=None
            )))

            task2_finished_index += 1

            weight = {
                'descriptor': results['descriptor'],
                'img_a': results['img_path_1'],
                'img_b': results['img_path_2'],
                'descriptor_1': results['descriptor_1'],
                'descriptor_2': results['descriptor_2'],
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
        print "img_a {} \nimg_b {} \nWeight {}\nDESC {}".format(w['img_a'], w['img_b'], w['weight'], w['descriptor'])

    print "Wrote " + str(number_descriptors_written) + ' new Descriptor files.'
    print "Completed " + str(len(tasks)) + ' Tasks.'
    print "Completed " + str(len(tasks2)) + ' Matches.'

    best_match = sorted_weights[-3:]
    for b in best_match:
        print '\n{}\n'.format(pprint.pformat(b, indent=1, width=80, depth=None))

        #TODO, this is daft
        # ss = ShowStuff()
        # ss.show_ORB(b['img_a'].replace('.sift', ''), b['img_b'].replace('.sift', ''))

    if DO_TASKS['save_descriptor_paths']:
        with open('descriptor_paths.txt', 'wb') as f1:
            f1.write(pprint.pformat(descriptor_paths, indent=1, width=80, depth=None))
        f1.close()

    if DO_TASKS['save_matches']:
        with open('matches_data.txt', 'wb') as f2:
            f2.write(pprint.pformat(sorted_weights, indent=1, width=80, depth=None))
        f2.close()

    if DO_TASKS['create_graphs']:
        create_graph(sorted_weights)
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

            desc_proc = get_descriptor_processor(task['descriptor'])
            creation_response = desc_proc.touch_descriptor(task['img_path'],
                                             detector_ext=task['descriptor'],
                                             output_path=task['output_path'])
            # had_to_create = False
            print "\nWorker {} performed task1 job here :\n {}\n".format(rank,
                                                                         pprint.pformat(
                                                                             task, indent=1, width=80, depth=None
                                                                         ))
            result = {
                'task_no': 1,
                'processing_class': desc_proc.name,
                'img_path': task['img_path'],
                'had_to_create': creation_response.had_to_create,
                'descriptor': task['descriptor'],
                'descriptor_path': creation_response.descriptor_path,
                # if error is None, we're al good
                'success': creation_response.error is None
            }
            comm.send(result, dest=0, tag=tags['DONE'])

        elif tag == tags['START_2']:
            print "\nWorker {} performed task2 job here : ".format(rank) + str(task) + "\n"

            desc_proc = get_descriptor_processor(task['descriptor'])

            matches = desc_proc.compare_descriptors(task['d1']['descriptor_path'], task['d2']['descriptor_path'], 1.5)
            result = {
                'task_no': 2,
                'descriptor': task['descriptor'],
                'img_path_1': task['d1']['image'],
                'img_path_2': task['d2']['image'],
                'descriptor_1': task['d1']['descriptor_path'],
                'descriptor_2': task['d2']['descriptor_path'],
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