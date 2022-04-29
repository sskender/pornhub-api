# -*- coding: UTF-8 -*-

from .core import *

class Gifs(object):
    
    def __init__(self, ProxyDictionary, keywords=[], *args, **kwargs):
        self.keywords = keywords
        self.ProxyDictionary = ProxyDictionary
        self.gifs_sort = kwargs

    def _sortGifs(self, sort_by):
        sort_dict = dict()
        if not sort_by:
            return sort_dict
        
        sort_keys = sort_by.keys()
        if "sort_by" in sort_keys:
            orders = {"recent": "mr", "view": "mv", "rate": "tr"}
            for key in orders:
                if key in sort_by["sort_by"].lower():
                    sort_dict["o"] = orders[key]

        if "period" in sort_keys and ("mv" in sort_dict.values() or "tr" in sort_dict.values()):
            periods = {"day": "t", "week": "w", "month": "m", "all": "a"}
            for key in periods:
                if key in sort_by["period"].lower():
                    sort_dict["t"] = periods[key]
        return sort_dict

    def _craftGifsURL(self, page_num):
        payload = dict()
        if self.keywords:
            search = ""
            for item in self.keywords:
                item = re.sub(r"[^\w\s]", "", item).replace("_", " ")
                search += " " + item
            payload["search"] = search.strip()

        if self.gifs_sort:
            gifs_sort = self._sortGifs(self.gifs_sort)
            for key in gifs_sort:
                payload[key] = gifs_sort[key]
        payload["page"] = page_num
        return payload

    def _loadGifsPage(self, page_num=None, url=None, viewkey=None):
        # load search gifs page
        if page_num:
            search_url = BASE_URL + GIFS_URL
            if self.keywords:
                search_url += SEARCH_URL
            r = requests.get(search_url, params=self._craftGifsURL(page_num=page_num), headers=HEADERS, proxies=self.ProxyDictionary)
        # load gif page
        else:
            if url and isGif(url):
                r = requests.get(url, headers=HEADERS, proxies=self.ProxyDictionary)
            else:
                r = requests.get(BASE_URL + GIF_URL + viewkey, headers=HEADERS, proxies=self.ProxyDictionary)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _scrapLiGifs(self, soup_data):
        section_wrappers = soup_data.findAll("div", class_="sectionWrapper")
        for wrapper in section_wrappers:
            LiGifs = wrapper.find_all("li", {"class": re.compile(".*gifVideoBlock js-gifVideoBlock.*")})
            if LiGifs != []:
                return LiGifs
        raise Exception("LiGifs Not Found")

    def _scrapGifsInfo(self, div_el):
        data = {
                "title"         : None,     # string
                "url"           : None,     # string
                "embed"         : None,     # string
                "img"           : None,     # string
                "gif"           : None,     # string
                "mp4"           : None,     # string
                "webm"          : None      # string
                }
        a_el = div_el.find("a")
        url = a_el["href"]
        data["title"] = a_el.span.text.strip()
        data["url"] = BASE_URL + url
        data["embed"] = data["url"].replace("gif", "embedgif")
        data["img"] = a_el.video["data-poster"]
        data["gif"] = GIF_DATA_URL + url + ".gif"
        data["mp4"] = a_el.video["data-mp4"]
        data["webm"] = a_el.video["data-webm"]
        return data
    
    def _scrapGifInfo(self, bs):
        data = {
                "title"                   : None,     # string
                "url"                     : None,     # string
                "img"                     : None,     # string
                "gif"                     : None,     # string
                "mp4"                     : None,     # string
                "webm"                    : None,     # string
                "embed"                   : None,     # string
                "views"                   : None,     # integer
                "rate"                    : None,     # integer
                "stars"                   : None,     # list
                "tags"                    : None,     # list
                "loaded"                  : None,     # string
                "original_title"          : None,     # string
                "original_url"            : None,     # string
                }

        div_el = bs.find("div", {"id": "js-gifToWebm"})
        try:
            data["title"] = div_el.attrs["data-gif-title"]
        except Exception as e:
            return data
        data["gif"] = div_el.attrs["data-gif"]
        data["mp4"] = div_el.attrs["data-mp4"]
        data["webm"] = div_el.attrs["data-webm"]

        head_el = bs.find("head")
        data["url"] = head_el.find("link", {"rel": "canonical"}).attrs["href"]
        data["img"] = head_el.find("link", {"rel": "image_src"}).attrs["href"]

        data["embed"] = bs.find("input", {"id": "directlink"})["value"]
        data["views"] = int(re.findall(r"\d+", bs.find("li", {"class": "gifViews"}).text.strip())[0])
        data["rate"] = int(bs.find("div", {"class": "votePercentage"}).span.text)
        data["loaded"] = bs.find("div", {"class": "added"}).text.strip()
        data["original_title"] = bs.find("div", {"class": "bottomMargin"}).a.text.strip()
        data["original_url"] = BASE_URL + re.findall(r"(\S+)&", bs.find("div", {"class": "bottomMargin"}).a.attrs["href"])[0]

        # scrap stars
        data["stars"] = []
        for star in bs.find_all("a", {"class": "pstar-list-btn"}):
            data["stars"].append(star.text.strip())
        
        # scrap tags
        data["tags"] = []
        for tag in bs.find("ul", {"class": "tagList"}).find_all("a", {"class": "tagText"}):
            data["tags"].append(tag.text.strip())

        return data

    def getGif(self, url=None, viewkey=None):
        if url or viewkey:
            return self._scrapGifInfo(self._loadGifsPage(url=url, viewkey=viewkey))
        else:
            raise ValueError("URL or Viewkey not entered")

    def getGifs(self, quantity=1, page=1, full_data=False, infinity=False, **sort_dict):
        """
        Get gifs.
        :param quantity: number of gifs to return
        :param page: starting page number
        :param infinity: never stop downloading
        """

        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0

        if sort_dict:
            self.gifs_sort.update(sort_dict)

        while True:
            for possible_gifs in self._scrapLiGifs(self._loadGifsPage(page_num=page)):
                data_dict = self._scrapGifsInfo(possible_gifs)

                if data_dict:
                    if full_data:
                        yield self.getGif(url=data_dict["url"])
                    else:
                        yield data_dict

                    if not infinity:
                        found += 1
                        if found >= quantity: return

            page += 1