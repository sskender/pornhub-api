# -*- coding: UTF-8 -*-

"""
    pornhub
    ----------
    PornHub Unofficial API for Python (2.7) + (Also works with Python 3.5)

    :copyright: (c) 2016 by Sven Skender
"""


from .core import *
from .stars import Stars
from .videos import Videos
from .photos import Photos   

class PornHub(Stars, Videos, Photos):
    def __init__(self, ProxyIP=None, ProxyPort=None, keywords=[], *args):
        self.setProxyDictionary(ProxyIP, ProxyPort)

        Stars.__init__(self, self.ProxyDictionary, *args)
        Videos.__init__(self, self.ProxyDictionary, keywords=keywords, *args)
        Photos.__init__(self, self.ProxyDictionary, keywords=keywords, *args)

    def setProxyDictionary(self, ProxyIP, ProxyPort):
        if ProxyIP == None or ProxyPort == None:
            self.ProxyDictionary = {}
        else:
            Address = "://" + ProxyIP + ":" + str(ProxyPort)
            self.ProxyDictionary = { "http"  : "http" + Address, "https" : "https" + Address } 



__copyright__   = "Copyright 2016 by Sven Skender"
__authors__      = ["Sven Skender", "Ibrahim Ipek"]
__source__      = "https://github.com/sskender/pornhub-api/"
__license__     = "MIT"

__all__ = ["PornHub",]