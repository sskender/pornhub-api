# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import requests
import time
import json
import re
import datetime
try:
    from urllib import urlencode
except ImportError:
    # For support Python 3
    from urllib.parse import urlencode

BASE_URL	= "https://pornhub.com"
EMBED_URL = "https://www.pornhub.com/embed/"
HEADERS         = { "Content-Type" : "text/html; charset=UTF-8" }
PHOTO_EXT       = ".jpg"                                                    # for validation
SEARCH_URL      = "/search"

PORNSTARS_URL	= "/pornstars"
PORNSTAR_URL	= "/pornstar/"                                              # for validation
MODEL_URL       = "/model/"
PORNSTAR_PHOTO	= ".phncdn.com/"                                            # for validation

VIDEOS_URL      = "/video"
VIDEO_URL	    = "/view_video.php?viewkey="                                    # for validation
VIDEO_IMAGE_URL = ".phncdn.com/videos/"                                     # for validation

ALBUMS_URL      = "/albums/"
ALBUM_URL	    = "/album/"                                                 # for validation
ALBUM_PHOTO_URL = "phncdn.com/pics/albums/"                                 # for validation
PHOTO_PREVIEW   = "/photo/"                                                 # for validation

GIFS_URL        = "/gifs"
GIF_URL         = "/gif/"
GIF_DATA_URL    = "https://dl.phncdn.com"

TIME_TO_WAIT    = 3                                                         # wait this amount in seconds before starting new threads
                                                                            # too many request in short time will result in firewall block

def isAlbum(url):
    """
    Validate album url
    www.pornhub.com/album/show_album?id=SOMENUMBERS
    """
    return True if ALBUM_URL in url else False

def isPhotoPreview(url):
    """
    Validate photo preview url
    In albums only photo preview url can be found, not the actual url
    www.pornhub.com/photo/SOMENUMBERS
    """
    return True if PHOTO_PREVIEW in url else False

def isPhoto(url):
    """
    Validate photo full url
    .pornhub.phncdn.com/pics/albums/SOMENUMBERS/SOMETEXT.jpg
    """
    return True if (ALBUM_PHOTO_URL in url) and (url[-4:] == PHOTO_EXT) else False

def isStar(url):
    """
    Validate pornstar's page
    www.pornhub.com/pornstar/SOMENAME
    """
    return True if (PORNSTAR_URL in url) or (MODEL_URL in url) else False

def isStarPhoto(url):
    """
    Validate pornstar's profile photo
    i0.cdn2a.image.pornhub.phncdn.com/pics/pornstars/SOMENUMBERS/SOMETEXT.jpg
    """
    return True if (PORNSTAR_PHOTO in url) and (url[-4:] == PHOTO_EXT) else False

def isVideo(url):
    """
    Validate video url
    www.pornhub.com/view_video.php?viewkey=SOMETEXT
    """
    return True if VIDEO_URL in url else False

def isVideoPhoto(url):
    """
    Validate video background photo
    .pornhub.phncdn.com/videos/SOMENUMBERS/SOMETEXT.jpg
    """
    return True if (VIDEO_IMAGE_URL in url) and (url[-4:] == PHOTO_EXT) else False

def isGif(url):
    """
    Validate gif url
    www.pornhub.com/gif/SOMENUMBER
    """
    return True if GIF_URL in url else False