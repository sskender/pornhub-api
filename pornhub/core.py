# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from urllib import urlencode
from threading import Thread
from queue import Queue
import requests
import time


BASE_URL	= "http://pornhub.com"
HEADERS         = { "Content-Type" : "text/html; charset=UTF-8" }
PHOTO_EXT       = ".jpg"                                                    # for validation

PORNSTARS_URL	= "/pornstars"
PORNSTAR_URL	= "/pornstar/"                                              # for validation
PORNSTAR_PHOTO	= "image.pornhub.phncdn.com/pics/pornstars/"                # for validation

VIDEOS_URL      = "/video/search?"
VIDEO_URL	= "/view_video.php?viewkey="                                # for validation
VIDEO_IMAGE_URL = "image.pornhub.phncdn.com/videos/"                        # for validation

ALBUMS_URL      = "/albums/"
ALBUM_URL	= "/album/show_album?id="                                   # for validation
ALBUM_PHOTO_URL = "image.pornhub.phncdn.com/pics/albums/"                   # for validation
PHOTO_PREVIEW   = "/photo/"                                                 # for validation

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
    i1.cdn2b.image.pornhub.phncdn.com/pics/albums/SOMENUMBERS/SOMETEXT.jpg
    """
    return True if (ALBUM_PHOTO_URL in url) and (url[-4:] == PHOTO_EXT) else False

def isStar(url):
    """
    Validate pornstar's page
    www.pornhub.com/pornstar/SOMENAME
    """
    return True if PORNSTAR_URL in url else False

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
    i0.cdn2b.image.pornhub.phncdn.com/videos/SOMENUMBERS/SOMETEXT.jpg
    """
    return True if (VIDEO_IMAGE_URL in url) and (url[-4:] == PHOTO_EXT) else False
