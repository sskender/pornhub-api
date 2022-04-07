# -*- coding: UTF-8 -*-

from .core import *

class Stars(object):

    def __init__(self, ProxyDictionary, *args, **kwargs):
        self.ProxyDictionary = ProxyDictionary
        self.stars_sort = kwargs

    def _sortStars(self, sort_by):
        sort_dict = dict()

        if not sort_by:
            return sort_dict
        
        sort_keys = sort_by.keys()

        if "sort_by" in sort_keys:
            orders = {"popular" : "mp", "view": "mv", "trend": "t", "subs": "ms", "alpha": "a", "videos": "nv", "random": "r"}

            for key in orders:
                if key in sort_by["sort_by"].lower():
                    sort_dict["o"] = orders[key]

                    if key == "alpha" and "letter" in sort_keys:
                        sort_dict["l"] = sort_by["letter"]
        
        if "period" in sort_keys:
            periods = {"week": "w", "month": "m", "year": "a"}
            for key in periods:
                if key in sort_by["period"].lower():
                    sort_dict["t"] = periods[key]

        if "p_type" in sort_keys:
            s_type = sort_by["p_type"].lower()
            if "star" in s_type:
                sort_dict["performerType"] = "pornstar"
            elif "model" in s_type or "amateur" in s_type:
                sort_dict["performerType"] = "amateur"

        return sort_dict
    
    def _craftStarsPage(self, page_num):
        payload = dict()
        if self.stars_sort:
            stars_sort = self._sortStars(self.stars_sort)
            for key in stars_sort:
                payload[key] = stars_sort[key]
        
        payload["page"] = page_num
        return payload
        
    def _loadStarsPage(self, page_num=None, url=None):
        if url:
            r = requests.get(url, headers=HEADERS, proxies=self.ProxyDictionary)
        else:
            r = requests.get(BASE_URL + PORNSTARS_URL, params=self._craftStarsPage(page_num), headers=HEADERS, proxies=self.ProxyDictionary)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _scrapLiStars(self, soup_data):
        # get div with list of stars (month popular is the 1st)
        div_el = soup_data.findAll("div", { "class" : "sectionWrapper", "id" : "pornstarsFilterContainer" } )[0]
        # get each porn star info (held in list block)
        li_el = div_el.find_all("li")
        
        return li_el

    def _scrapStarsInfo(self, li_el):
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
        for span_tag in li_el.find_all("span", {"class": "rank_number"}):
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
        for span_tag in li_el.find_all("span", {"class": "modelBadges"}):

            if span_tag.find_all("i", {"class": "verifiedIcon"}):
                data["verified"] = True

            if span_tag.find_all("i", {"class": "trophyPornStar"}):
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

    def _newFormatPage(self, div):
        # info, socials
        data = dict()
        data["photo"] = div.find("img", {"id": "getAvatar"}).attrs["src"]
        data["cover"] = div.find("img", {"id": "coverPictureDefault"}).attrs["src"]
        data["subs"] = div.find("div", {"data-title": re.compile("Subscribers:")}).span.text.strip()

        # scrap about pstar
        if div.find("div", {"itemprop": "description"}):
            data["about"] = div.find("div", {"itemprop": "description"}).text.strip()
        # scrap about model
        else:
            about = div.find("section", {"class": "aboutMeSection"})
            if about.find("div", class_=False):
                data["about"] = about.find("div", class_=False).text.strip()
        
        # scrap infos
        try:
            infos = dict()
            for info in div.find_all("div", {"class": "infoPiece"}):
                key = info.find("span", class_=False).text.strip().replace(":", "")
                infos[key] = info.find("span", {"class": "smallInfo"}).text.strip()
            data["infos"] = infos
        except Exception as e:
                pass
        
        # scrap social
        try:
            socials = dict()
            for social in div.find("ul", {"class": "socialList"}).find_all("li"):
                soc = social.find("a")
                socials[soc.text.strip()] = soc["href"]
            data["socials"] = socials
        except Exception as e:
                pass
        
        return data
        
    def _oldFormatPage(self, div):
        
        data = dict()
        data["photo"] = div.find("div", {"class": "thumbImage"}).find("img").attrs["src"]
        
        # scrap about
        try:
            data["about"] = div.find("div", {"class": "longBio"}).text.strip().replace(">", "")
        except Exception as e:
                pass

        # scrap subs
        for el in div.find_all("div", {"class": "infoBox"}):
            if "subscribers" in el.div.text.strip().lower():
                data["subs"] = el.span.text.strip()
        
        # scrap infos
        try:
            infos = dict()
            for info in div.find_all("div", {"class": "infoPiece"}):
                key = info.find("span").text.strip().lower().replace(":", "")
                if "website" in key:
                    infos[key] = info.find("a").attrs["href"]
                else:
                    infos[key] = info.contents[1].strip()
            data["infos"] = infos
        except Exception as e:
                pass
        
        return data

    def _scrapStarInfo(self, bs):
        data = {
            "name"              : None,     # string
            "rank"              : None,     # integer
            "ranks"             : None,     # dict
            "type"              : None,     # string
            "videos"            : None,     # integer
            "views"             : None,     # string
            "accurate_views"    : None,     # integer
            "verified"          : False,    # bool
            "trophy"            : False,    # bool
            "url"               : None,     # string
            "photo"             : None,     # string
            "cover"             : None,     # string
            "subs"              : None,     # string
            "about"             : None,     # string
            "infos"             : None,     # dict
            "socials"           : None,     # dict
            "geo_block"         : False     # bool
        }

        data["url"] = bs.find("head").find("link", {"rel": "canonical"}).attrs["href"]
        data["name"] = re.findall(r"(model/|pornstar/)(\S+)", data["url"])[0][1].replace("-", " ").title()
        
        # scrap type
        if "pornstar" in data["url"]:
            data["type"] = "pornstar"
        else:
            data["type"] = "model"

        # check geo block of page
        if bs.find("div", {"class": "geoBlocked"}):
            data["geo_block"] = True
            return data

        # scrap ranks
        ranks = dict()
        for rank in bs.find("div", {"class": "rankingInfo"}).find_all("div", {"class": "infoBox"}):
            ranks[rank.find("div").text.strip()] = rank.find("span").text.strip()
        data["ranks"] = ranks
        data["rank"] = list(ranks.values())[0]

        # scrap badges
        if bs.find("span", {"class": "verifiedPornstar"}):
            data["verified"] = True
        if bs.find("span", {"class": "trophyPornStar"}):
            data["trophy"] = True

        # scrap videos number
        data["videos"] = 0
        for div_el in bs.find_all("div", {"class": "pornstarVideosCounter"}):
            data["videos"] += int(div_el.text.strip().split("of")[1])
        
        data["views"] = bs.find("div", {"class": "videoViews"}).span.text.strip()
        data["accurate_views"] = int("".join(re.findall(r"\d+", bs.find("div", {"class": "videoViews"}).attrs["data-title"])))

        # scrap photo, cover, subs, about, info, socials
        if bs.find("div", class_="withCover"):
            div_data = self._newFormatPage(bs.find("div", {"class": "withCover"}))
        else:
            div_data = self._oldFormatPage(bs.find("div", {"class": "withThumb"}))
        for key in div_data:
            data[key] = div_data[key]
        
        return data

    def getStar(self, url):
        
        if isStar(url):
            return self._scrapStarInfo(self._loadStarsPage(url=url))
        else:
            raise ValueError("Wrong URL")

    def getStars(self, quantity=1, page=1, full_data=False, infinity=False, **sort_dict):
        """
        Get pornstar's basic informations.

        :param quantity: number of pornstars to return
        :param page: starting page number
        :param infinity: never stop downloading
        """
        if sort_dict:
            self.stars_sort.update(sort_dict)

        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0

        while True:

            for possible_star in self._scrapLiStars(self._loadStarsPage(page_num=page)):
                data_dict = self._scrapStarsInfo(possible_star)

                if data_dict:
                    if full_data:
                        yield self.getStar(data_dict["url"])
                    else:
                        yield data_dict

                    if not infinity:
                        found += 1
                        if found >= quantity: return

            page += 1
