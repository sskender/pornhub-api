# -*- coding: UTF-8 -*-

from .core import *
import re
from .video import Video

class Videos(Video):
    
    def __init__(self, ProxyDictionary, keywords=[], *args):
        self.keywords = keywords
        self.ProxyDictionary = ProxyDictionary

    def _sortVideos(self, sort_by):
        sort_dict = dict()

        if not sort_by:
            return sort_dict
        
        if self.keywords:
            sort_types = {"recent": "mr", "view": "mv", "rate": "tr", "long": "lg"}
        else:
            sort_types = {"view": "mv", "rate": "tr", "hot":"ht", "long": "lg", "new": "cm"}
        
        for key in sort_types:
            if key in sort_by.lower():
                sort_dict["o"] = sort_types[key]
                return sort_dict
        
        return sort_dict

    def _craftVideosURL(self, page_num, sort_by):
        # url example:
        # pornhub.com/video/search?search=arg1+arg2
        # pornhub.com/video/search?search=arg1+arg2&p=professional
        # pornhub.com/video/search?search=arg1+arg2&p=professional&page=3
        payload = dict()

        if self.keywords:
            payload["search"] = ""

            for item in self.keywords:
                if (item == "professional") or (item == "pro"):
                    payload["p"] = "professional"
                elif (item == "homemade") or (item == "home"):
                    payload["p"] = "homemade"
                else:
                    payload["search"] += (item + " ")

            payload["search"] = payload["search"].strip() # removing the last space, otherwise it will always be 1 page
        
        video_sort = self._sortVideos(sort_by)
        for key in video_sort:
            payload[key] = video_sort[key]
        
        payload["page"] = page_num

        return payload

    def _loadVideosPage(self, page_num, sort_by):
        
        if self.keywords:
            r = requests.get(BASE_URL + VIDEOS_URL + SEARCH_URL, params=self._craftVideosURL(page_num, sort_by), headers=HEADERS, proxies=self.ProxyDictionary)
        else:
            r = requests.get(BASE_URL + VIDEOS_URL, params=self._craftVideosURL(page_num, sort_by), headers=HEADERS, proxies=self.ProxyDictionary)

        html = r.text
        return BeautifulSoup(html, "lxml")

    def _scrapLiVideos(self, soup_data):
        return soup_data.find_all("li", { "class" : re.compile(".*videoblock videoBox.*") } )

    def _scrapVideosInfo(self, div_el):
        data = {
            "title"         : None,     # string
            "url"           : None,     # string
            "rating"        : None,     # integer
            "duration"      : None,     # string
            "img_url"       : None      # string
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

    def getVideos(self, quantity = 1, page = 1, sort_by = None, full_data=False, infinity = False):
        """
        Get videos basic informations.

        :param quantity: number of videos to return
        :param page: starting page number
        :param sort_by: sort type
        :param full_data: take full video data
        :param infinity: never stop downloading
        """

        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0

        while True:
            first_four_skip = 4  # first 4 elements skip, they are not relevant to the query
            
            for possible_video in self._scrapLiVideos(self._loadVideosPage(page, sort_by)):
                if first_four_skip > 0:  # first 4 elements skip , they are not relevant to the query
                    first_four_skip -= 1  # first 4 elements skip , they are not relevant to the query
                else:
                    data_dict = self._scrapVideosInfo(possible_video)

                    if data_dict:
                        if full_data:
                            yield self.getVideo(data_dict['url'])
                        else:
                            yield data_dict

                        if not infinity:
                            found += 1
                            if found >= quantity: return

            page += 1