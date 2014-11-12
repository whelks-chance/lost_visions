import math
import pprint

__author__ = 'ubuntu'
#
# # import networkx as NX
# import pygraphviz as PG
#
# G = PG.AGraph()
# # nlist = "A B C D E".split()
# # a, b = "A A B", "B C D"
# # elist = zip(a.split(), b.split())
#
# # G.add_nodes_from(nlist)
# # G.add_nodes_from(elist)
# G.node_attr.update(color="red", style="filled")
# G.edge_attr.update(color="blue", len="2.0", width="2.0")
#
# print(G.edge_attr)
# # returns {'color': 'red', 'width': '', 'len': '2.0'}
#
# # add new edge with custom length (all others have length=2.0):
# G.add_edge("C", "E", len="3.0", color="blue", width="2.0")
#
# edge = G.get_edge("C", "E")
# print(edge.attr)
# # returns {'color': 'blue', 'width': '2.0', 'len': '3.0'}
#
# # and you can confirm that introspection by drawing & printing this graph:
# G.draw('somefilename.png', format='png', prog='neato')


def graph_matches(sorted_weights):

    # print pprint.pformat(sorted_weights)

    import matplotlib
    matplotlib.use('qt4agg')
    from matplotlib import pyplot as plt
    import numpy as np

    ax = plt.gca()

    matches_dict = dict()
    name_set = set()
    for match in sorted_weights:
        a = match['img_a'].split('/')[-1].split('_')[0]
        b = match['img_b'].split('/')[-1].split('_')[0]

        name_set.add(a)
        name_set.add(b)
        matches_dict[(a, b)] = match['weight']

    # print '\n{}\n'.format(pprint.pformat(matches_dict))


    # matrix = np.array(len(name_set), len(name_set))

    name_list = list(name_set)
    print len(name_list)

    matrix = []

    for img1 in name_list:
        line = []
        for img2 in name_list:
            weight = matches_dict.get((img1, img2), None)
            if weight is None:
                weight = matches_dict.get((img2, img1), None)

            if weight is None:
                weight = 0
            else:
                weight -= 0

            print '{} {} : {}'.format(img1, img2, weight)
            line.append(math.sqrt(weight))
            # line.append(weight)

        matrix.append(line)

    matrix = np.array(matrix)

    # matrix = np.random.rand(len(name_set), len(name_set))

    max_weight = 2**np.ceil(np.log(np.abs(matrix).max())/np.log(2))

    ax.patch.set_facecolor('gray')
    ax.set_aspect('equal', 'box')
    # ax.xaxis.set_major_locator(plt.NullLocator())
    # ax.yaxis.set_major_locator(plt.NullLocator())

    for (x, y), w in np.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = np.sqrt(np.abs(w))
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    ax.set_xticklabels(list(name_set), rotation=90)
    ax.set_yticklabels(list(name_set))

    # ax.spines['left'].set_position(('outward', 10))
    # ax.spines['bottom'].set_position(('outward', 10))

    ax.autoscale_view()
    ax.invert_yaxis()
    plt.axis([0, len(name_list), 0, len(name_list)])
    plt.show()


def create_graph(matches):

    nodes = set()
    edges = []

    maximums = dict()

    import pygraphviz as PG

    G = PG.AGraph(splines=True)
    G.node_attr.update(color="red", style="filled")
    G.edge_attr.update(color="blue", len="2.0", width="2.0")

    print(G.edge_attr)

    for match in matches:
        if match['descriptor'] not in maximums:
            maximums[match['descriptor']] = 0
        if match['weight'] > maximums.get(match['descriptor']):
            maximums[match['descriptor']] = match['weight']

    print maximums

    for match in matches:
        length = maximums[match['descriptor']] - match['weight']

        if 'orb' in match['descriptor'] and length < (maximums[match['descriptor']] * 0.4):
            colour = "yellow"
            if 'map' in match['img_a']:
                colour = 'green'
            if 'portrait' in match['img_a']:
                colour = "blue"
            if 'animal' in match['img_a']:
                colour = "red"

            G.add_node(match['img_a'], color=colour)

            colour = "yellow"
            if 'map' in match['img_b']:
                colour = 'green'
            if 'portrait' in match['img_b']:
                colour = "blue"
            if 'animal' in match['img_b']:
                colour = "red"

            G.add_node(match['img_b'], color=colour)


            G.add_edge(match['img_a'], match['img_b'],
                       len=math.sqrt(float(length))*2, color="blue", width="1.0", label=length)


    # G.add_edge("C", "E", len="3.0", color="blue", width="2.0")

    # edge = G.get_edge("C", "E")
    # print(edge.attr)

    G.draw('somefilename.png', format='png', prog='neato')