import urllib2
from BeautifulSoup import BeautifulSoup
import nltk

__author__ = 'ubuntu'


def getImageCatagories_depositphotos():

    resp = urllib2.urlopen('http://depositphotos.com/category/')

    if resp.code == 200:
        data = resp.read()

        xml = BeautifulSoup(data)

        for elm in xml.findAll('div', {'class': 'categories_img d_category'}):
            for div in elm.findAll('div'):
                for a in div.findAll('a'):
                    for img in a.findAll('img'):
                        if hasattr(img, 'alt'):
                            if img['alt'] != 'Overlay':
                                print img['alt']



def getImageCatagories_photospin():
    print '\n\n'

    resp = urllib2.urlopen('https://www.photospin.com/browse_photos.asp?')

    if resp.code == 200:
        data = resp.read()

        xml = BeautifulSoup(data)

        for elm in xml.findAll('div', {'class': 'six columns'}):
            for h4 in elm.findAll('h4'):
                print h4.text


def getImageCatagories_shutterpoint():
    print '\n\n'

    resp = urllib2.urlopen('http://www.shutterpoint.com/Photos-BrowseCat.cfm')

    if resp.code == 200:
        data = resp.read()

        xml = BeautifulSoup(data)

        for elm in xml.findAll('table', {'id': 'catTable'}):
            for tr in elm.findAll('tr'):
                for td in tr.findAll('td'):
                    for p in td.findAll('p'):
                        for a in p.findAll('a'):
                            print a.text


def getImageCatagories_istockphoto():
    print '\n\n'

    resp = urllib2.urlopen('http://www.istockphoto.com/browse')

    if resp.code == 200:
        data = resp.read()

        xml = BeautifulSoup(data)

        allLists = dict()

        for elm in xml.findAll('div', {'class': 'fullPage'}):
            for ul in elm.findAll('ul', {'class': 'separatedList'}):
                for li_top in ul.findAll('li'):
                    sublist = []
                    for ul in li_top.findAll('ul'):
                        for li in ul.findAll('li'):
                            for a in li.findAll('a'):
                                sublist.append(a.text)

                    for h2 in li_top.findAll('h2'):
                        for a in h2.findAll('a'):
                            print '    ' + a.text
                            for title in sublist:
                                print title
                            allLists[a.text] = sublist
