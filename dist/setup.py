#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
        name = "pyHFS",
        version="0.1",
        packages = ['hfs', 'res', 'tpl'],
        package_dir = {'hfs':'../src', 'res':'../res', 'tpl':'../tpl'},
        package_data = {
            '': [ '*.gif', '*.ico', '*.tpl' ],
        },
        include_package_data = True,
        zip_safe = False,

        description = "HTTP File Server in Python.",
        long_description = "This package provides client & server API for Feinno's RPC services.",
        author = "codelulu",
        author_email = "codelulu@gmail.com",
        url = "https://github.com/codelulu/pyHFS",

        license = "GPL",
        keywords = ("HFS, HTTP File Server, PC File Download, WP7"),
        platforms = "Linux, Macosx"
)
