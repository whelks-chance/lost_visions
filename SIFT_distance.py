import os
import cv2
import numpy as np

__author__ = 'ubuntu'


files = [
    './maps_small/af.jpg',
    './maps_small/sa.jpg',
    './maps_small/uk.jpg',
    './map/11002054014_84bd33c2d0_z.jpg',
    './map/11002526453_7abdd80dc0_z.jpg',
    './portrait/11040852736_83cc5c2155_z.jpg',
    './portrait/11045912473_da4f27de0a_z.jpg',
    './portrait/11068132784_eed4264f41_z.jpg'
]

def iterall(files_list, match_thresh=1.5):

    detector = cv2.SIFT()
    all_descriptors = {}
    descriptor_distances = {}
    desc_strings = {}

    for idx, img_path in enumerate(files_list):
        print str(idx) + ' : ' + str(img_path)

        img = cv2.imread(img_path)
        img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
        keypoints, descriptors = detector.detectAndCompute(img_gray, None)

        all_descriptors[idx] = descriptors

    for descriptor_a in all_descriptors:
        # print 'descriptors for ' + str(descriptor_a) + str(files[descriptor_a])
        # print len(all_descriptors[descriptor_a])

        descriptor_orders = {}
        for descriptor_b in all_descriptors:

            if descriptor_a != descriptor_b:

                # print 'comparing to ' + str(descriptor_b) + str(files[descriptor_b])
                # print len(all_descriptors[descriptor_b])

                matches_size = find_matches(str(descriptor_a) + ',' + str(descriptor_b),
                                            all_descriptors[descriptor_a],
                                            all_descriptors[descriptor_b],
                                            match_thresh)
                descriptor_orders[str(descriptor_b)] = matches_size
                descriptor_distances[str(descriptor_a) + ':' + str(descriptor_b)] = matches_size

                # for w in sorted(descriptor_orders, key=descriptor_orders.get, reverse=True):
                #     print w, descriptor_orders[w]

        print '\nImage ' + files_list[descriptor_a] + ' is most similar to ' \
              + files_list[int(list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True))[0])] + '\n'

        desc_string =  str(list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True)))

        desc_strings[descriptor_a] = desc_string

        # print descriptor_distances

    for s in desc_strings:
        print s + ' : ' + desc_strings[s]

def start():
    img_a = cv2.imread('./maps_small/af.jpg')

    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)

    detector = cv2.SIFT()
    keypoints_a, descriptors_a = detector.detectAndCompute(img_a, None)




    img_b = cv2.imread('./maps_small/sa.jpg')

    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)

    detector = cv2.SIFT()
    keypoints_b, descriptors_b = detector.detectAndCompute(img_b, None)

    print find_matches('ab', descriptors_a, descriptors_b, 1.5)



    img_c = cv2.imread('./maps_small/uk.jpg')

    img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)

    detector = cv2.SIFT()
    keypoints_c, descriptors_c = detector.detectAndCompute(img_c, None)

    print find_matches('ac', descriptors_a, descriptors_c, 1.5)


def find_matches(desc, template_descriptors, current_img_descriptors, match_thresh):
    # print '\n*'
    # print desc
    # print len(template_descriptors)
    # print len(current_img_descriptors)
    # print '*\n'

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(current_img_descriptors, flann_params)
    idx, dist = flann.knnSearch(template_descriptors, 2, params={})
    del flann
    matches = np.c_[np.arange(len(idx)), idx[:,0]]
    pass_filter = dist[:,0]*match_thresh < dist[:,1]
    matches = matches[pass_filter]

    return len(matches)


def find_files(folders):
    all_files = []
    for folder in folders:
        print folder
        for a_file in os.listdir(folder):
            print a_file
            if os.path.isfile(os.path.join(folder, a_file)):
                all_files.append(os.path.join(folder, a_file))

    return all_files

to_match = find_files(['./map', './animals', './portrait'])

iterall(to_match, 1.5)