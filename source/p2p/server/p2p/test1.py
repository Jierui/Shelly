# -*- coding:utf-8 -*-
import socket
import selectors


class TcpServer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.select = selectors.DefaultSelector
        self.sock = None

    def bind(self):
        self.sock = socket.socket()
        self.sock.bind((self.ip, self.port))

    def listen(self, backlog):
        self.sock.listen(backlog)
        self.sock.setblocking(False)
        self.select.register(self.sock, selectors.EVENT_READ, self.accept)

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        # print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.select.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1000)  # Should be ready
        if data:
            # print('echoing', repr(data), 'to', conn)
            conn.send(data)  # Hope it won't block
        else:
            # print('closing', conn)
            self.select.unregister(conn)
            conn.close()

    def run_server(self):
        while True:
            events = self.select.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

