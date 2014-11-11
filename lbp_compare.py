
# Messed about with by Ian Harvey, from original code found here:
# https://github.com/lionaneesh/LBP-opencv-python/blob/master/Basic-3x3-LBP.py

import pprint
import sys
import math
import itertools
from TimeKeeper import TimeKeeper

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


def np_hist_to_cv(np_histogram_output):
    counts, bin_edges = np_histogram_output
    return counts.ravel().astype('float32')

tk = TimeKeeper()
tk.time_now('start')

filename = 'animals/11175682543_4db70a7f6f_z.jpg'

img = cv2.imread(filename, 0)
transformed_img = cv2.imread(filename, 0)

tk.time_now('read img')

transformed_img = calculate_lbp(img, transformed_img)

tk.time_now('lpb')

# cv2.imshow('image', img)
# cv2.imshow('thresholded image', transformed_img)

hist, bins = np.histogram(transformed_img.flatten(), 256, [0, 256])

tk.time_now('np hist')

hist1 = np_hist_to_cv((hist, bins))

tk.time_now('np to cv')

hist2 = cv2.calcHist([transformed_img.flatten()], [0], None, [256], [0, 256])

tk.time_now('cv hist')

val = cv2.compareHist(hist1, hist2, 1)

tk.time_now('cmp chi sqr')

print ('Comp method {} gives value : {}'.format('chi-sqr', val))

cv2.imshow('thresholded image', transformed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

