# -*- coding: utf-8 -*-
"""
    jokk
    ~~~~

    RESTful mock api server.

    :copyright: (c) 2013 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages

requires = ['werkzeug']
try:
    import argparse
except:
    requires.append('argparse')

app_name = 'jokk'

description = file(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
setup(
    name=app_name,
    version='0.1',
    author='Shinya Ohyanagi',
    author_email='sohyanagi@gmail.com',
    url='http://github.com/heavenshell/py-jokk',
    description='RESTful Mock api server',
    long_description=description,
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ],
    entry_points="""
    [console_scripts]
    jokk = jokk.server:main
    """,
    tests_require=[],
    test_suite='tests'
)
