from django.utils.encoding import smart_unicode
from flickr_json_api import get_json, download_from_search_term
from image_scrape import downloadImage, getImageTags, getTagsFromBasePage

__author__ = 'ubuntu'




search_term = 'portrait'
page = 3

# download_from_search_term(search_term, page, number_of_pages=page, download_folder=search_term, image_size='z')

getTagsFromBasePage(baseurl='http://www.flickr.com/search?data=1&m=tags&q=portrait&w=12403504%40N02&append=1',
                    downloadImages=True,
                    download_folder='portrait'
)