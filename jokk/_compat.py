# -*- coding: utf-8 -*-
"""
    jokk.compat
    ~~~~~~~~~~~

    Compatible to Python2.6,2.7 and Python3.3

    This module is copyed from Werkzeug's `_compat.py`.

    https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/_compat.py

    :copyright: (c) 2013 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys

PY2 = sys.version_info[0] == 2


if PY2:
    text_type = unicode
else:
    text_type = str


def to_unicode(x, charset=sys.getdefaultencoding(), errors='strict',
               allow_none_charset=False):
    if x is None:
        return None
    if not isinstance(x, bytes):
        return text_type(x)
    if charset is None and allow_none_charset:
        return x
    return x.decode(charset, errors)
