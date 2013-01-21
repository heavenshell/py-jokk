# -*- coding: utf-8 -*-
"""
    jokk.server
    ~~~~~~~~~~~

    RESTful Mock api server.

    Jokk can provide HTTP Response mock data easly.

    If you access `http://example.com/user/1` Jokk will find
    `./data/user/1_get.{json,xml,html,txt}` file and return.

    Jokk is heavily inspered by `EasyMock Server` written in Node.js.

    :copyright: (c) 2013 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import re
import argparse
import json
from string import Template
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule


class Jokk(object):
    mimetypes = [
        {'ext': 'json', 'mimetype': 'application/json'},
        {'ext': 'xml', 'mimetype': 'application/xml'},
        {'ext': 'html', 'mimetype': 'text/html'},
        {'ext': 'txt', 'mimetype': 'text/plain'}
    ]

    def __init__(self, config_path):
        """Read config.json and create routings.

        :param config_path: Path to config.json
        """
        self.config_path = config_path
        self.config = config = self.read_config(self.config_path)

        #: Routings are defined in config.json.
        self.url_map = self.create_url_map(config['routes'])

        #: Served data path's root is same as `config.json` path.
        #:
        #: .. code-block:: text
        #:
        #:   ├─config.json
        #:   └─data
        #:     └─user_get.json
        data_path = config['data'] if 'data' in config else './data'
        config_root_path = os.path.dirname(config_path)
        self.data_path = os.path.join(config_root_path, data_path)

        #: Cache `config.json`'s timestamp for auto-reloading.
        #: If `config.json` is edited after server start,
        #: you need to restart server.
        #: But it's not convenient for developer.
        #: So, `config.json` changed, reload `config.json` automatically.
        self._file_timestamp = os.path.getmtime(self.config_path)

    def read_config(self, path):
        """Read config.json and load to dict.

        :param path: Path to config.json
        """
        with open(path, 'r') as f:
            data = f.read()

            return json.loads(data)

    def create_url_map(self, routes):
        """Create url_map.

        :param routes: Routing dict
        """
        rules = []
        for route in routes:
            rules.append(Rule(route, endpoint=route, strict_slashes=False))

        return Map(rules)

    def dispatch(self, request):
        """Dispatch HTTP requests and create response.

        :param request: Werkzeug request
        """
        #: Reload config.json unless config.json modified after server start.
        file_timestamp = os.path.getmtime(self.config_path)
        if file_timestamp > self._file_timestamp:
            config = self.read_config(self.config_path)
            self.config = config
            url_map = self.create_url_map(config['routes'])
            self._file_timestamp = file_timestamp
        else:
            config = self.config

        url_map = self.url_map
        urls = url_map.bind_to_environ(request.environ)
        endpoint, args = urls.match()

        response, status, mimetype = self.create_response(request, args,
                                                          endpoint)

        #: If config.json contains `variables` assign variable to response.
        if 'variables' in config:
            template = Template(response)
            response = template.safe_substitute(**config['variables'])

        if 'jsonp' in config and config['jsonp'] is True:
            callback = request.args.get('callback', False)
            if callback:
                response = '{0}({1})'.format(callback, response)
            else:
                response = 'function({0})'.format(response)

        response = Response(response, mimetype=mimetype)
        if status is not None:
            response.status_code = status

        if 'cors' in config and config['cors'] is True:
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods',
                                 'GET,PUT,POST,DELETE,PATCH')
            response.headers.add('Access-Control-Allow-Headers',
                                 'Content-Type, Authorization')

        return response

    def create_response(self, request, params, endpoint):
        """Read response file(json,xml,html,txt), status file.

        ============== ======================
        HTTP request   JSON file.
        ============== ======================
        GET /user/1    ./data/user/1_get.json
        POST /user     ./user/post.json
        GET /user/<id> ./user/id_get.json
        HEAD /user/1   empty string
        ============== ======================

        Find response file json, xml, html, txt order.

        :param request: Request object.
        :param params:
        :param endpoint: Base response file name rule.
        """
        method = request.method.lower()

        file_name = ''
        #: http://127.0.0.1:5000/ should return `_get.json`.
        if not endpoint == '/':
            file_name = re.sub(r'[<|>]', '', endpoint.lstrip('/'))

        status_path = '{0}/{1}_{2}.{3}'.format(self.data_path, file_name,
                                               method, 'status')

        #: If `.status` file exists, read it and set to Response.status_code.
        #: Otherwise return default status_code.
        status = None
        if os.path.exists(status_path):
            with open(status_path, 'r') as f:
                status = int(f.read())

        #: `HTTP HEAD` method should return empty string.
        if method == 'head':
            return '', status, None

        exts = self.mimetypes
        response = ''
        mimetype = None
        for v in exts:
            file_path = '{0}/{1}_{2}.{3}'.format(self.data_path, file_name,
                                                 method, v['ext'])

            if os.path.exists(file_path) is False:
                continue

            with open(file_path, 'r') as f:
                data = f.read()
                #: You can use string.Template variable in response file.
                #: Template variable is like `${xxx}`.
                #: For example routing is /user/<userid>,
                #: you can use ${userid} in response file.
                #: See more detail about string.Template.
                #: http://docs.python.org/2/library/string.html#template-strings
                template = Template(data)
                response = template.safe_substitute(**params)
                mimetype = v['mimetype']
                break

        return response, status, mimetype

    def wsgi_app(self, environ, start_response):
        """Create WSGI response.

        :param environ: Environmen
        :param start_response: Response
        """
        request = Request(environ)
        response = self.dispatch(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """__call__

        :param environ: Environmen
        :param start_response: Response
        """

        return self.wsgi_app(environ, start_response)


def create_app(config_path):
    """Create wsgi app.

    If you want use another HTTP server, such as Gevent.
    import create_app function.

    >>> from gevent.wsgi import WSGIServer
    >>> from yokk.server import create_app
    >>> app = create_app('/path/to/config.json')
    >>> http_server = WSGIServer(('', 5000), app)
    >>> http_server.serve_forever()

    :param config_path: Path to config.json
    """
    app = Jokk(config_path)

    return app


def parse_option():
    """Parse options.

    =============== ========= ===============
    Options         Default   Description
    =============== ========= ===============
    -b, --bind      127.0.0.1 Mock server url
    -p, --port      5000      Port number
    -d, --debug     True      Show tracelog
    -r, --reloader  False     Auto reloader
    -s, --show_urls False     Show urls
    -c, --config    None      Config file
    =============== ========= ===============

    """
    description = 'Simple api mock server in Python.'
    parser = argparse.ArgumentParser(description=description, add_help=False)
    parser.add_argument('-b', '--bind', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=5000, type=int)
    parser.add_argument('-d', '--debug', default=True)
    parser.add_argument('-r', '--reloader', default=False)
    parser.add_argument('-s', '--show_urls', default=False, nargs='*')
    parser.add_argument('-c', '--config')

    args = parser.parse_args()

    return args


def show_urls(app):
    """Displays all of the url matching routes.

    :param app: Jokk object
    """
    rules = sorted(app.url_map.iter_rules())
    for v in rules:
        print v.endpoint


def main():
    """Main"""
    from werkzeug.serving import run_simple
    args = parse_option()
    if args.config is None:
        return
    config_path = os.path.abspath(args.config)
    app = create_app(config_path)

    if args.show_urls is not False:
        show_urls(app)
        return

    run_simple(args.bind, args.port, app, use_debugger=args.debug,
               use_reloader=args.reloader)


if __name__ == '__main__':
    main()
