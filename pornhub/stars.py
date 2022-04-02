# -*- coding: UTF-8 -*-

from .core import *

class Stars(object):

    def __init__(self, ProxyDictionary, *args):
        self.ProxyDictionary = ProxyDictionary

    def _sortStars(self, sort_by):
        sort_dict = dict()

        if not sort_by:
            return sort_dict
        
        sort_types = {"view": "mv", "trend": "t", "subs": "ms", "alpha": "a", "videos": "nv", "random": "r"}

        for key in sort_types:
            if key in sort_by.lower():
                sort_dict["o"] = sort_types[key]
                return sort_dict
        
        return sort_dict
    
    def _craftStarsPage(self, page_num, sort_by):
        payload = dict()

        stars_sort = self._sortStars(sort_by)
        for key in stars_sort:
            payload[key] = stars_sort[key]
        
        payload["page"] = page_num
        return payload
        
    def _loadStarsPage(self, page_num, sort_by):
        
        r = requests.get(BASE_URL + PORNSTARS_URL, params=self._craftStarsPage(page_num, sort_by), headers=HEADERS, proxies=self.ProxyDictionary)
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
            "name"          : None,         # string
            "rank"          : None,         # integer
            "type"          : None,         # string
            "videos"        : None,         # integer
            "views"         : None,         # string
            "verified"      : False,        # bool
            "trophy"        : False,        # bool
            "url"           : None,         # string
            "photo"         : None,         # string
        }
        
        # scrap rank
        for span_tag in li_el.find_all("span", class_="rank_number"):
            try:
                data["rank"] = int(span_tag.text)
            except Exception as e:
                pass
        
        # scrap name and url
        for a_tag in li_el.find_all("a", href=True):
            try:
                url = a_tag.attrs["href"]
                if isStar(url):
                    data["url"] = BASE_URL + url
                    data["name"] = a_tag.attrs["data-mxptext"]                 
                    break
            except Exception as e:
                pass
   
        # scrap photo url
        for img_tag in li_el.find_all("img", src=True):
            try:
                photo_url = img_tag.attrs["data-thumb_url"]
                if isStarPhoto(photo_url):
                    data["photo"] = photo_url
                    break
            except Exception as e:
                pass

        # scrap num of videos and views
        for span_tag in li_el.find_all("span", { "class" : "videosNumber" }):
            try:
                data["videos"] = int(span_tag.text.split()[0])
                data["views"] = span_tag.text.split()[2]
                break
            except Exception as e:
                pass

        # scrap badges
        for span_tag in li_el.find_all("span", class_="modelBadges"):

            if span_tag.find_all("i", class_="verifiedIcon"):
                data["verified"] = True

            if span_tag.find_all("i", class_="trophyPornStar"):
                data["trophy"] = True
        
        # scrap type
        try:
            if "pornstar" in data["url"]:
                data["type"] = "pornstar"
            else:
                data["type"] = "model"
        except Exception as e:
                pass
        
        # return
        return data if None not in data.values() else False

    def getStars(self, quantity = 1, page = 1, sort_by=None, infinity = False):
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

            for possible_star in self._scrapLiStars(self._loadStarsPage(page, sort_by)):
                data_dict = self._scrapStarInfo(possible_star)

                if data_dict:
                    yield data_dict

                    if not infinity:
                        found += 1
                        if found >= quantity: return

            page += 1
