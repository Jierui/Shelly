# -*- coding:utf-8 -*-
import socket


class UDPServer:
    def __init__(self, ip, port, callback):
        self.soct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.soct.bind((ip, port))
        self.is_run = False
        self.callback = callback

    def run(self):
        self.is_run = True
        while self.is_run:
            data, addr = self.soct.recvfrom(1024)
            self.callback(self.soct, data, addr)
        self.soct.close()

    def close(self):
        self.is_run = False