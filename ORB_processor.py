__author__ = 'ubuntu'

from DescriptorBase import DescriptorBase, DescriptorCreationResponse
import os
import cPickle
import sys

try:
    from local_settings import *
except ImportError as ie:
    print ie

sys.path.append(OPENCV_LOCATION)
import cv2
import numpy as np


class ORB_processor(DescriptorBase):
    def __init__(self):
        DescriptorBase.__init__(self)
        self.name = 'ORB descriptor processor'

    # Check for SIFT file and create if not there
    # Return True if had to write file, False if already exists
    def touch_descriptor(self, img_path, detector_ext=None, output_path=None):

        print '\n*********' + detector_ext

        detector = cv2.ORB()

        descriptor_path = img_path + detector_ext
        if output_path is not None:
            descriptor_path = os.path.join(output_path, 'desc' + detector_ext)

        if os.path.isfile(descriptor_path):
            print 'Found descriptor file : ' + descriptor_path
            return DescriptorCreationResponse(descriptor_path, had_to_create=False)
        else:
            try:
                print 'Creating descriptor : ' + descriptor_path
                img = cv2.imread(img_path)
                img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
                del img

                keypoints, descriptors = detector.detectAndCompute(img_gray, None)
                del img_gray

                key_desc_temp = self.pickle_keypoints(keypoints, descriptors)
                with open(descriptor_path, 'wb') as f:
                    cPickle.dump(key_desc_temp, f, protocol=cPickle.HIGHEST_PROTOCOL)
                f.close()
                del f

                del keypoints
                del descriptors

                return DescriptorCreationResponse(descriptor_path, had_to_create=True)
            except cv2.error as ome:
                print ome
                dcr = DescriptorCreationResponse('', False)
                dcr.error = ome
                return dcr

    def pickle_keypoints(self, keypoints, descriptors):
        i = 0
        temp_array = []
        for point in keypoints:
            temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
            i += 1
            temp_array.append(temp)
        return temp_array

    def compare_descriptors(self, d1, d2, thresh):
        if os.path.isfile(d1) and os.path.isfile(d1):
            with open(d1, 'rb') as f1:
                keypoints1, descriptors1 = self.unpickle_keypoints( cPickle.load(f1) )
            with open(d2, 'rb') as f2:
                keypoints2, descriptors2 = self.unpickle_keypoints( cPickle.load(f2) )
            return self.find_ORB_matches(descriptors1, descriptors2, thresh)

        else:
            return 0

    def unpickle_keypoints(self, array):
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

    def find_ORB_matches(self, des1, des2, match_thresh):
            # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1, des2)

        # Sort them in the order of their distance.
        matches = sorted(matches, key = lambda x:x.distance)
        return len(matches)