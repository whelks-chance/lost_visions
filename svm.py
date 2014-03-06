import os
import cv2
import numpy as np
from opencv_utils import surf_detect_and_compute_from_folder

SZ=20
bin_n = 16 # Number of bins

svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_C_SVC,
                    C=2.67, gamma=5.383 )

affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv2.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
    return img


def hog(img):
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantizing binvalues in (0...16)
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist is a 64 bit vector
    return hist

def images_from_folder(folder):
    train_cells = []
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        image = cv2.imread(filepath)
        train_cells.append(image)
    return train_cells

# img = cv2.imread('digits.png',0)
#
# cells = [np.hsplit(row,100) for row in np.vsplit(img,50)]
#
# # First half is trainData, remaining is testData
# train_cells = [ i[:50] for i in cells ]
# test_cells = [ i[50:] for i in cells]

def func(a):
    print a
    return a * 2

a = [1,2,3,4]
c = map(func, a)

print 'c = ' + str(c)
b = np.arange(2)
print 'b = ' + str(b)
d = np.repeat(b, 4)
print 'd = ' + str(d)

train_cells1 = np.array(images_from_folder('./maps_small'))
train_cells2 = np.array(images_from_folder('./not_maps'))

test_cells = np.array(images_from_folder('./to_test'))

######     Now training      ########################

deskewed1 = [map(deskew, row1a) for row1a in train_cells1]
hogdata1 = [map(hog, row1b) for row1b in deskewed1]
print '\nallhog1 ' + str(len(hogdata1))
for object1 in hogdata1:
    print '\nobject in hog1 ' + str(len(object1))
    # for o1 in object1:
        # print 'object in object in hog1 ' + str(len(o1))
trainData1 = np.float32(hogdata1).reshape(-1,64)

deskewed2 = [map(deskew, row2a) for row2a in train_cells2]
hogdata2 = [map(hog, row2b) for row2b in deskewed2]
# print hogdata2
print '\nallhog2 ' + str(len(hogdata2))
for object2 in hogdata2:
    print '\nobject in hog2 ' + str(len(object2))
    # for o2 in object2:
        # print 'object in object in hog2 ' + str(len(o2))
trainData2 = np.float32(hogdata2).reshape(-1,64)

trainData = []
for t1 in trainData1:
    trainData.append(t1)
for t2 in trainData2:
    trainData.append(t2)
trainData = np.array(trainData)

responses1 = np.float32(np.repeat(1, len(trainData1)))
responses2 = np.float32(np.repeat(0, len(trainData2)))

responses = []
for r1 in responses1:
    responses.append(r1)
for r2 in responses2:
    responses.append(r2)đ
responses = np.array(responses)

# responses = np.concatenate(responses1, responses2)
# responses = np.float32(np.repeat(np.arange(10),250)[:,np.newaxis])
# print responses
# print len(responses)

svm = cv2.SVM()
svm.train(trainData,responses, params=svm_params)
svm.save('svm_data.dat')

######     Now testing      ########################

deskewed = [map(deskew,row) for row in test_cells]
hogdata = [map(hog,row) for row in deskewed]
testData = np.float32(hogdata).reshape(-1,bin_n*4)
result = svm.predict_all(testData)

#######   Check Accuracy   ########################
mask = result==responses
correct = np.count_nonzero(mask)
print correct*100.0/result.size