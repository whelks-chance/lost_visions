import math

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