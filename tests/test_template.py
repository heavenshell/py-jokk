# -*- coding: utf-8 -*-
"""
    jokk.tests.test_template
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Template tests for Jokk.


    :copyright: (c) 2014 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import json
from jokk._compat import to_unicode
from . import TestBase


class TestTemplate(TestBase):
    def test_url_var_remapped(self):
        """ Routes /<userid> remapped to /userid. """
        client = self._create_client('template.json')
        res = client.get('/foo')
        self.assertEqual(res.status_code, 200)

    def test_url_var_assign_to_response_file(self):
        """ Routes /<userid> url vars should assing to response body. """
        client = self._create_client('template.json')
        res = client.get('/foo')
        text = json.loads(to_unicode(res.data))['message']
        self.assertEqual(text, 'foo')

    def test_variable_assign_to_response_file(self):
        """ Variables should assign to response body. """
        client = self._create_client('template.json')
        res = client.get('/template')
        text = json.loads(to_unicode(res.data))['server']
        self.assertEqual(text, 'http://example.com')
