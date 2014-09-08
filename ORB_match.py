import sys

__author__ = 'ubuntu'


import numpy as np
sys.path.append("/home/ubuntu/opencv-2.4.8/build/lib")

import cv2
import scipy as sp


class ShowStuff():

    def __init__(self):
        pass

    def show_ORB(self, img1, img2):
        img1 = cv2.imread(img1, 0)          # queryImage
        img2 = cv2.imread(img2, 0) # trainImage

        # Initiate SIFT detector
        orb = cv2.ORB()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = orb.detectAndCompute(img1,None)
        kp2, des2 = orb.detectAndCompute(img2,None)
        #
        # print kp1[0].pt
        # print kp1[0].angle
        # print kp1[0].size

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1,des2)

        # Sort them in the order of their distance.
        matches = sorted(matches, key = lambda x:x.distance)

        # Draw first 10 matches.
        # img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], flags=2)
        #
        # plt.imshow(img1), plt.show()
        # plt.imshow(img2), plt.show()



        # #####################################
        # visualization
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
        view[:h1, :w1, 0] = img1
        view[:h2, w1:, 0] = img2
        view[:, :, 1] = view[:, :, 0]
        view[:, :, 2] = view[:, :, 0]

        for m in matches:
            # draw the keypoints
            # print m.queryIdx, m.trainIdx, m.distance
            color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
            cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])) , (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)

        cv2.imshow("view", view)
        cv2.waitKey()

# ShowStuff.show_ORB('./map/11307086946_fe8ed3563a_z.jpg', './map/11236384793_e8093786a2_z.jpg')