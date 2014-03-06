import json
import urllib2
from django.utils.encoding import smart_unicode
from image_scrape import downloadImage, getImageTags

__author__ = 'ubuntu'


def get_json(url, search_term, page=1, image_size='o'):
    url = url + search_term + '&page=' + str(page) + '&w=12403504%40N02&magic_cookie=0f723f9fa7a22f1e2199967fbb5f2e7b'
    print url

    resp = urllib2.urlopen(url)

    if resp.code == 200 and resp.headers['content-type'] == 'application/json':

        json_object = json.loads(resp.read())
        imageURLs = []

        for search_result in json_object['photos']:
            imageURLs.append(search_result['sizes'][image_size]['url'])

        return imageURLs

    else:
        print 'return type not json'
        print resp.headers['content-type']
        return None


def download_from_search_term(search_term, start_page, download_folder, number_of_pages=None, image_size='o'):
    all_image_urls = []

    to_continue = True
    while to_continue:
        image_urls = get_json('http://www.flickr.com/search?data=1&m=tags&q=',
                              search_term=search_term, page=start_page, image_size=image_size)
        if image_urls is None:
            to_continue = False
        else:
            for url in image_urls:
                print url
                all_image_urls.append(url)
            start_page += 1
        if number_of_pages is not None and start_page >= number_of_pages:
            to_continue = False

    outputfile = open('./tags.txt', 'a')

    for url in all_image_urls:
        outputfile.write(url + '\n')

        downloadImage(url, download_folder=download_folder)

        imageID = (url.rsplit('/', 1)[1]).split('_')[0]

        tags = getImageTags('http://www.flickr.com/photos/britishlibrary/' + imageID)
        outputfile.write('http://www.flickr.com/photos/britishlibrary/' + imageID + '\n')

        if tags is not None:
           for key in tags:
                print key + '       :       ' + tags[key]
                if outputfile is not None:
                    outputString = (key + "::::" + tags[key] + '\n')
                    strstring = smart_unicode(outputString, encoding='utf-8', strings_only=False,
                                          errors='strict').encode('utf-8')
                    outputfile.write(strstring)

    outputfile.close()


# print get_json('http://www.flickr.com/search?data=1&q=', search_term='map', page=20)