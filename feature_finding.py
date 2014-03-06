__author__ = 'ubuntu'


import cv2
import numpy as np

filename = './image_cropped.jpg'
img = cv2.imread(filename)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]


# Adds "good features to track" dots
corners = cv2.goodFeaturesToTrack(gray,250,0.01,10)
corners = np.int32(corners)
for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,128,-1)


#SIFT
#needed to change the depth of the grayscale image
height, width = gray.shape
blank_image = np.zeros((height, width, 3), np.uint8)
gray = cv2.convertScaleAbs(gray, blank_image, 1.0, 0.0)


img2 = cv2.imread(filename)


# then we try sift
sift = cv2.SIFT()
sift_key_points, sift_descriptors = sift.detectAndCompute(img2, None)
sift_img=cv2.drawKeypoints(img2, sift_key_points, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


#SURF
surf = cv2.SURF(hessianThreshold=1000)
surf_key_points, surf_descriptors = surf.detectAndCompute(img2, None)
surf_img = cv2.drawKeypoints(img2, surf_key_points, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


#FastFeatureDetector
fast = cv2.FastFeatureDetector()
# fast.setBool('nonmaxSuppression',0)
# cv2.FAST_FEATURE_DETECTOR_TYPE_9_16
fast_key_points = fast.detect(img2, None)
fast_img = cv2.drawKeypoints(img2, fast_key_points, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# Print all default params
print "Threshold: ", fast.getInt('threshold')
print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
# print "neighborhood: ", fast.getInt('type')
print "Total Keypoints with nonmaxSuppression: ", len(fast_key_points)



# Initiate STAR detector
star = cv2.FeatureDetector_create("STAR")
# Initiate BRIEF extractor
brief = cv2.DescriptorExtractor_create("BRIEF")
# find the keypoints with STAR
brief_keypoints = star.detect(img2,None)
# compute the descriptors with BRIEF
kp, des = brief.compute(img2, brief_keypoints)
brief_img = cv2.drawKeypoints(img2, brief_keypoints, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



# Initiate STAR detector
orb = cv2.ORB()
# find the keypoints with ORB
orb_keypoints = orb.detect(img2,None)
# compute the descriptors with ORB
orb_keypoints, orb_descriptors = orb.compute(img2, orb_keypoints)
# draw only keypoints location,not size and orientation
orb_image = cv2.drawKeypoints(img2, orb_keypoints, color=(0,255,0), flags=0)





# show stuff
cv2.imshow('sift', sift_img)

cv2.imshow('surf', surf_img)

cv2.imshow('fast', fast_img)

cv2.imshow('brief', brief_img)

cv2.imshow('orb', orb_image)


cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()