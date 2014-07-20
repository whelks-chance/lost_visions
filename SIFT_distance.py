import cv2
import numpy as np

__author__ = 'ubuntu'


def start():
    img_a = cv2.imread('./maps_small/af.jpg')

    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)

    detector = cv2.SIFT()
    keypoints_a, descriptors_a = detector.detectAndCompute(img_a, None)




    img_b = cv2.imread('./maps_small/sa.jpg')

    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)

    detector = cv2.SIFT()
    keypoints_b, descriptors_b = detector.detectAndCompute(img_b, None)

    print len(find_matches(descriptors_a, descriptors_b, 1.5))



    img_c = cv2.imread('./maps_small/uk.jpg')

    img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)

    detector = cv2.SIFT()
    keypoints_c, descriptors_c = detector.detectAndCompute(img_c, None)

    print len(find_matches(descriptors_a, descriptors_c, 1.5))


def find_matches(template_descriptors, current_img_descriptors, match_thresh):

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(current_img_descriptors, flann_params)
    idx, dist = flann.knnSearch(template_descriptors, 2, params={})
    del flann
    matches = np.c_[np.arange(len(idx)), idx[:,0]]
    pass_filter = dist[:,0]*match_thresh < dist[:,1]
    matches = matches[pass_filter]

    return matches


start()