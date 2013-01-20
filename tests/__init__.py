# -*- coding: utf-8 -*-
"""
    jokk.tests
    ~~~~~~~~~~

    Basic tests for Jokk.


    :copyright: (c) 2013 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from unittest import TestCase
from functools import wraps
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from jokk.server import create_app


def paramterized(**kwargs):
    def _paramterized_test(func):
        @wraps(func)
        def __paramterized_test(*args):
            func(args[0], kwargs)
            return func
        return __paramterized_test
    return _paramterized_test


class TestBase(TestCase):
    def setUp(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))

    def _read_json(self, file_name):
        file_path = os.path.join(self.root_path, 'data', file_name)
        with open(file_path, 'r') as f:
            data = f.read()
            return data

    def _create_app(self, file_name):
        root_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(root_path, 'configs', file_name)
        self.file_path = file_path
        app = create_app(file_path)

        return app

    def _create_client(self, file_name):
        app = self._create_app(file_name)
        client = Client(app, BaseResponse)

        return client
