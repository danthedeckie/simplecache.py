#!/usr/bin/python
'''
    simplecache.py - (C) 2014 Daniel Fairhead <daniel.fairhead@.om.org>
        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
            ---------------------------------
    A very simple python proxy which routes all GET requests to another server,
    and caches the results as simple flat files, which it stores indefinately.

    This is often really useful when prototyping and debugging slow services.
    If you want to use it in production (be careful!!) for anything, make sure
    it's only public facing with a good revese proxy such as nginx in front of
    it, and it's probably a good idea to create a cron job or something to daily
    flush the cache.
    ---------------------------------
    usage:

    python simpleserver.py <other_site>
'''

import SimpleHTTPServer
import SocketServer
import urllib
from os import makedirs
from os.path import dirname, join as pathjoin, exists
import sys
#pylint: disable=too-many-public-methods

PORT = 8080
CACHEDIR = pathjoin(dirname(__file__), 'cache')


class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    ''' simple proxy to another server '''
    def do_GET(self):
        cached_url = pathjoin(CACHEDIR, self.path[1:])

        if not exists(cached_url):
            if not exists(dirname(cached_url)):
                makedirs(dirname(cached_url))
            print 'Live', cached_url
            urllib.urlretrieve(REAL + self.path, cached_url)
        else:
            print 'Cached', cached_url

        if exists(cached_url):
            self.copyfile(urllib.urlopen(cached_url), self.wfile)
        else:
            print 'Does not exist!'
            self.send_error(404)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Usage:'
        print 'python simplecache.py <server to proxy to...>'
        exit(0)

    REAL = sys.argv[1]
    if not ':' in REAL:
        REAL = 'http://' + REAL

    SERVER = SocketServer.TCPServer(("", PORT), Proxy)

    print "serving on port:", PORT

    SERVER.serve_forever()
