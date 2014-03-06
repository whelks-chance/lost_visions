import numpy
import os
import cv2

__author__ = 'ubuntu'


def images_from_folder(folder):
    train_cells = []
    surf = cv2.SURF(hessianThreshold=1000)

    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        print filepath
        image = cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR)

        surf_key_points, surf_descriptors = surf.detectAndCompute(image, None)


        # image = numpy.asarray(image[:,:])
        # image = numpy.array(image, dtype=numpy.uint32)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # img = cv2.imdecode(numpy.frombuffer(image, numpy.uint8), 1)
        # cv2.imshow('test', image)


        # image = numpy.asarray(image[:,:])
        train_cells.append(surf_descriptors)
    return train_cells


# def surf_image(img):
    #SURF
    # surf_img = cv2.drawKeypoints(img, surf_key_points, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


surf = cv2.SURF(hessianThreshold=1000)

train_imgs1 = numpy.array(images_from_folder('./maps_small'))
train_imgs2 = numpy.array(images_from_folder('./not_maps'))

all_training = []
all_responses = []

for img1 in train_imgs1:
    # surf_key_points, surf_descriptors = surf.detectAndCompute(img1, None)
    # all_training.append(surf_descriptors)
    all_responses.append(1)

for img2 in train_imgs2:
    # surf_key_points, surf_descriptors = surf.detectAndCompute(img2, None)
    # all_training.append(surf_descriptors)
    all_responses.append(0)


# data = [1, 3, 5, 7, 9, 11]

# responses = [0, 0, 0, 1, 1, 1]

train_data = numpy.float32(all_training)

responses_data = numpy.float32(all_responses)

svm = cv2.SVM()

svm.train(train_data, responses_data)

svm.save('svm_save.dat')


filepath = './maid'
test_image = cv2.imread(filepath)
surf_key_points, surf_descriptors = surf.detectAndCompute(test_image, None)

test_data = numpy.float32( surf_descriptors )

# test_responses = numpy.float32( [1] )

result = svm.predict_all(test_data)

print result