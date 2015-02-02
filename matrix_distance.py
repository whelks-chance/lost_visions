import itertools
import json
import pprint
import numpy as np

__author__ = 'ubuntu'

class PictureDetails():
    def __init__(self, name, features):
        self.features = features
        self.name = name

arr = []

for a in range(0, 2000):
    rnd_data = np.random.randint(1000, size=127)
    arr.append(PictureDetails(str(a), rnd_data))


# a = (1, 2, 3, 4, 5, 6, 7, 8, 9)
# b = (10, 20, 30, 40, 50, 60, 70, 80, 90)
# c = (100, 200, 300, 400, 500, 600, 700, 800, 900)


# arr = [
#     PictureDetails('a', a),
#     PictureDetails('b', b),
#     PictureDetails('c', c),
#     ]

combs = itertools.combinations(arr, 2)

dists = []

for pair in combs:

    dist = np.linalg.norm(np.array(pair[0].features) - np.array(pair[1].features))

    dists.append(
        {
            'a': pair[0].name,
            'b': pair[1].name,
            'dst': dist
        }
    )

with open('dists.json', 'w') as f:
    json.dump(dists, f, indent=4)
        # f.write(json.dumps(pair, indent=4))
    # print pprint.pformat(dists)