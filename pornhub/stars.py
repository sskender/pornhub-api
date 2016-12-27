# -*- coding: UTF-8 -*-

from .core import *

class Stars(object):

    def __init__(self, *args):
        pass

    def _loadStarsPage(self, page_num):
        payload = { "page" : page_num }
        r = requests.get(BASE_URL + PORNSTARS_URL, params=payload, headers=HEADERS)
        html = r.text

        return BeautifulSoup(html, "lxml")

    def _scrapLiStars(self, soup_data):
        # get div with list of stars (month popular is the 1st)
        div_el = soup_data.findAll("div", { "class" : "sectionWrapper", "id" : "pornstarsFilterContainer" } )[0]
        # get each porn star info (held in list block)
        li_el = div_el.find_all("li")
        
        return li_el

    def _scrapStarInfo(self, li_el):
        data = {
            "name"      : None,         # string
            "url"       : None,         # string
            "photo"     : None,         # string
            "videos"    : None          # integer
        }

        # scrap url
        for a_tag in li_el.find_all("a", href=True):
            try:
                url = a_tag.attrs["href"]
                if isStar(url):
                    data["url"] = BASE_URL + url
                    break
            except Exception as e:
                pass

        # scrap name and photo url
        for img_tag in li_el.find_all("img", src=True):
            try:
                photo_url = img_tag.attrs["src"]
                if isStarPhoto(photo_url):
                    data["photo"] = photo_url
                    data["name"] = img_tag.attrs["alt"]
                    break
            except Exception as e:
                pass

        # scrap num of videos
        for span_tag in li_el.find_all("span", { "class" : "videosNumber" }):
            try:
                data["videos"] = int( str(span_tag).split(">")[1].split(" ")[0] )
                break
            except Exception as e:
                pass

        # return
        return data if None not in data.values() else False

    def getStars(self, quantity = 1, page = 1, infinity = False):
        """
        Get pornstar's basic informations.

        :param quantity: number of pornstars to return
        :param page: starting page number
        :param infinity: never stop downloading
        """

        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0

        while True:

            for possible_star in self._scrapLiStars(self._loadStarsPage(page)):
                data_dict = self._scrapStarInfo(possible_star)

                if data_dict:
                    yield data_dict

                    if not infinity:
                        found += 1
                        if found >= quantity: return

            page += 1
