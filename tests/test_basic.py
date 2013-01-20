# -*- coding: utf-8 -*-
"""
    jokk.tests.test_basic
    ~~~~~~~~~~~~~~~~~~~~~

    Basic tests for Jokk.


    :copyright: (c) 2013 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from jokk.server import Jokk
from . import TestBase, paramterized


class TestBasic(TestBase):
    def test_create_app(self):
        """ create_app() should return Jokk instance. """
        app = self._create_app('basic.json')
        self.assertTrue(isinstance(app, Jokk))

    def test_should_set_data_path(self):
        """ create_app() should read json and set data path to property. """
        app = self._create_app('basic.json')
        data_path = '../data/basic'
        config_path = os.path.dirname(self.file_path)
        path = os.path.join(config_path, data_path)

        self.assertEqual(app.data_path, path)

    @paramterized(expected=['/user', '/user/<userid>'])
    def test_should_set_url_map(self, params):
        """ URL Routings should set from json file. """
        app = self._create_app('basic.json')
        for k, v in enumerate(app.url_map.iter_rules()):
            self.assertEqual(v.rule, params['expected'][k])

    def test_get_request(self):
        """ GET /user should serve user_get.json """
        client = self._create_client('basic.json')
        res = client.get('/user')
        expected = self._read_json('basic/user_get.json')
        self.assertEqual(res.data, expected)

    def test_post_request(self):
        """ POST /user should serve user_post.json """
        client = self._create_client('basic.json')
        res = client.post('/user')
        expected = self._read_json('basic/user_post.json')
        self.assertEqual(res.data, expected)

    def test_put_request(self):
        """ PUT /user should serve user_put.json """
        client = self._create_client('basic.json')
        res = client.put('/user')
        expected = self._read_json('basic/user_put.json')
        self.assertEqual(res.data, expected)

    def test_delete_request(self):
        """ DELETE /user should serve user_put.json """
        client = self._create_client('basic.json')
        res = client.delete('/user')
        expected = self._read_json('basic/user_delete.json')
        self.assertEqual(res.data, expected)

    def test_head_request(self):
        """ HEAD /user should serve empty body. """
        client = self._create_client('basic.json')
        res = client.head('/user')
        self.assertEqual(res.data, '')

    def test_patch_request(self):
        """ PATCH /user should serve user_put.json """
        client = self._create_client('basic.json')
        res = client.patch('/user')
        expected = self._read_json('basic/user_patch.json')
        self.assertEqual(res.data, expected)

    def test_get_request_remapped(self):
        """ GET /user/<userid> should serve userid_get.json. """
        client = self._create_client('basic.json')
        res = client.get('/user/1')
        expected = self._read_json('basic/user/userid_get.json')
        self.assertEqual(res.data, expected)

    def test_post_request_remapped(self):
        """ POST /user/<userid> should serve userid_post.json. """
        client = self._create_client('basic.json')
        res = client.post('/user/1')
        expected = self._read_json('basic/user/userid_post.json')
        self.assertEqual(res.data, expected)

    def test_put_request_remapped(self):
        """ PUT /user/<userid> should serve userid_put.json. """
        client = self._create_client('basic.json')
        res = client.put('/user/1')
        expected = self._read_json('basic/user/userid_put.json')
        self.assertEqual(res.data, expected)

    def test_delete_request_remapped(self):
        """ DELETE /user/<userid> should serve userid_put.json. """
        client = self._create_client('basic.json')
        res = client.delete('/user/1')
        expected = self._read_json('basic/user/userid_delete.json')
        self.assertEqual(res.data, expected)

    def test_head_request_remapped(self):
        """ HEAD /user/<userid> should serve empty body. """
        client = self._create_client('basic.json')
        res = client.head('/user/1')
        self.assertEqual(res.data, '')

    def test_patch_request_remapped(self):
        """ PATCH /user/<userid> should serve userid_patch.json. """
        client = self._create_client('basic.json')
        res = client.patch('/user/1')
        expected = self._read_json('basic/user/userid_patch.json')
        self.assertEqual(res.data, expected)

    def test_get_status(self):
        """ GET /user should return 200. """
        client = self._create_client('basic.json')
        res = client.get('/user')
        self.assertEqual(res.status_code, 200)

    def test_custom_status_201(self):
        """ POST /user should return 201. """
        client = self._create_client('basic.json')
        res = client.post('/user')
        expected = self._read_json('basic/user_post.status')
        self.assertEqual(res.status_code, int(expected))

    def test_not_found(self):
        """ NotFound exception should be raised when url not matched. """
        from werkzeug.routing import NotFound
        client = self._create_client('basic.json')
        try:
            client.post('/foo')
        except NotFound as e:
            self.assertTrue(isinstance(e, NotFound))
