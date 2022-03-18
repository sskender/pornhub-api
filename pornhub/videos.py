# -*- coding: UTF-8 -*-

from .core import *
import re
import json

class Videos(object):
    
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

    def _loadPage(self, page_num=None, sort_by=None, url=None, viewkey=None):
        
        # load search page
        if page_num:
            if self.keywords:
                r = requests.get(BASE_URL + VIDEOS_URL + SEARCH_URL, params=self._craftVideosURL(page_num, sort_by), headers=HEADERS, proxies=self.ProxyDictionary)
            else:
                r = requests.get(BASE_URL + VIDEOS_URL, params=self._craftVideosURL(page_num, sort_by), headers=HEADERS, proxies=self.ProxyDictionary)
        # load video page
        else:
            if url and isVideo(url):
                r = requests.get(url, headers=HEADERS, proxies=self.ProxyDictionary)
            else:
                r = requests.get(BASE_URL + VIDEO_URL + viewkey, headers=HEADERS, proxies=self.ProxyDictionary)
        
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
                    data["title"] = a_tag.attrs["title"]
                    break
            except Exception as e:
                pass

        # scrap background photo url
        for img_tag in div_el.find_all("img", src=True):
            try:
                url = img_tag.attrs["data-thumb_url"]
                if isVideoPhoto(url):
                    data["img_url"] = url
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

    # Scrap duration, upload_date, author, embed_url, accurate_views
    def _scrapScriptInfo(self, soup_data):

        data = dict()
        script_dict = json.loads(soup_data.replace("'",'"'))

        data["author"] = script_dict["author"] 
        data["embed_url"] = script_dict['embedUrl']
        data["duration"] = ":".join(re.findall(r'\d\d',script_dict['duration']))
        data["upload_date"] = re.findall(r'\d{4}-\d{2}-\d{2}',script_dict['uploadDate'])[0]
        data["accurate_views"] = int(script_dict['interactionStatistic'][0]['userInteractionCount'].replace(',',''))

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
            "img_url"           : None,     # string
            "embed_url"         : None      # string
        }

        # Scrap duration, upload_date, author, embed_url, accurate_views
        try:
            script_data = self._scrapScriptInfo(soup_data.find("script", type='application/ld+json').text)
        except:
            data['title'] = '***Video not available in your country***'
            return data

        for key in script_data:
            data[key] = script_data[key]
        
        data['title'] = soup_data.find("head").find('title').text
        data['url'] = soup_data.find("head").find('link', rel="canonical")['href']
        data["img_url"] = soup_data.find("head").find('link', rel="preload")['href']

        video = soup_data.find("div", class_='video-wrapper')
        
        data['views'] = video.find("span", class_="count").text  # Scrap view
        data['rating'] = int(video.find("span", class_="percent").text.replace('%',''))  # Scrap rating
        data["loaded"] = video.find("span", class_="white").text  # Scrap loaded
        data["likes"] = video.find("span", class_="votesUp").text  # Scrap like
        data["accurate_likes"] = video.find("span", class_="votesUp")["data-rating"]  # Scrap accurate_like
        data["dislikes"] = video.find("span", class_="votesDown").text  # Scrap dislike
        data["accurate_dislikes"] = video.find("span", class_="votesDown")["data-rating"] # Scrap accurate_dislike
        data["favorite"] = video.find("span", class_="favoritesCounter").text.strip() # Scrap favorite
        data["production"] = video.find("div", class_="productionWrapper").find_all('a', class_="item")[0].text # Scrap production

        # Scrap pornstars
        pornstars = [] 
        for star in video.find_all('a', class_='pstar-list-btn'):
            pornstars.append(star.text.strip())
        data["pornstars"] = pornstars
        
        # Scrap categories
        categories = []
        for category in video.find("div", class_="categoriesWrapper").find_all('a', class_="item"):
            categories.append(category.text)
        data["categories"] = categories

        # Scrap tags
        tags = []
        for tag in video.find("div", class_="tagsWrapper").find_all('a', class_="item"):
            tags.append(tag.text)
        data["tags"] = tags

        return data

    def getVideo(self, url=None, viewkey=None, *args):
        """
        Get video informations.
        You can enter the full video url or just the viewkey
        :url: video url on phub
        :viewkey: viewkey of video
        """
        if url or viewkey:
            return self._scrapVideoInfo(self._loadPage(url=url, viewkey=viewkey))
        else:
            print('***URL or Viewkey not entered***')

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
            
            for possible_video in self._scrapLiVideos(self._loadPage(page_num=page, sort_by=sort_by)):
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