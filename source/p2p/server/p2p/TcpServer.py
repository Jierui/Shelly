# -*- coding:utf-8 -*-
import selectors
import socket

sel = selectors.DefaultSelector()


class TcpServer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.shut_down = False

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1000)  # Should be ready
        if data:
            print('echoing', repr(data), 'to', conn)
            conn.send(data)  # Hope it won't block
        else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()

    def run_forever(self):
        self.shut_down = True
        self.sock = socket.socket()
        self.sock.bind((self.ip, self.port))
        self.sock.listen(100)
        self.sock.setblocking(False)
        sel.register(self.sock, selectors.EVENT_READ, self.accept)
        while self.shut_down:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

