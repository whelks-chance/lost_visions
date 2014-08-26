from django.utils.encoding import smart_unicode
from flickr_json_api import get_json, download_from_search_term
from image_scrape import downloadImage, getImageTags, getTagsFromBasePage

__author__ = 'ubuntu'




search_term = 'etching'
page = 1
base_url = 'http://www.flickr.com/search?data=1&q=' + search_term + '&w=12403504%40N02&append=1'

# tags only
# base_url = 'http://www.flickr.com/search?data=1&m=tags&q=' + search_term + '&w=12403504%40N02&append=1'


# base_url = 'http://127.0.0.1:8000/static/blflkr.html'

# base_url = 'http://127.0.0.1:8080/static/flkr_music.html'

# download_from_search_term(search_term, page, number_of_pages=page, download_folder=search_term, image_size='z')

getTagsFromBasePage(baseurl=base_url,
                    downloadImages=True,
                    download_folder=search_term,
                    basepagenumber=page
)