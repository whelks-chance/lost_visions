import pprint
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

__author__ = 'ubuntu'


class LBP_Processor(DescriptorBase):
    def __init__(self):
        DescriptorBase.__init__(self)
        self.name = 'Local Binary Pattern descriptor processor'
        self.settings = {
            'metrics': [
                ['CV_COMP_BHATTACHARYYA', 3],
                ['CV_COMP_CHISQR', 1],
                ['CV_COMP_CORREL', 0],
                ['CV_COMP_INTERSECT', 2]
            ]
        }

    # Return True if had to write file, False if already exists
    def touch_descriptor(self, img_path, detector_ext=None, output_path=None):

        print '\n*********' + detector_ext
        print output_path

        if output_path is not None:
            descriptor_path = os.path.join(output_path, 'desc' + detector_ext)
        else:
            descriptor_path = img_path + detector_ext

        if os.path.isfile(descriptor_path):
            print 'Found descriptor file : ' + descriptor_path
            return DescriptorCreationResponse(descriptor_path, had_to_create=False)
        else:
            try:
                print 'Creating descriptor : ' + descriptor_path
                img = cv2.imread(img_path, 0)
                transformed_img = cv2.imread(img_path, 0)

                lbp_img = self.calculate_lbp(img, transformed_img)

                with open(descriptor_path, 'wb') as f:
                    cPickle.dump(lbp_img, f, protocol=cPickle.HIGHEST_PROTOCOL)
                f.close()
                del f

                return DescriptorCreationResponse(descriptor_path, had_to_create=True)
            except cv2.error as ome:
                print ome
                dcr = DescriptorCreationResponse('', False)
                dcr.error = ome
                return dcr

    def compare_descriptors(self, d1, d2, thresh):
        if os.path.isfile(d1) and os.path.isfile(d1):
            with open(d1, 'rb') as f1:
                lbp_img1 = cPickle.load(f1)
                hist1 = cv2.calcHist([lbp_img1.flatten()], [0], None, [256], [0, 256])

            with open(d2, 'rb') as f2:
                lbp_img2 = cPickle.load(f2)
                hist2 = cv2.calcHist([lbp_img2.flatten()], [0], None, [256], [0, 256])

            return_matches = []
            for metric in self.settings['metrics']:
                return_matches.append(
                    {
                        'metric_name': metric[0],
                        'metric_value': cv2.compareHist(hist1, hist2, metric[1])
                    }
                )
            print pprint.pformat(return_matches)
            return return_matches
            # return cv2.compareHist(hist1, hist2, 0)

        else:
            return 0

    # def pickle_keypoints(self, keypoints, descriptors):
    #     i = 0
    #     temp_array = []
    #     for point in keypoints:
    #         temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
    #         i += 1
    #         temp_array.append(temp)
    #     return temp_array
    #
    # def unpickle_keypoints(self, array):
    #     keypoints = []
    #     descriptors = []
    #     for point in array:
    #         temp_feature = cv2.KeyPoint(
    #             x=point[0][0],
    #             y=point[0][1],
    #             _size=point[1],
    #             _angle=point[2],
    #             _response=point[3],
    #             _octave=point[4],
    #             _class_id=point[5]
    #         )
    #
    #         temp_descriptor = point[6]
    #         keypoints.append(temp_feature)
    #         descriptors.append(temp_descriptor)
    #     return keypoints, np.array(descriptors)

    def thresholded(self, center, pixels):
        out = []
        for a in pixels:
            if a >= center:
                out.append(1)
            else:
                out.append(0)
        return out

    def get_pixel_else_0(self, l, idx, idy, default=0):
        try:
            return l[idx,idy]
        except IndexError:
            return default

    def calculate_lbp(self, img, transformed_img):

        for x in range(0, len(img)):
            for y in range(0, len(img[0])):
                center        = img[x,y]
                top_left      = self.get_pixel_else_0(img, x-1, y-1)
                top_up        = self.get_pixel_else_0(img, x, y-1)
                top_right     = self.get_pixel_else_0(img, x+1, y-1)
                right         = self.get_pixel_else_0(img, x+1, y )
                left          = self.get_pixel_else_0(img, x-1, y )
                bottom_left   = self.get_pixel_else_0(img, x-1, y+1)
                bottom_right  = self.get_pixel_else_0(img, x+1, y+1)
                bottom_down   = self.get_pixel_else_0(img, x,   y+1 )

                values = self.thresholded(center, [top_left, top_up, top_right, right, bottom_right,
                                                   bottom_down, bottom_left, left])

                weights = [1, 2, 4, 8, 16, 32, 64, 128]
                res = 0
                for a in range(0, len(values)):
                    res += weights[a] * values[a]

                transformed_img.itemset((x,y), res)

        return transformed_img
        # print x

    def np_hist_to_cv(self, np_histogram_output):
        counts, bin_edges = np_histogram_output
        return counts.ravel().astype('float32')
