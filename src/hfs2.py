"""HFS ( HTTP File Server)

http://www.rejetto.com/hfs/.

It's based on Simple HTTP Server.

"""

__author__ = 'codelulu@gmail.com'
__version__ = "0.1"
__all__ = ["HTTPFileServerRequestHandler"]

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import sys
import shutil
import mimetypes
import time
import datetime
import socket
import tarfile
import tempfile

from stat import *
from hfs_template import *
from hfs_util import *

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

__dir__ = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

class HTTPFileServerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    server_version = "2.2f"
    uptime = time.time()
    dl_count = {}

    def inc_dl_count(self, name):
        if name not in self.dl_count:
            self.dl_count[name] = 1
        else:
            self.dl_count[name] += 1

    def get_dl_count(self, name):
        if name in self.dl_count:
            return self.dl_count[name]

        return 0

    def get_query(self, name):
        pos = self.path.find('?')
        if pos == -1:
            return None

        query = self.path[pos + 1:]
        queries = query.split('&')
        for segment in queries:
            pair = segment.split('=')
            if pair[0] == name:
                if len(pair) > 1:
                    return pair[1]
                else:
                    return True

        return None

    def do_GET(self):
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        f = self.send_head()
        if f:
            f.close()

    def response_string(self, data, mimetype = 'text'):
        f = StringIO()
        f.write(data)

        length = f.tell()
        f.seek(0)

        self.send_response(200)

        if mimetype == 'text':
            encoding = sys.getfilesystemencoding()
            self.send_header("Content-type", "text/plain; charset=%s" % encoding)
        elif mimetype == 'html':
            encoding = sys.getfilesystemencoding()
            self.send_header("Content-type", "text/html; charset=%s" % encoding)
        elif mimetype == 'tar':
            self.send_header("Content-type", 'application/x-tar')
        else:
            self.send_header("Content-type", 'application/octet-stream')

        self.send_header("Content-Length", str(length))
        self.end_headers()

        return f

    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if '?' not in self.path and not self.path.endswith('/'):
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            else:
                return self.list_directory(path)

        basename = os.path.basename(path)
        dirname = os.path.dirname(path)

        if basename == '~files.lst':
            return self.list_files(path)
        elif basename == '~folder.tar':
            return self.tar_folder(path)

        ctype = self.guess_type(path)

        if self.path[:5] == '/~img':
            path = __dir__ + '/../res/' + basename[1:] + '.gif'
        elif self.path == '/favicon.ico':
            path = __dir__ + '/../res/favicon.ico'

        try:
            f = open(path, 'rb')
            self.inc_dl_count(path)
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def tar_folder(self, path):
        dirname = os.path.dirname(path)
        recursive = self.get_query('recursive')
        base_path = os.path.dirname(path)

        all_files = []
        def list_dir(dirroot):
            try:
                files = os.listdir(dirroot)
                for filename in files:
                    if filename[:1] == '.':
                        continue

                    fullname = os.path.join(dirroot, filename)
                    if os.path.isdir(fullname):
                        if recursive:
                            all_files.append(fullname)
                            list_dir(fullname)
                    else:
                        all_files.append(fullname)

            except os.error:
                self.send_error(404, "No permission to list directory")
                return None

        list_dir(base_path)

        tmpf = tempfile.NamedTemporaryFile(delete = False)
        tmpfname = tmpf.name
        tmpf.close()

        tar = tarfile.open(name = tmpfname, mode = 'w')
        offset = len(dirname) + 1
        for f in all_files:
            arcname = f[offset:]
            tar.add(f, arcname = arcname)
        tar.close()

        f = open(tmpfname, 'r')
        data = f.read()
        f.close()

        os.unlink(tmpfname)

        return self.response_string(data, 'tar')

    def get_host(self):
        host = getattr(self, 'host', '')
        if host == '':
            ip, port = self.server.socket.getsockname()
            if ip == '0.0.0.0':
                ip = get_lan_ip()

            if port != 80:
                host = ip + ':' + str(port)
                
            self.host = host

        return host

    def list_files(self, path):
        recursive = self.get_query('recursive')
        base_path = os.path.dirname(path)
        base_url = os.path.dirname(self.vpath)
        host = self.get_host()

        all_files = []
        def list_dir(dirroot, urlroot):
            try:
                files = os.listdir(dirroot)
                for filename in files:
                    if filename[:1] == '.':
                        continue

                    if urlroot[-1] != '/':
                        fullurl = urlroot + '/' + filename
                        urlroot += '/'
                    else:
                        fullurl = urlroot + filename

                    fullname = os.path.join(dirroot, filename)

                    if os.path.isdir(fullname):
                        if recursive:
                            list_dir(fullname, fullurl)
                    else:
                        item = { 'dir': urlroot, 'name': filename }
                        all_files.append(item)
                
            except os.error:
                self.send_error(404, "No permission to list directory")
                return None

        list_dir(base_path, base_url)

        t = HFS_Template(__dir__ + '/../tpl/filelist.tpl')
        txtList = ''
        for f in all_files:
            txtFile = t['file']
            txtFile = txtFile.replace('%host%', host)
            txtFile = txtFile.replace('%encoded-folder%', f['dir'])
            txtFile = txtFile.replace('%item-url%', f['name'])

            txtList += txtFile

        txtFiles = t['files']
        txtFiles = txtFiles.replace('%list%', txtList)

        txt = t['']
        txt = txt.replace('%files%', txtFiles).strip()

        return self.response_string(txt, 'text')

    def list_cmp_weight(self, path, sortField):
        modeWeight = 0
        stat = os.stat(path)
        mode = stat.st_mode

        if S_ISDIR(mode):
            modeWeight = 2
        elif S_ISLNK(mode):
            modeWeight = 1
        else:
            modeWeight = 0

        if sortField == 's':
            return modeWeight, stat.st_size
        elif sortField == 't':
            return modeWeight, - stat.st_mtime
        elif sortField == 'd':
            return modeWeight, - self.get_dl_count(path)
        else:
            return modeWeight, os.path.basename(path)

    def list_directory(self, path):
        buildTime = time.time()

        try:
            list = os.listdir(path)
            self.inc_dl_count(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        newlist = []
        for item in list:
            if item[0] != '.':
                newlist.append(item)

        list = newlist
        
        sortField = self.get_query('sort')

        def list_cmp(patha, pathb):
            modea, fielda = self.list_cmp_weight(os.path.join(path, patha), sortField)
            modeb, fieldb = self.list_cmp_weight(os.path.join(path, pathb), sortField)
            if modea != modeb:
                return modeb - modea

            if fielda.__class__ != int:
                if fielda > fieldb:
                    return 1
                elif fielda < fieldb:
                    return -1
                else:
                    return 0
            else:
                return fielda - fieldb

        list.sort(cmp = list_cmp)

        displaypath = self.vpath
        upload_link = False
        folder_comment = ''
        user = ''
        
        t = HFS_Template(__dir__ + '/../tpl/default.tpl')

        txt = t['']
        txt = txt.replace('%style%', t['style'])
        txt = txt.replace('%folder%', displaypath)
        txt = txt.replace('%login-link%', t['login-link'])
        if user != '':
            txt = txt.replace('%loggedin%', t['loggedin'].replace('%user%', user))
        else:
            txt = txt.replace('%loggedin%', '')
        if upload_link:
            txt = txt.replace('%upload-link%', t['upload-link'])
        else:
            txt = txt.replace('%upload-link%', '')
        txt = txt.replace('%folder-comment%', '')
        if displaypath != '/':
            txt = txt.replace('%up%', t['up'])
        else:
            txt = txt.replace('%up%', '')

        number_folders = 0
        number_files = 0
        total_size = 0
        txt_lists = ''

        for name in list:
            fullname = os.path.join(path, name)
            linkname = name

            if os.path.isdir(fullname):
                linkname = name + '/'
                number_folders += 1
                txt_list = t['folder']
            elif os.path.islink(fullname):
                number_files += 1
                txt_list = t['link']
            else:
                number_files += 1
                txt_list = t['file']
                size = os.path.getsize(fullname)
                total_size += size
                txt_list = txt_list.replace('%item-size%', smart_size(size))
            
            txt_list = txt_list.replace('%new%', '')
            txt_list = txt_list.replace('%protected%', '')
            txt_list = txt_list.replace('%item-url%', urllib.quote(linkname))
            txt_list = txt_list.replace('%item-name%', name)
            txt_list = txt_list.replace('%comment%', '')
            txt_list = txt_list.replace('%item-modified%', str(datetime.datetime.fromtimestamp(int(os.path.getmtime(fullname)))))
            txt_list = txt_list.replace('%item-dl-count%', str(self.get_dl_count(fullname)))

            txt_lists += txt_list

        txt_files = t['files']
        txt_files = txt_files.replace('%number-folders%', str(number_folders))
        txt_files = txt_files.replace('%number-files%', str(number_files))
        txt_files = txt_files.replace('%total-size%', smart_size(total_size))
        txt_files = txt_files.replace('%archive%', t['archive'])
        txt_files = txt_files.replace('%list%', txt_lists)

        txt = txt.replace('%files%', txt_files)
        txt = txt.replace('%version%', self.server_version)
        now = time.time()

        txt = txt.replace('%timestamp%', str(datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')))
        uptime = int(time.time() - self.uptime)
        uptime = '%02d:%02d:%02d' % (uptime / 3600, (uptime / 60) % 60, uptime % 60) 
        txt = txt.replace('%uptime%', uptime)
        txt = txt.replace('%build-time%', '%0.3f' % (now - buildTime))

        return self.response_string(txt, 'html')

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        self.vpath = path

        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types

    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
            '': 'application/octet-stream', # Default
            '.tpl': 'text/plain',
            '.py': 'text/plain',
            '.c': 'text/plain',
            '.h': 'text/plain',
            })


def test(HandlerClass = HTTPFileServerRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
