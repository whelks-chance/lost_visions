from dateutil.tz import tzlocal
import itertools
import json
import datetime
import pprint
import numpy as np

__author__ = 'ubuntu'

class PictureDetails():
    def __init__(self, name, features):
        self.features = features
        self.name = name
        self.url = ''


def find_dists(arr):
    timestamp = datetime.datetime.now(tzlocal()).strftime('%Y-%m-%dT%H:%M:%S.%f')

    combs = itertools.combinations(arr, 2)

    # print len(list(combs))
    dists = []
    closests = []

    for pair in combs:

        dist = np.linalg.norm(np.array(pair[0].features) - np.array(pair[1].features))

        dists.append(
            {
                'a': pair[0].name,
                'a-url': pair[0].url,
                'b': pair[1].name,
                'b-url': pair[1].url,
                'dist': dist
            }
        )

        closests = update_closests(closests, pair, dist)

        # fake_a = PictureDetails(pair[1].name, [])
        # fake_a.url = pair[1].url
        # fake_b = PictureDetails(pair[0].name, [])
        # fake_b.url = pair[0].url
        closests = update_closests(closests, (pair[1], pair[0]), dist)

    print pprint.pformat(closests)

    with open('./bly-data/results/dists-' + timestamp + '.json', 'w') as f1:
        json.dump(dists, f1, indent=4)
        # f.write(json.dumps(pair, indent=4))
        # print pprint.pformat(dists)

    sorted_dists = sorted(dists, key=lambda image: image['dist'])

    with open('./bly-data/results/dists_sorted-' + timestamp + '.json', 'w') as f2:
        json.dump(sorted_dists, f2, indent=4)

    return dists, closests


def update_closests(closests, pair, dist):
    try:
        a_closest = (item for item in closests if item["a"] == pair[0].name).next()
    except StopIteration:
        a_closest = dict({
            'a': pair[0].name,
            'a-url': pair[0].url,
            'close': [],
            'dist': 100,
            'b': pair[1].name,
            'b-url': pair[1].url
        })

    found_dist = a_closest['dist']

    if len(a_closest['close']) < 3:
        try:
            index = closests.index(a_closest)
        except ValueError:
            index = -1

        close_entry = {'dist': dist,
                       'b': pair[1].name,
                       'b-url': pair[1].url
        }

        a_closest['close'].append(close_entry)

        if index == -1:
            closests.append(a_closest)
        else:
            closests[index] = a_closest

        if dist < found_dist:
            try:
                index = closests.index(a_closest)
            except ValueError:
                index = -1

            a_closest['dist'] = dist
            a_closest['b'] = pair[1].name
            a_closest['b-url'] = pair[1].url

            if index == -1:
                closests.append(a_closest)
            else:
                closests[index] = a_closest

    else:
        try:
            index = closests.index(a_closest)
        except ValueError:
            index = -1

        close_entry = {'dist': dist,
                       'b': pair[1].name,
                       'b-url': pair[1].url
        }

        # a_closest['close'].append(close_entry)

        found = False
        for item_closest in sorted(a_closest['close'], key=lambda image: image['dist']):
            if found:
                break

            if item_closest['dist'] > dist:
                try:
                    index = a_closest['close'].index(item_closest)

                    a_closest['close'][index] = close_entry
                    found = True

                except ValueError:
                    pass

        if index == -1:
            closests.append(a_closest)
        else:
            closests[index] = a_closest

        if dist < found_dist:
            try:
                index = closests.index(a_closest)
            except ValueError:
                index = -1

            a_closest['dist'] = dist
            a_closest['b'] = pair[1].name
            a_closest['b-url'] = pair[1].url


            if index == -1:
                closests.append(a_closest)
            else:
                closests[index] = a_closest


    return closests

# arr = []
#
# for a in range(0, 200):
#     rnd_data = np.random.randint(1000, size=127)
#     arr.append(PictureDetails(str(a), rnd_data))
#
# find_dists(arr)

# a = (1, 2, 3, 4, 5, 6, 7, 8, 9)
# b = (10, 20, 30, 40, 50, 60, 70, 80, 90)
# c = (100, 200, 300, 400, 500, 600, 700, 800, 900)


# arr = [
#     PictureDetails('a', a),
#     PictureDetails('b', b),
#     PictureDetails('c', c),
#     ]

