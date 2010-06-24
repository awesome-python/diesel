# vim:ts=4:sw=4:expandtab
import socket
import errno
from uuid import uuid4
from collections import deque

class Client(object):
    '''An agent that connects to an external host and provides an API to
    return data based on a protocol across that host.
    '''
    def __init__(self, addr, port, security=None):
        self.security = security
        self.connected = False
        self.conn = None
        self.addr = addr
        self.port = port

        from resolver import resolve_dns_name
        from core import _private_connect

        ip = resolve_dns_name(self.addr)
        remote_addr = (ip, self.port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)

        try:
            sock.connect(remote_addr)
        except socket.error, e:
            if e[0] == errno.EINPROGRESS:
                _private_connect(self, ip, sock)
            else:
                raise

    def close(self):
        '''Close the socket to the remote host.
        '''
        if not self.closed:
            self.on_close()
            self.conn.pipeline.close_request()
            self.conn = None
            self.closed = True
            self.connected = True

    @property
    def is_closed(self):
        return self.conn is None

    def on_connect(self):
        '''Hook to implement a handler to do any setup after the
        connection has been established.
        '''
        pass

    def on_close(self):
        '''Hook called when the remote side closes the connection,
        for cleanup.
        '''
        pass
