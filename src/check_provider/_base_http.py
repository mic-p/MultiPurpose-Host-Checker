# -*- coding: UTF-8 -*-

import ssl
import http.client as http_client
from urllib.parse import urlparse
import socket

import libs.constants as C

def do_get_reply(host, address, msg_err):
    """"""
    # verify if we need to connect with the S version of http
    if host.specific_config.use_https:
        f = http_client.HTTPSConnection
        prefix = "https://"
    else:
        f = http_client.HTTPConnection
        prefix = "http://"

    # connect
    if not address.startswith("http"):
        address = prefix + address
    
    # clean address
    addr = urlparse(address)
    
    conn = f(addr.netloc)
    error_found = 0
    try:
        conn.request("GET", addr.path or "/")
    except ssl.SSLCertVerificationError:
        error_found = 1
        err_type = "SSL error for service"
    except TimeoutError:
        error_found = 1
        err_type = "Timeout for service"
    except socket.gaierror:
        error_found = 1
        err_type = "DNS Error? No such name or service"
    
    if error_found:
        (msg_err, str(addr))
        return (C.CHECK_ERROR, "%s. %s: %s" % (msg_err, err_type, str(addr)))
    else:
        return (C.CHECK_OK, conn.getresponse())
