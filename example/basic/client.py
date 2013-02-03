#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

def get(url):
    f = urllib.urlopen(url)
    print(f.getcode())
    print(f.read())
    print('-' * 80)

get('http://127.0.0.1:5000')

get('http://127.0.0.1:5000/user/foo')

get('http://127.0.0.1:5000/user/foo/profile')

get('http://127.0.0.1:5000/user/foo/inbox/100')
