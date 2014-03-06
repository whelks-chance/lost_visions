import numpy
import os
import cv2
from opencv_utils import surf_detect_and_compute_from_folder

__author__ = 'ubuntu'




# introduce new values
def is_image_a_map(filename):
    image = cv2.imread(filename)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    new_keypoints, new_descriptor = detector.detectAndCompute(grey,None)
    newcomer = numpy.array(new_descriptor).astype(numpy.float32)
    ret, results, neighbours ,dist = knn.find_nearest(newcomer, 3)

    positive_match = 0
    for result in results:
        if result[0] == 1.0:
            positive_match += 1
    print 'score : ' + str(positive_match) + ' / ' + str(len(results))
    return float(positive_match) / float(len(results))


hessian_threshold = 1000
detector = cv2.SURF(hessian_threshold)

# get descriptors for 2 sets of images, Maps and non-maps

#maps

# map_array = []
# for file in os.listdir('./maps_small'):
#     print file
#     image = cv2.imread('./maps_small/' + file)
#     grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # build feature detector and descriptor extractor
#     map_keypoints, map_descriptors = detector.detectAndCompute(grey,None)
#
#     for desc in map_descriptors:
#         map_array.append(desc)

map_array = surf_detect_and_compute_from_folder('./maps_small')

# print map_array
map_samples = numpy.array(map_array).astype(numpy.float32)
# samples = numpy.array([[1,1],[2,2]]).astype(numpy.float32)
# print map_samples


# non-maps

# non_map_array = []
# for file in os.listdir('./not_maps'):
#     print file
#     image = cv2.imread('./not_maps/' + file)
#     grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # build feature detector and descriptor extractor
#     non_map_keypoints, non_map_descriptors = detector.detectAndCompute(grey,None)
#
#     for nm_desc in non_map_descriptors:
#         non_map_array.append(nm_desc)

non_map_array = surf_detect_and_compute_from_folder('./not_maps')

non_map_samples = numpy.array(non_map_array).astype(numpy.float32)
# samples = numpy.array([[1,1],[2,2]]).astype(numpy.float32)
# print non_map_samples

all_samples = []
all_responses = []
for description in map_array:
    all_samples.append(description)
    all_responses.append(1)

for description in non_map_array:
    all_samples.append(description)
    all_responses.append(0)

samples = numpy.array(all_samples).astype(numpy.float32)
# print samples

responses = numpy.array(all_responses).astype(numpy.float32)
# print responses


# train system with sets of descriptors and map/non-map value

knn = cv2.KNearest()
knn.train(samples,responses)


val = is_image_a_map('./to_test/not_a_map.jpg')
print val
print 'This image is a map : ' + str(val > 0.65)

print 'animal scores'
non_match = 0
total = 0
for file in os.listdir('./animals'):
    val = is_image_a_map('./animals/' + file)
    print val
    if val < 0.65:
        non_match +=1
    total +=1
    print '\n'

print 'animals correctly found to be not maps : ' + str(non_match) + ' out of ' + str(total)

print 'map scores'
m_match = 0
m_total = 0
for file in os.listdir('./map'):
    val = is_image_a_map('./map/' + file)
    print val
    if val > 0.65:
        m_match +=1
    m_total +=1
    print '\n'

print 'maps correctly found to be maps : ' + str(m_match) + ' out of ' + str(m_total)


# print "result: ", results,"\n"
# print "neighbours: ", neighbours,"\n"
# print "distance: ", dist