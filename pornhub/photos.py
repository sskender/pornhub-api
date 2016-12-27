# -*- coding: UTF-8 -*-

from .core import *

class Photos(object):
    
    def __init__(self, keywords=[], *args):
        self.keywords = keywords
        self.photos_queue = Queue()

    def _loadAlbumsPage(self, page_num):
        # url example:
        # pornhub.com/albums/female-straight?search=arg1+arg2
        # pornhub.com/albums/uncategorized?search=arg1&page=3

        payload = {"search" : "", "page" : page_num}
        categories = list()

        for item in self.keywords:
            if (item == "female"):
                categories.append(item)
            elif (item == "straight"):
                categories.append(item)
            elif (item == "misc"):
                categories.append(item)
            elif (item == "male"):
                categories.append(item)
            elif (item == "gay"):
                categories.append(item)
            else:
                payload["search"] += (item + " ")

        search_url = BASE_URL + ALBUMS_URL + "-".join(categories) + "?"
        r = requests.get(search_url, params=payload, headers=HEADERS)
        html = r.text

        return BeautifulSoup(html, "lxml")

    def _scrapAlbumsURL(self, soup_data):
        album_divs = soup_data.find_all("div", { "class" : "photoAlbumListBlock" } )
        albums_url = list()

        for album_div in album_divs:
            for a_tag in album_div.find_all("a", href=True):
                url = a_tag.attrs["href"]
                if isAlbum(url):
                    albums_url.append(BASE_URL + url)
                    break

        return albums_url

    def _scrapPhotoFullURL(self, preview_url):
        r = requests.get(preview_url, headers=HEADERS)
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        for image in soup.find_all("img", src=True):
            image_url = image.attrs["src"]
            if isPhoto(image_url):
                self.photos_queue.put(str(image_url))
                return image_url
        return False
        
    def _scrapAlbumPhotos(self, album_url):
        r = requests.get(album_url, headers=HEADERS)
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        for possible_image in soup.find_all("a", href=True):
            try:
                preview_url = possible_image.attrs["href"]
                if isPhotoPreview(preview_url):
                    yield (BASE_URL + preview_url)
            except Exception as e:
                pass

    def getPhotos(self, quantity = 1, page = 1, infinity = False):
        """
        Download photos.

        :param quantity: number of photos to return
        :param page: starting page number
        :param infinity: never stop downloading
        """

        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0
        workers = list()

        while True:

            for album_url in self._scrapAlbumsURL(self._loadAlbumsPage(page)):
                for preview_url in self._scrapAlbumPhotos(album_url):

                    worker = Thread(target=self._scrapPhotoFullURL, kwargs={"preview_url" : preview_url})
                    worker.start()
                    workers.append(worker)
                    
                    while not self.photos_queue.empty():
                        if (found < quantity) or (infinity):
                            yield self.photos_queue.get()
                            found += 1
                        else:
                            raise StopIteration

                    if (len(workers)+1) % 4 == 0:
                        time.sleep(TIME_TO_WAIT)

            page += 1