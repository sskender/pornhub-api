# -*- coding: UTF-8 -*-

from .core import *
import re

class Videos(object):
    
    def __init__(self, ProxyDictionary, keywords=[], *args):
        self.keywords = keywords
        self.ProxyDictionary = ProxyDictionary

    def _craftVideoURL(self, page_num):
        # url example:
        # pornhub.com/video/search?search=arg1+arg2
        # pornhub.com/video/search?search=arg1+arg2&p=professional
        # pornhub.com/video/search?search=arg1+arg2&p=professional&page=3
        payload = {"page" : page_num}

        if self.keywords:
            payload["search"] = ''

            for item in self.keywords:
                if (item == "professional") or (item == "pro"):
                    payload["p"] = "professional"
                elif (item == "homemade") or (item == "home"):
                    payload["p"] = "homemade"
                else:
                    payload["search"] += (item + " ")

            payload["search"] = payload["search"].strip() # removing the last space, otherwise it will always be 1 page

        return payload

    def _loadVideosPage(self, page_num):
        
        if self.keywords:
            r = requests.get(BASE_URL + VIDEOS_URL + SEARCH_URL, params=self._craftVideoURL(page_num), headers=HEADERS, proxies=self.ProxyDictionary)
        else:
            r = requests.get(BASE_URL + VIDEOS_URL, params=self._craftVideoURL(page_num), headers=HEADERS, proxies=self.ProxyDictionary)

        html = r.text
        return BeautifulSoup(html, "lxml")

    def _scrapLiVideos(self, soup_data):
        return soup_data.find_all("li", { "class" : re.compile(".*videoblock videoBox.*") } )

    def _scrapVideoInfo(self, div_el):
        data = {
            "name"          : None,     # string
            "url"           : None,     # string
            "rating"        : None,     # integer
            "duration"      : None,     # string
            "background"    : None      # string
        }

        # scrap url, name
        for a_tag in div_el.find_all("a", href=True):
            try:
                url = a_tag.attrs["href"]
                if isVideo(url):
                    data["url"] = BASE_URL + url
                    data["name"] = a_tag.attrs["title"]
                    break
            except Exception as e:
                pass

        # scrap background photo url
        for img_tag in div_el.find_all("img", src=True):
            try:
                url = img_tag.attrs["data-thumb_url"]
                if isVideoPhoto(url):
                    data["background"] = url
                    break
            except Exception as e:
                pass

        # scrap duration
        for var_tag in div_el.find_all("var", { "class" : "duration" } ):
            try:
                data["duration"] = str(var_tag).split(">")[-2].split("<")[-2]
                break
            except Exception as e:
                pass

        # scrap rating
        for div_tag in div_el.find_all("div", { "class" : "value" } ):
            try:
                data["rating"] = int( str(div_tag).split(">")[1].split("%")[0] )
                break
            except Exception as e:
                pass

        # return
        return data if None not in data.values() else False

    def getVideos(self, quantity = 1, page = 1, infinity = False):
        """
        Get videos basic informations.

        :param quantity: number of videos to return
        :param page: starting page number
        :param infinity: never stop downloading
        """

        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0

        while True:
            first_four_skip = 4  # first 4 elements skip, they are not relevant to the query
            
            for possible_video in self._scrapLiVideos(self._loadVideosPage(page)):
                if first_four_skip > 0:  # first 4 elements skip , they are not relevant to the query
                    first_four_skip -= 1  # first 4 elements skip , they are not relevant to the query
                else:
                    data_dict = self._scrapVideoInfo(possible_video)

                    if data_dict:
                        yield data_dict

                        if not infinity:
                            found += 1
                            if found >= quantity: return

            page += 1