.. Jokk documentation master file, created by
   sphinx-quickstart on Sat Jan 19 17:59:59 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Jokk's documentation!
================================

What is Jokk?
-------------

RESTful mock api server.

`Jokk` can provide HTTP Response mock data easly.

.. code-block:: text

  GET  /user/1 => user/1_get.json
  POST /user/1 => user/1_post.json

`Jokk` is heavily inspiered by `EasyMock <https://github.com/cyberagent-jp/node-easymock>`_.

Naming of `Jokk` is inspiered by `JokkMokk <http://en.wikipedia.org/wiki/Jokkmokk>`_ because pronunciation is similar to `Mock`.


- `Repository <https://github.com/heavenshell/py-jokk/>`_
- `Documentation <https://jokk.readthedocs.org/en/latest/>`_

Installation
------------

.. code-block:: sh

  $ virtualenv --distribute jokk_sample
  $ source jokk_sample/bin/activate
  $ cd jokk_sample
  $ pip install jokk

`Jokk` depends on `Werkzeug <http://werkzeug.pocoo.org>`_ using for WSGI Utility Library.

Usage
-----

1. Create `config.json` for configure settings such as routes, variables
2. Create `data` directory for serve response files
3. Put response file into `data` directory
4. Start Jokk server

.. code-block:: sh

  $ jokk -c config.json

5. Access to jokk server client such as Web browser.
6. Jokk would return response file

Configure settings
------------------

Configure settings like below.

.. code-block:: json

  {
    "data": "./data",
    "jsonp": true,
    "cors": true,
    "routes": [
      "/user",
      "/user/<userid>"
      "/user/<userid>/show"
    ],
    "variables" : {
      "server": "http://example.com"
    }
  }

=============== ===================================================
Key             Value
=============== ===================================================
data            Path to data directory for serve response file
jsonp           Enable to use JSONP
cors            Enable to use Cross-Origin Resource Sharing
routes          Routes to serve response file
variables       Enable to assign setting key-value to response body
=============== ===================================================

data
^^^^
Defined relative path from `config.json`.

For example, if you defined `./data` in `config.json`, directory structors should be like following.

.. code-block:: text

  ├─config.json
  └─data
     └─user_get.json
     └─user
       ├─userid_get.json
       └─userid_post.json

JSONP and CORS
^^^^^^^^^^^^^^

`jsonp` and `cors(Cross-Origin Resource Sharing)` are for cross domain access.

- When `jsonp` value is true, response body would add callback method.
- When `cors` value is true, response header would add following header.

============================ ===========================
Header name                  Header value
============================ ===========================
Access-Control-Allow-Origin  `*`
Access-Control-Allow-Methods GET,PUT,POST,DELETE,PATCH
Access-Control-Allow-Headers Content-Type, Authorization
============================ ===========================

routes
^^^^^^
Routes for serve response file.
When url rules matched, Jokk will search response file and status file.

=================== =========================
Rules               Response file path
=================== =========================
/                   ./data/_get.json
/user               ./data/user_get.json
/user/<userid>      ./data/userid_get.json
/user/<userid>/<id> ./data/userid/id_get.json
=================== =========================

Convention of file name is following.

.. code-block:: text

  Url rules + '_' + HTTP method + {.json,.xml,.html,txt}
  Url rules + '_' + HTTP method + .status

=========== ======== ====================
HTTP method rutes    response file name
=========== ======== ====================
GET         /items/1 items/1_get.json
POST        /items/1 items/1_post.json
PUT         /items/1 items/1_put.json
DELETE      /items/1 items/1_delete.json
PATCH       /items/1 items/1_patch.json
HEAD        /items/1 [#f1]_
=========== ======== ====================

.. [#f1] HEAD method returns empty response body.

Status file
~~~~~~~~~~~

If you want to send custom status code, put status file such as `item/1_get.stasus` into same directory as response file.

In status file you just put integer value like following.

.. code-block:: text

  201

Response file types
~~~~~~~~~~~~~~~~~~~

Following response file types are available.

========= ================
File type MimeType
========= ================
json      application/json
xml       application/xml
html      text/html
text      text/plain
========= ================

Variable Rules
~~~~~~~~~~~~~~
To add variable parts to a URL you can mark these special sections as <variable_name> and the given name will be available as a variable.

For example, routes defined such as `/user/<userid>` in `config.json`, and call  `GET /user/1234` would be mapped to  `./data/user/userid_get.json`.

You can write variable in response file.

.. code-block:: json

  {
    "userid": "${userid}"
  }

Above response would be replaced to following.

.. code-block:: json

  {
    "userid": "1234"
  }


variables
^^^^^^^^^
If you define `variables` in `config.json`, you can use in response file.

.. code-block:: json

  {
    "variables" : {
      "server": "http://example.com"
    }
  }

Define response file like following.

.. code-block:: json

  {
    "server": "${server}"
  }

Response body would be replaced like following.

.. code-block:: json

  {
    "server": "http://example.com"
  }


API
---

.. autoclass:: jokk.server.Jokk
  :members:

.. autoclass:: jokk.server.parse_option
  :members:

.. autoclass:: jokk.server.show_urls
  :members:

ChangeLog
---------

.. include:: ../../CHANGES.rst

Contributing
------------
1. Fork it
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request


.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

