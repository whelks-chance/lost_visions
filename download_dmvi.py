import urllib2
from BeautifulSoup import BeautifulSoup

__author__ = 'ubuntu'


def iterate_elements(elm, depth, route, outputfile=None):

    parent = route

    for li in elm.findAll('li', recursive=False):

        # print li.contents[2].strip()
        route = (parent + ">" + li.contents[2].strip())

        print route

        if outputfile:
            outputfile.write(route + '\n')

        for leaf in li.findAll('ul', {'class': 'non_leaf show'}, recursive=False):

            depth += 1

            if outputfile:
                outputfile.write('\n')

            iterate_elements(leaf, depth, route, outputfile)


def download_dmvi_categories(outputfile=None):

    resp = urllib2.urlopen('http://www.dmvi.org.uk/browsevocab.php#0')

    if resp.code == 200:
        data = resp.read()

        root_elm = BeautifulSoup(data)

        for elm in root_elm.findAll('ul', {'id': 'vocab'}):
            iterate_elements(elm, 0, "category", outputfile)


outputfile = open('./categories.txt', 'a')

download_dmvi_categories(outputfile)

outputfile.close()