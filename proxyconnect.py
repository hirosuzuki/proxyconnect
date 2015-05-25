#!/bin/env python
# coding: utf-8

from base64 import b64encode
from httplib import HTTPConnection
from urlparse import urlparse

import os
import select
import socket
import sys

def main():

    def exit_with_mesg(message, status=-1, color=31):
        sys.stderr.write("\x1b[%sm%s\x1b[0m\n" % (color, message))
        exit(status)

    if len(sys.argv) < 3:
        exit_with_mesg("usage %s: host port [proxy_url]" % sys.argv[0])

    host, port = sys.argv[1:3]

    proxy_url = os.environ.get("http_proxy", "")

    if len(sys.argv) >= 4:
        proxy_url = sys.argv[3]

    proxy = urlparse(proxy_url)

    if proxy.hostname == None or proxy.port == None:
        exit_with_mesg("Proxy Setting Error: url=%s" % proxy_url)

    try:

        req_headers = {}

        if proxy.username or proxy.password:
            auth = b64encode(proxy.username + ":" + proxy.password)
            req_headers["Proxy-Authorization"] = "Basic " + auth

        conn = HTTPConnection(proxy.hostname, proxy.port, timeout=5)
        conn.request("CONNECT", "%s:%s" % (host, port), headers=req_headers)
        resp = conn.getresponse()

        if resp.status != 200:
            exit_with_mesg("Proxy Error: %s %s" % (resp.status, resp.reason))

        stdin, stdout = 0, 1
        proxy_socket = resp.fp.fileno()

        while True:
            read_ready = select.select([stdin, proxy_socket], [], [])[0]
            for fileno in read_ready:
                buffer = os.read(fileno, 4096)
                os.write(proxy_socket if fileno == stdin else stdout, buffer)

    except KeyboardInterrupt:
        exit_with_mesg("Keyboard Interrupt")

    except socket.error, e:
        exit_with_mesg("Socket Error: %s" % e)

if __name__ == '__main__':
    main()

