
# Messed about with by Ian Harvey, from original code found here:
# https://github.com/lionaneesh/LBP-opencv-python/blob/master/Basic-3x3-LBP.py

import pprint
import sys
import math
import itertools

try:
    from local_settings import *
except ImportError as ie:
    print ie

sys.path.append(OPENCV_LOCATION)

import numpy as np
import cv2

import matplotlib
matplotlib.use('qt4agg')
from matplotlib import pyplot as plt

def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out

def get_pixel_else_0(l, idx, idy, default=0):
    try:
        return l[idx,idy]
    except IndexError:
        return default

def calculate_lbp(img, transformed_img):

    for x in range(0, len(img)):
        for y in range(0, len(img[0])):
            center        = img[x,y]
            top_left      = get_pixel_else_0(img, x-1, y-1)
            top_up        = get_pixel_else_0(img, x, y-1)
            top_right     = get_pixel_else_0(img, x+1, y-1)
            right         = get_pixel_else_0(img, x+1, y )
            left          = get_pixel_else_0(img, x-1, y )
            bottom_left   = get_pixel_else_0(img, x-1, y+1)
            bottom_right  = get_pixel_else_0(img, x+1, y+1)
            bottom_down   = get_pixel_else_0(img, x,   y+1 )

            values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,
                                          bottom_down, bottom_left, left])

            weights = [1, 2, 4, 8, 16, 32, 64, 128]
            res = 0
            for a in range(0, len(values)):
                res += weights[a] * values[a]

            transformed_img.itemset((x,y), res)

    return transformed_img
    # print x


def create_hist(filename):
    img = cv2.imread(filename, 0)
    transformed_img = cv2.imread(filename, 0)

    transformed_img = calculate_lbp(img, transformed_img)

    # cv2.imshow('image', img)
    # cv2.imshow('thresholded image', transformed_img)

    hist, bins = np.histogram(img.flatten(),256,[0,256])

    return [hist, bins, img, transformed_img]


image_files = [
    'maid.jpg',
    'maid (copy).jpg',
    'image_cropped.jpg',
    'animals/11175682543_4db70a7f6f_z.jpg'
]
image_hists = {}

for filename in image_files:
    image_hists[filename] = create_hist(filename)


print pprint.pformat(image_hists)


for filename in image_hists:

    hist = image_hists[filename][0]
    transformed_img = image_hists[filename][3]

    # cv2.imshow('image', image_hists[filename][2])
    # cv2.imshow('thresholded image', transformed_img)

    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()

    # plt.plot(cdf_normalized, color='b')
    #
    # # TODO sort out this 256 or 254 issue
    # plt.hist(transformed_img.flatten(), 256, [1, 254], color='r')
    # plt.xlim([0, 256])
    #
    # plt.legend(('cdf', 'histogram'), loc='upper left')
    # plt.show()

for pair in itertools.combinations(image_hists, 2):
    print pair

    # cv2.cv.CV_COMP_CHISQR
    comp_methods = [
        ['CV_COMP_BHATTACHARYYA', 3],
        ['CV_COMP_CHISQR', 1],
        ['CV_COMP_CORREL', 0],
        ['CV_COMP_INTERSECT', 2]
    ]
    for method in comp_methods:
        img1 = image_hists[pair[0]][3]
        img2 = image_hists[pair[1]][3]

        hist1 = cv2.calcHist([img1.flatten()], [0], None, [256], [0, 256])

        # print hist1

        hist2 = cv2.calcHist([img2.flatten()], [0], None, [256], [0, 256])

        # print hist2

        val = cv2.compareHist(hist1, hist2, method[1])

        print ('Comp method {} gives value : {}'.format(method[0], val))
    print '\n'

cv2.waitKey(0)
cv2.destroyAllWindows()