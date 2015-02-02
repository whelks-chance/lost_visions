import time
import cPickle

__author__ = 'lostvisions'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline

# Make sure that caffe is on the python path:
caffe_root = '/home/lostvisions/caffe/'  # this file is expected to be in {caffe_root}/examples
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
PRETRAINED = caffe_root + '/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
IMAGE_FILE = '/home/lostvisions/learn_2cat_huge/portrait/11059618046_dd938c21db_z.jpg'
CLASS_LABELS_FILE = '/home/lostvisions/caffe/data/ilsvrc12/synset_words.txt'
BET_FILE = '/home/lostvisions/caffe/data/ilsvrc12/imagenet.bet.pickle'


starttime = time.time()

net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))


with open(CLASS_LABELS_FILE) as f:
    labels_df = pd.DataFrame([
        {
            'synset_id': l.strip().split(' ')[0],
            'name': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
        }
        for l in f.readlines()
    ])
labels = labels_df.sort('synset_id')['name'].values

bet = cPickle.load(open(BET_FILE))
# A bias to prefer children nodes in single-chain paths
# I am setting the value to 0.1 as a quick, simple model.
# We could use better psychological models here...
bet['infogain'] -= np.array(bet['preferences']) * 0.1


net.set_phase_test()
net.set_mode_cpu()

input_image = caffe.io.load_image(IMAGE_FILE)
# plt.imshow(input_image)

# prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
# print 'prediction shape:', prediction[0].shape
# plt.plot(prediction[0])
# print 'predicted class:', prediction[0].argmax()
#
# prediction = net.predict([input_image], oversample=False)
# print 'prediction shape:', prediction[0].shape
# plt.plot(prediction[0])
# print 'predicted class:', prediction[0].argmax()

# Resize the image to the standard (256, 256) and oversample net input sized crops.
# input_oversampled = caffe.io.oversample([caffe.io.resize_image(input_image, net.image_dims)], net.crop_dims)
# 'data' is the input blob name in the model definition, so we preprocess for that input.
# caffe_input = np.asarray([net.preprocess('data', in_) for in_ in input_oversampled])
# forward() takes keyword args for the input blobs with preprocessed input arrays.
# %timeit net.forward(data=caffe_input)


scores = net.predict([input_image], oversample=True).flatten()

indices = (-scores).argsort()[:5]
predictions = labels[indices]

# In addition to the prediction text, we will also produce
# the length for the progress bar visualization.
meta = [
    (p, '%.5f' % scores[i])
    for i, p in zip(indices, predictions)
]
print ('result: %s', str(meta))

# Compute expected information gain
expected_infogain = np.dot(
    bet['probmat'], scores[bet['idmapping']])
expected_infogain *= bet['infogain']

# sort the scores
infogain_sort = expected_infogain.argsort()[::-1]
bet_result = [(bet['words'][v], '%.5f' % expected_infogain[v])
              for v in infogain_sort[:5]]
print('bet result: %s', str(bet_result))

endtime = time.time()

print endtime - starttime