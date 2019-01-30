# -*- coding:utf-8 -*-

import socketserver
'''
此模块弃用
'''

class UdpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        soct = self.request[1]
        print(data)
        soct.sendto(data, self.client_address)
        self.client_address


class TcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print(data)
        print("\n")
        # self.request.write("hhh".encode())


class P2PServer(socketserver.UDPServer):
    pass


class Server(socketserver.TCPServer):
    pass


UDP_HOST = ""
UDP_PORT = 9999
TCP_HOST = ""
TCP_POST = 9999


def start_p2p_server():
    with P2PServer((UDP_HOST, UDP_PORT), UdpHandler) as p2p_server:
        p2p_server.serve_forever()


def start_server():
    with Server((UDP_HOST, UDP_PORT), TcpHandler) as server:
        server.serve_forever()
