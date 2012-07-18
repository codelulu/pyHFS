pyHFS
==========
A simple HTTP File Server(2.2f) implemented in python. 

It's mainly used for running in MacOSX / Linux as a HFS server to assist in <b>PC File Download</b> in WP7.

It contains only a few simple functions (compared to http://www.rejetto.com/hfs/), 
    such as browsing, downloading, file-listing, folder-tarring.

The implementatinon is modified from SimpleHTTPServer.

Emmmm, running in MacOSX will be tested later.


build, install, uninstall, run
==============================
build:

    $ make

  python-setuptools is necessary.

install:

    $ sudo make install

  python-setuptools is necessary.

uninstall:

    $ sudo make uninstall

  python-pip is necessary.

run:

    $ python -m hfs.hfs2 [ port ]

  or in the pyHFS's dir:

    $ python src/hfs2.py


License
=========
GPLv2.

pyHFS comes with ABSOLUTELY NO WARRANTY.

The files in the directory tpl and res:

    GPLv2, Copyright (C) 2002-2008  Massimo Melina (www.rejetto.com).


HTTP File Server
================
http://www.rejetto.com/hfs/

