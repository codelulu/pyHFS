#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
        name = "pyHFS",
        version="0.1",
        packages = ['hfs'],
        package_dir = {'hfs':'../src' },
        zip_safe = False,

        description = "HTTP File Server in Python.",
        long_description = "This package provides client & server API for Feinno's RPC services.",
        author = "codelulu",
        author_email = "codelulu@gmail.com",

        license = "GPL",
        keywords = ("HFS, HTTP File Server, PC File Download, WP7"),
        platforms = "Linux, Macosx",
        url = "",
)
