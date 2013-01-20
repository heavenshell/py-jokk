# -*- coding: utf-8 -*-
"""
    jokk.tests.test_crossdomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Cross-Domain tests for Jokk.


    :copyright: (c) 2013 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from . import TestBase


class TestCrossdomain(TestBase):
    def _read_json(self, file_name):
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'data', 'basic', file_name)
        with open(path, 'r') as f:
            data = f.read()

            return data

    def test_jsonp_true_function(self):
        """
        Response body should contains function() when jsonp option is true.
        """
        client = self._create_client('jsonp_true.json')
        res = client.get('/user')
        data = self._read_json('user_get.json')
        self.assertEqual(res.data, 'function({0})'.format(data))

    def test_jsonp_true_callback(self):
        """
        Response body should contain callback() when jsonp option is true.
        """
        client = self._create_client('jsonp_true.json')
        res = client.get('/user?callback=callback')
        data = self._read_json('user_get.json')
        self.assertEqual(res.data, 'callback({0})'.format(data))

    def test_jsonp_false(self):
        """
        Response body should not contains any callback when jsonp is false.
        """
        client = self._create_client('jsonp_false.json')
        res = client.get('/user')
        data = self._read_json('user_get.json')
        self.assertEqual(res.data, data)

    def test_cors_true(self):
        """
        Response should contains CORS headers when cors option is true.
        """
        client = self._create_client('cors_true.json')
        res = client.get('/user')
        self.assertEqual(res.headers.get('Access-Control-Allow-Origin'), '*')
        self.assertEqual(res.headers.get('Access-Control-Allow-Methods'),
                         'GET,PUT,POST,DELETE,PATCH')
        self.assertEqual(res.headers.get('Access-Control-Allow-Headers'),
                         'Content-Type, Authorization')

    def test_cors_false(self):
        """
        Response should not contains CORS headers when cors option is false.
        """
        client = self._create_client('cors_false.json')
        res = client.get('/user')
        self.assertFalse('Access-Control-Allow-Origin' in res.headers)
        self.assertFalse('Access-Control-Allow-Methods' in res.headers)
        self.assertFalse('Access-Control-Allow-Headers' in res.headers)
