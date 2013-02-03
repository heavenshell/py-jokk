#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2

url = 'http://127.0.0.1:5000/user'
params = urllib.urlencode({'foo':1})
f = urllib2.urlopen(url, params)
print(f.getcode())
print(f.read())
