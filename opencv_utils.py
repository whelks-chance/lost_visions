import os
import cv2
import numpy as np

__author__ = 'ubuntu'


def surf_detect_and_compute_from_folder(folder):
    hessian_threshold = 1000
    detector = cv2.SURF(hessian_threshold)
    descriptors_array = []
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        image = cv2.imread(filepath)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = detector.detectAndCompute(grey,None)
        for nm_desc in descriptors:
            descriptors_array.append(nm_desc)
    return np.array(descriptors_array).astype(np.float32)


