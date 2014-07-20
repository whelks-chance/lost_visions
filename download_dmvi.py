import urllib2
from BeautifulSoup import BeautifulSoup

__author__ = 'ubuntu'


def iterate_elements(elm, depth, parent, parent_id, max_id, outputfile=None):
    depth += 1

    for li in elm.findAll('li', recursive=False):
        max_id += 1
        # print li.contents[2].strip()
        route = (str(parent_id) + ">" + str(max_id) + '>' + li.contents[2].strip())

        jstree_parent = str(parent_id)
        if parent_id == -1:
            jstree_parent = "#"
        jstree_object.append({'parent': jstree_parent, 'id': str(max_id), 'text': str(li.contents[2].strip())})
        print route

        if outputfile:
            outputfile.write(route + '\n')

        for leaf in li.findAll('ul', {'class': 'non_leaf show'}, recursive=False):

            max_id = iterate_elements(leaf, depth,
                                      parent=parent_id, parent_id=max_id,
                                      max_id=max_id, outputfile=outputfile)

    return max_id

def download_dmvi_categories(outputfile=None):

    resp = urllib2.urlopen('http://www.dmvi.org.uk/browsevocab.php#0')

    if resp.code == 200:
        data = resp.read()

        root_elm = BeautifulSoup(data)

        for elm in root_elm.findAll('ul', {'id': 'vocab'}):
            iterate_elements(elm, 0, "category", parent_id=-1, max_id=-1, outputfile=outputfile)


jstree_object = []


outputfile = open('./categories.txt', 'a')

download_dmvi_categories(outputfile)

outputfile.close()

print jstree_object