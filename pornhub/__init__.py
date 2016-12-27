# -*- coding: UTF-8 -*-

"""
    pornhub
    ----------
    PornHub Unofficial API for Python (2.7)

    :copyright: (c) 2016 by Sven Skender
"""


from .core import *
from .stars import Stars
from .videos import Videos
from .photos import Photos

class PornHub(Stars, Videos, Photos):
    def __init__(self, keywords=[], *args):
        Stars.__init__(self, *args)
        Videos.__init__(self, keywords=keywords, *args)
        Photos.__init__(self, keywords=keywords, *args)



__copyright__   = "Copyright 2016 by Sven Skender"
__author__      = "Sven Skender"
__source__      = "https://github.com/sskender/pornhub-api/"
__license__     = "MIT"

__all__ = ["PornHub",]