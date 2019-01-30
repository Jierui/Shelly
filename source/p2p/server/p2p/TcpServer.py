# -*- coding:utf-8 -*-
import selectors
import socket
import p2p.Logger
import proto.proto_pack
sel = selectors.DefaultSelector()


class TcpServer:

    def __init__(self, ip, port, read_handler):
        self.ip = ip
        self.port = port
        self.sock = None
        self.shut_down = False
        self.proto_reader = proto.proto_pack.ReadProto()
        self.read_handler = read_handler

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        p2p.Logger.log.info("accepted {0} from {1}".format(conn, addr))
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1000)  # Should be ready
        if data:
            print('echoing', repr(data), 'to', conn)
            d = self.proto_reader.read(data)
            if d is not None:
                self.read_hander(conn, mask, data)
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
                # p2p.Logger.log.info("socket {0} has recevied".format(key.fileobj))
        sel.unregister(self.sock)
        self.sock.close()

