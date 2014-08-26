import os
import cPickle
import threading
import cv2
import numpy as np
# from datetime import time, datetime
import nltk
from TimeKeeper import TimeKeeper

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
    def __init__(self, img_idx, img_path):
        self.img_idx = img_idx
        self.img_path = img_path
        self.weights = {}

    def get_sift(self, detector=None, create_file=True):
        if detector is None:
            detector = cv2.SIFT()

        if os.path.isfile(self.img_path + '.sift'):
            try:
                with open(self.img_path + '.sift', 'rb') as f:
                    keypoints, descriptors = unpickle_keypoints( cPickle.load(f) )
            except cPickle.UnpicklingError as ue:
                print 'Unpickling error, recreating sift pickle : ' + str(ue)
                keypoints, descriptors = self.create_sift(detector, create_file)
        else:
            keypoints, descriptors = self.create_sift(detector, create_file)

        return keypoints, descriptors

    def create_sift(self, detector, create_file):
        img = cv2.imread(self.img_path)
        img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
        keypoints, descriptors = detector.detectAndCompute(img_gray, None)
        key_desc_temp = pickle_keypoints(keypoints, descriptors)
        if create_file:
            with open(self.img_path + '.sift', 'wb') as f:
                cPickle.dump(key_desc_temp, f, protocol=cPickle.HIGHEST_PROTOCOL)
        return keypoints, descriptors

    def add_distance(self, image_ref, weighting):
        self.weights[image_ref] = weighting

    def get_sorted_weights(self):
        return sorted(self.weights, key=self.weights.get, reverse=True)

    def get_image_signature(self):
        sig = ''
        for img_idx in list(self.get_sorted_weights()):
            sig += str(img_idx)
        return sig

    def get_weighted_signature(self):
        sig = ''
        weighted_list = self.get_sorted_weights()

        for img_idx in weighted_list:
            sig += str(str(img_idx) * self.weights[img_idx])
        return sig


class ImageDescriptorManager():
    def __init__(self, match_threshold=1.5, detector=None):
        self.detector = detector
        self.match_threshold = match_threshold
        self.image_descriptors = {}

    def add_descriptor(self, descriptor, add_to_set=True):
        print '\nAdding descriptor ' + str(descriptor.img_idx) + ' ' + descriptor.img_path

        for img_idx in self.image_descriptors:
            print str(img_idx) + ' ',

            img_desc = self.image_descriptors[img_idx]

            sift_key_a, sift_desc_a = descriptor.get_sift(detector=self.detector)
            sift_key_b, sift_desc_b = img_desc.get_sift(detector=self.detector)
            weight = find_matches(
                '',
                sift_desc_a,
                sift_desc_b,
                self.match_threshold
            )
            descriptor.add_distance(img_desc.img_idx, weight)
            if add_to_set:
                img_desc.add_distance(descriptor.img_idx, weight)

        if add_to_set:
            self.image_descriptors[descriptor.img_idx] = descriptor

    def get_all_image_signatures(self, weighted=False):
        img_sigs = dict()
        for img_desc_idx in self.image_descriptors:
            img_desc = self.image_descriptors[img_desc_idx]
            if weighted:
                img_sigs[img_desc_idx] = img_desc.get_weighted_signature()
            else:
                img_sigs[img_desc_idx] = img_desc.get_image_signature()
        return img_sigs

    def quick_init(self, img_descriptor):
        self.add_descriptor(img_descriptor, add_to_set=False)


