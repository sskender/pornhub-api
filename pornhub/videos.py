# -*- coding: UTF-8 -*-

from .core import *

class Videos(object):
    
    def __init__(self, ProxyDictionary, keywords=[], *args, **kwargs):
        self.keywords = keywords
        self.ProxyDictionary = ProxyDictionary
        self.video_sort = kwargs

    def _sortVideos(self, sort_by):
        sort_dict = dict()

        if not sort_by:
            return sort_dict
        
        sort_keys = sort_by.keys()

        if "sort_by" in sort_keys:
            if self.keywords:
                orders = {"recent": "mr", "view": "mv", "rate": "tr", "long": "lg"}
            else:
                orders = {"view": "mv", "rate": "tr", "hot":"ht", "long": "lg", "new": "cm"}
            
            for key in orders:
                if key in sort_by["sort_by"].lower():
                    sort_dict["o"] = orders[key]
        
        if "period" in sort_keys and ("mv" in sort_dict.values() or "tr" in sort_dict.values()):
            periods = {"day": "t", "week": "w", "month": "m", "year": "y", "all": "a"}
            for key in periods:
                if key in sort_by["period"].lower():
                    sort_dict["t"] = periods[key]
        
        if "region" in sort_keys and ("mv" in sort_dict.values() or "ht" in sort_dict.values()):
            sort_dict["cc"] = sort_by["region"]
        
        return sort_dict

    def _craftVideosURL(self, page_num):
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
        
        if self.video_sort:
            video_sort = self._sortVideos(self.video_sort)
            for key in video_sort:
                payload[key] = video_sort[key]
        
        payload["page"] = page_num

        return payload

    def _loadVideoPage(self, page_num=None, url=None, viewkey=None):
        
        # load search page
        if page_num:
            search_url = BASE_URL + VIDEOS_URL
            if self.keywords:
                search_url += SEARCH_URL
            r = requests.get(search_url, params=self._craftVideosURL(page_num), headers=HEADERS, proxies=self.ProxyDictionary)
        
        # load video page
        else:
            if url and isVideo(url):
                r = requests.get(url, headers=HEADERS, proxies=self.ProxyDictionary)
            else:
                r = requests.get(BASE_URL + VIDEO_URL + viewkey, headers=HEADERS, proxies=self.ProxyDictionary)
        
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _scrapLiVideos(self, soup_data):
        return soup_data.find("div", class_="sectionWrapper").find_all("li", { "class" : re.compile(".*videoblock videoBox.*") } )

    def _scrapVideosInfo(self, div_el):
        data = {
            "title"         : None,     # string
            "url"           : None,     # string
            "embed"         : None,     # string
            "rating"        : None,     # integer
            "duration"      : None,     # string
            "img"           : None      # string
        }

        # scrap url, name
        for a_tag in div_el.find_all("a", href=True):
            try:
                url = a_tag.attrs["href"]
                if isVideo(url):
                    data["url"] = BASE_URL + url
                    data["embed"] = EMBED_URL + re.findall(r"viewkey=(\S+)", url)[0]
                    data["title"] = a_tag.attrs["title"]
                    break
            except Exception as e:
                pass

        # scrap background photo url
        for img_tag in div_el.find_all("img", src=True):
            try:
                url = img_tag.attrs["data-thumb_url"]
                if isVideoPhoto(url):
                    data["img"] = url
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

    # Scrap upload_date, author, accurate_views
    def _scrapScriptInfo(self, soup_data):
        data = dict()
        script_dict = json.loads(soup_data)
        data["author"] = script_dict["author"] 
        data["upload_date"] = re.findall(r"\d{4}-\d{2}-\d{2}",script_dict["uploadDate"])[0]
        data["accurate_views"] = int(script_dict["interactionStatistic"][0]["userInteractionCount"].replace(",",""))
        return data

    def _scrapVideoInfo(self, soup_data):

        data = {
            "title"             : None,     # string
            "views"             : None,     # string
            "accurate_views"    : None,     # integer
            "rating"            : None,     # integer
            "duration"          : None,     # string
            "loaded"            : None,     # string
            "upload_date"       : None,     # string
            "likes"             : None,     # string
            "accurate_likes"    : None,     # integer
            "dislikes"          : None,     # string
            "accurate_dislikes" : None,     # integer
            "favorite"          : None,     # string
            "author"            : None,     # string
            "pornstars"         : None,     # list
            "categories"        : None,     # list
            "tags"              : None,     # list
            "production"        : None,     # string
            "url"               : None,     # string
            "img"               : None,     # string
            "embed"             : None,     # string
            "geo_block"         : False     # bool
        }

        url = soup_data.find("head").find("link", {"rel": "canonical"}).attrs["href"]
        data["url"] = url
        data["embed"] = EMBED_URL + re.findall(r"viewkey=(\S+)", url)[0]

        if soup_data.find("div", {"class" : "geoBlocked"}):
            data["geo_block"] = True
            return data
        
        data["title"] = soup_data.find("head").find("title").text
        data["img"] = soup_data.find("head").find("link", {"rel": "preload"}).attrs["href"]

        duration = int(soup_data.find("head").find("meta", {"property": "video:duration"}).attrs["content"])
        data["duration"] = str(datetime.timedelta(seconds=duration))

        # Scrap upload_date, author, accurate_views
        try:
            script_data = self._scrapScriptInfo(soup_data.find("script", {"type": "application/ld+json"}).text)
            for key in script_data:
                data[key] = script_data[key]
        except Exception as e:
            pass

        video = soup_data.find("div", {"class": "video-wrapper"})    
        data["views"] = video.find("span", {"class": "count"}).text  # Scrap view
        data["rating"] = int(video.find("span", {"class": "percent"}).text.replace("%",""))  # Scrap rating
        data["loaded"] = video.find("span", {"class": "white"}).text  # Scrap loaded
        data["likes"] = video.find("span", {"class": "votesUp"}).text  # Scrap like
        data["accurate_likes"] = video.find("span", {"class": "votesUp"})["data-rating"]  # Scrap accurate_like
        data["dislikes"] = video.find("span", {"class": "votesDown"}).text  # Scrap dislike
        data["accurate_dislikes"] = video.find("span", {"class": "votesDown"}).attrs["data-rating"] # Scrap accurate_dislike
        data["favorite"] = video.find("span", {"class": "favoritesCounter"}).text.strip() # Scrap favorite
        data["production"] = video.find("div", {"class": "productionWrapper"}).find_all("a", {"class": "item"})[0].text # Scrap production

        # Scrap pornstars
        data["pornstars"] = list()
        for star in video.find_all("a", {"class": "pstar-list-btn"}):
            data["pornstars"].append(star.text.strip())
        
        # Scrap categories
        data["categories"]= list()
        for category in video.find("div", {"class": "categoriesWrapper"}).find_all("a", {"class": "item"}):
            data["categories"].append(category.text)

        # Scrap tags
        data["tags"] = list()
        for tag in video.find("div", {"class":"tagsWrapper"}).find_all("a", {"class": "item"}):
            data["tags"].append(tag.text)

        return data

    def getVideo(self, url=None, viewkey=None):
        """
        Get video informations.
        You can enter the full video url or just the viewkey
        :url: video url on phub
        :viewkey: viewkey of video
        """
        if url or viewkey:
            return self._scrapVideoInfo(self._loadVideoPage(url=url, viewkey=viewkey))
        else:
            raise ValueError("URL or Viewkey not entered")

    def getVideos(self, quantity = 1, page = 1, full_data=False, infinity = False, **sort_dict):
        """
        Get videos basic informations.

        :param quantity: number of videos to return
        :param page: starting page number
        :param full_data: take full video data
        :param infinity: never stop downloading
        """
        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0

        if sort_dict:
            self.video_sort.update(sort_dict)

        while True:
            for possible_video in self._scrapLiVideos(self._loadVideoPage(page_num=page)):
                data_dict = self._scrapVideosInfo(possible_video)

                if data_dict:
                    if full_data:
                        yield self.getVideo(data_dict["url"])
                    else:
                        yield data_dict

                    if not infinity:
                        found += 1
                        if found >= quantity: return

            page += 1