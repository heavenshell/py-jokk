Jokk
====

RESTful mock api server.

`Jokk` is heavily inspiered by `EasyMock <https://github.com/cyberagent-jp/node-easymock>`_.

.. image:: https://travis-ci.org/heavenshell/py-jokk.png?branch=master

- `Repository <https://github.com/heavenshell/py-jokk/>`_
- `Documentation <https://jokk.readthedocs.org/en/latest/>`_

Installation
------------

::

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

::

  $ jokk -c config.json

5. Access to jokk server client such as Web browser.
6. Jokk would return response file

Options
-------

See documantaion.


Contributing
------------
1. Fork it
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

