import os
import cPickle
import threading
import cv2
import numpy as np
import nltk

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


class ImageDescriptor():
    def __init__(self, img_path):
        self.img_path = img_path

    def get_sift(self, detector=None, create_file=True):
        if detector is None:
            detector = cv2.SIFT()

        if os.path.isfile(self.img_path + '.sift'):
            with open(self.img_path + '.sift', 'rb') as f:
                keypoints, descriptors = unpickle_keypoints( cPickle.load(f) )
        else:
            img = cv2.imread(self.img_path)
            img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
            keypoints, descriptors = detector.detectAndCompute(img_gray, None)

            key_desc_temp = pickle_keypoints(keypoints, descriptors)

            if create_file:
                with open(self.img_path + '.sift', 'wb') as f:
                    cPickle.dump(key_desc_temp, f, protocol=cPickle.HIGHEST_PROTOCOL)
        return keypoints, descriptors


def iterall(files_list, match_thresh=1.5):

    detector = cv2.SIFT()
    all_descriptors = {}
    descriptor_distances = {}
    desc_strings = {}
    weighted_strings = {}

    for img_idx in files_list:
        img_path = files_list[img_idx]
        print str(img_idx) + ' : ' + img_path

        if os.path.isfile(img_path + '.sift'):
            print 'found sift file : ' + img_path + '.sift'
            with open(img_path + '.sift', 'rb') as f:
                keypoints, descriptors = unpickle_keypoints( cPickle.load(f) )
        else:
            print 'didnt find sift file : ' + img_path + '.sift'
            img = cv2.imread(img_path)
            img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
            keypoints, descriptors = detector.detectAndCompute(img_gray, None)

            key_desc_temp = pickle_keypoints(keypoints, descriptors)

            with open(img_path + '.sift', 'wb') as f:
                cPickle.dump(key_desc_temp, f, protocol=cPickle.HIGHEST_PROTOCOL)

                # all_descriptors[idx] = descriptors

    thread_pool = []

    for file_a in files_list:
        print '\nComparing file ' + str(file_a) + ' to : '

        descriptor_orders = {}
        weighted_orders = {}
        for file_b in files_list:
            print file_b,
            if file_a != file_b:
                with open(files_list[file_a] + '.sift', 'rb') as fa:
                    keypoints_a, descriptors_a = unpickle_keypoints( cPickle.load(fa) )
                with open(files_list[file_b] + '.sift', 'rb') as fb:
                    keypoints_b, descriptors_b = unpickle_keypoints( cPickle.load(fb) )

                # t = threading.Thread(target=find_matches, args=(str(file_a) + ',' + str(file_b),
                #                                                 descriptors_a,
                #                                                 descriptors_b,
                #                                                 match_thresh))
                # thread_pool.append(t)

                matches_size = find_matches(str(file_a) + ',' + str(file_b),
                                            descriptors_a,
                                            descriptors_b,
                                            match_thresh)
                descriptor_orders[str(file_b)] = matches_size

                weighted_orders[str(file_b)] = (str(file_b) + '=' + str(matches_size)) + ':'

                descriptor_distances[str(file_a) + ':' + str(file_b)] = matches_size

        print '\nImage ' + files_list[file_a] + ' is most similar to ' \
              + files_list[int(list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True))[0])] + '\n'

        desc_arr = list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True))

        item_string = ''
        for item in desc_arr:
            item_string += str(weighted_orders[item])
        weighted_strings[file_a] = item_string

        desc_strings[file_a] = ' '.join(desc_arr)
        print 'Array of img_idx for file ' + str(file_a) + ', closest match first : \n' \
              + desc_strings[file_a]

    print '\n****\nArray of distances between images : \n' + str(descriptor_distances)

    # for descriptor_a in all_descriptors:
    #     # print 'descriptors for ' + str(descriptor_a) + str(files[descriptor_a])
    #     # print len(all_descriptors[descriptor_a])
    #
    #     descriptor_orders = {}
    #     for descriptor_b in all_descriptors:
    #
    #         if descriptor_a != descriptor_b:
    #
    #             # print 'comparing to ' + str(descriptor_b) + str(files[descriptor_b])
    #             # print len(all_descriptors[descriptor_b])
    #
    #             matches_size = find_matches(str(descriptor_a) + ',' + str(descriptor_b),
    #                                         all_descriptors[descriptor_a],
    #                                         all_descriptors[descriptor_b],
    #                                         match_thresh)
    #             descriptor_orders[str(descriptor_b)] = matches_size
    #             descriptor_distances[str(descriptor_a) + ':' + str(descriptor_b)] = matches_size
    #
    #             # for w in sorted(descriptor_orders, key=descriptor_orders.get, reverse=True):
    #             #     print w, descriptor_orders[w]
    #
    #     print '\nImage ' + files_list[descriptor_a] + ' is most similar to ' \
    #           + files_list[int(list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True))[0])] + '\n'
    #
    #     desc_arr = list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True))
    #
    #     desc_strings[descriptor_a] = ' '.join(desc_arr)
    #
    #     print descriptor_distances

    for ws in weighted_strings:
        print str(ws) + ' : ' + weighted_strings[ws]

    print '\n****\nAll images description strings : \n' + str(desc_strings)
    for s in desc_strings:
        for st in desc_strings:
            dist = nltk.metrics.edit_distance(
                desc_strings[s],
                desc_strings[st])
            if (len(files_list) * 0.3) < dist < (len(files_list) * 0.8):
                print '\n****\nClosest image pair signatures within 0.8 of each other:'
                print str(s) + ' : ' + desc_strings[s]
                print str(st) + ' : ' + desc_strings[st]
                print 'Deviation of sigs (lower is better) : ' + str(dist)
                print files_list[s]
                print files_list[st]
                print '\n'

                # print str(s) + ' : ' + desc_strings[s]


def pickle_keypoints(keypoints, descriptors):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
        i += 1
        temp_array.append(temp)
    return temp_array

def unpickle_keypoints(array):
    keypoints = []
    descriptors = []
    for point in array:
        temp_feature = cv2.KeyPoint(
            x=point[0][0],
            y=point[0][1],
            _size=point[1],
            _angle=point[2],
            _response=point[3],
            _octave=point[4],
            _class_id=point[5]
        )

        temp_descriptor = point[6]
        keypoints.append(temp_feature)
        descriptors.append(temp_descriptor)
    return keypoints, np.array(descriptors)

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
        # print folder
        for a_file in os.listdir(folder):
            # print a_file
            fileName, fileExtension = os.path.splitext(a_file)

            if os.path.isfile(os.path.join(folder, a_file)) and '.sift' not in fileExtension:
                all_files.append(os.path.join(folder, a_file))

    files_dict = {}
    for f in all_files[:10]:
        files_dict[int(len(files_dict))] = f

    print str(files_dict) + '\n\n****\n'
    return files_dict


to_match = find_files(['./map', './animals', './portrait'])

iterall(to_match, 1.5)