def iterall(files_list, match_thresh=1.5):

    timekeeper = TimeKeeper()
    timekeeper.time_now('start', True)

    detector = cv2.SIFT()
    all_descriptors = {}
    descriptor_distances = {}
    desc_strings = {}
    weighted_strings = {}

    desc_man = ImageDescriptorManager(match_threshold=match_thresh, detector=detector)

    wrote_sift = 0
    for img_idx in files_list:
        img_path = files_list[img_idx]
        # print str(img_idx) + ' : ' + img_path

        if os.path.isfile(img_path + '.sift'):
            print 'Found sift file : ' + img_path + '.sift'
            # print '.',
            # with open(img_path + '.sift', 'rb') as f:
            #     keypoints, descriptors = unpickle_keypoints( cPickle.load(f) )
        else:
            print 'Creating sift : ' + img_path + '.sift'
            img = cv2.imread(img_path)
            img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
            keypoints, descriptors = detector.detectAndCompute(img_gray, None)

            key_desc_temp = pickle_keypoints(keypoints, descriptors)

            with open(img_path + '.sift', 'wb') as f:
                cPickle.dump(key_desc_temp, f, protocol=cPickle.HIGHEST_PROTOCOL)
            del keypoints
            del descriptors
            wrote_sift += 1
                # all_descriptors[idx] = descriptors
    print 'Had to create ' + str(wrote_sift) + ' .sift files.'

    timekeeper.time_now('After check SIFT')

    for filea in files_list:
        img_desc = ImageDescriptor(filea, files_list[filea])
        desc_man.add_descriptor(img_desc)

    time_delta = timekeeper.time_now('After create ImageDescriptors', True)
    print '\nAvg ' + str(float(time_delta) / len(files_list)) + ' secs per img load'

    for man_img_idx in desc_man.image_descriptors:
        man_img = desc_man.image_descriptors[man_img_idx]
        print '***\n'
        print 'img sig : ' + man_img.get_image_signature()
        print man_img.get_weighted_signature()
        print 'Image ' + man_img.img_path + ' is most similar to ' + files_list[list(man_img.get_sorted_weights())[0]]
        for i in files_list:
            if files_list[i] == man_img.img_path:
                print str(man_img.img_path) + ' : ' + str(i)

        for j in files_list:
            if files_list[j] == files_list[list(man_img.get_sorted_weights())[0]]:
                print 'Similar to image : ' + str(j)

        print '\n'

    print timekeeper.time_now('After similarities', True)



    # for file_a in files_list:
    #     print '\nComparing file ' + str(file_a) + ' to : '
    #
    #     descriptor_orders = {}
    #     weighted_orders = {}
    #     with open(files_list[file_a] + '.sift', 'rb') as fa:
    #         keypoints_a, descriptors_a = unpickle_keypoints( cPickle.load(fa) )
    #
    #     for file_b in files_list:
    #         print file_b,
    #         if file_a != file_b:
    #             with open(files_list[file_b] + '.sift', 'rb') as fb:
    #                 keypoints_b, descriptors_b = unpickle_keypoints( cPickle.load(fb) )
    #
    #             matches_size = find_matches(str(file_a) + ',' + str(file_b),
    #                                         descriptors_a,
    #                                         descriptors_b,
    #                                         match_thresh)
    #             descriptor_orders[str(file_b)] = matches_size
    #
    #             weighted_orders[str(file_b)] = (str(file_b) + '=' + str(matches_size)) + ':'
    #             # weighted_orders[str(file_b)] = (str(file_b) * matches_size)
    #
    #             descriptor_distances[str(file_a) + ':' + str(file_b)] = matches_size
    #
    #     print '\nImage ' + files_list[file_a] + ' is most similar to ' \
    #           + files_list[int(list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True))[0])] + '\n'
    #
    #     desc_arr = list(sorted(descriptor_orders, key=descriptor_orders.get, reverse=True))
    #
    #     item_string = ''
    #     for item in desc_arr:
    #         item_string += str(weighted_orders[item])
    #     weighted_strings[file_a] = item_string

        # desc_strings[file_a] = ' '.join(desc_arr)
        # print 'Array of img_idx for file ' + str(file_a) + ', closest match first : \n' + desc_strings[file_a]

    # print '\n****\nArray of distances between images : \n' + str(descriptor_distances)




    # for ws in weighted_strings:
    #     print str(ws) + ' : ' + weighted_strings[ws]

    # print '\n****\nAll images description strings : \n' + str(desc_strings)
    # for s in desc_strings:
    #     for st in desc_strings:
    #         dist = nltk.metrics.edit_distance(
    #             desc_strings[s],
    #             desc_strings[st])
    #         if (len(files_list) * 0.3) < dist < (len(files_list) * 0.8):
    #             print '\n****\nClosest image pair signatures within 0.8 of each other:'
    #             print str(s) + ' : ' + desc_strings[s]
    #             print str(st) + ' : ' + desc_strings[st]
    #             print 'Deviation of sigs (lower is better) : ' + str(dist)
    #             print files_list[s]
    #             print files_list[st]
    #             print '\n'

    print '\n****\nAll images description strings : \n' + str(desc_strings)
    sigs = desc_man.get_all_image_signatures()
    for s in sigs:
        for st in sigs:
            dist = nltk.metrics.edit_distance(
                sigs[s],
                sigs[st])
            print sigs[s] + '\n' + sigs[st] + '\n' + str(dist)
            if (len(files_list) * 0.3) < dist < (len(files_list) * 0.8):
                print '\n****\nClosest image pair signatures within 0.8 of each other:'
                print str(s) + ' : ' + sigs[s]
                print str(st) + ' : ' + sigs[st]
                print 'Deviation of sigs (lower is better) : ' + str(dist)
                print files_list[s]
                print files_list[st]
                print '\n'

    print timekeeper.time_now('After description strings', True)

    new_desc = ImageDescriptor(len(files_list), './portrait/11040852736_83cc5c2155_z.jpg')
    desc_man.quick_init(new_desc)
    print '\n' + new_desc.get_image_signature()
    print new_desc.get_weighted_signature()
    timekeeper.time_now('Finish', True)

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

def walk_folder(folder, all_files):
    for a_file in os.listdir(folder):
        # print a_file
        fileName, fileExtension = os.path.splitext(a_file)

        if os.path.isfile(os.path.join(folder, a_file)) and '.sift' not in fileExtension:
            all_files.append(os.path.join(folder, a_file))

        if os.path.isdir(os.path.join(folder, a_file)):
            all_files = walk_folder(os.path.join(folder, a_file), all_files)
    return all_files


def find_files(folders):
    all_files = []
    for folder in folders:
        # print folder
        count = 0
        for a_file in os.listdir(folder):
            if count < 10:
                count += 1
                # print a_file
                fileName, fileExtension = os.path.splitext(a_file)

                if os.path.isfile(os.path.join(folder, a_file)) and '.sift' not in fileExtension:
                    all_files.append(os.path.join(folder, a_file))
        all_files = walk_folder(folder, all_files)

    print 'Found ' + str(len(all_files)) + ' files'
    files_dict = {}
    for f in all_files[:100]:
        files_dict[int(len(files_dict))] = f

    print str(files_dict) + '\n\n****\n'
    print 'Loading ' + str(len(files_dict)) + ' files.'
    return files_dict


to_match = find_files(['./learn-all'])

iterall(to_match, 1.5)