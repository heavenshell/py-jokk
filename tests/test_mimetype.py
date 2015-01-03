# -*- coding: utf-8 -*-
"""
    jokk.tests.test_mimetype
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Mimetype tests for Jokk.


    :copyright: (c) 2014-2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from . import TestBase


class TestMimetype(TestBase):
    def test_mimetype_json(self):
        """ json response's Content-Type should be application/json. """
        client = self._create_client('mimetype.json')
        res = client.get('/json')
        self.assertEqual(res.headers.get('Content-Type'), 'application/json')

    def test_mimetype_xml(self):
        """ xml response's Content-Type should be application/xml. """
        client = self._create_client('mimetype.json')
        res = client.get('/xml')
        self.assertEqual(res.headers.get('Content-Type'),
                         'application/xml; charset=utf-8')

    def test_mimetype_html(self):
        """ html response's Content-Type should be text/html. """
        client = self._create_client('mimetype.json')
        res = client.get('/html')
        self.assertEqual(res.headers.get('Content-Type'),
                         'text/html; charset=utf-8')

    def test_mimetype_txt(self):
        """ txt response's Content-Type should be text/plain. """
        client = self._create_client('mimetype.json')
        res = client.get('/txt')
        self.assertEqual(res.headers.get('Content-Type'),
                         'text/plain; charset=utf-8')
