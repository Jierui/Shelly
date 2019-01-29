# -*- coding:utf-8 -*-
import p2p.TcpServer
TCP_SERVER_IP = ""
TCP_SERVER_PORT = 9999


def tcp_server_run():
    server = p2p.TcpServer.TcpServer(TCP_SERVER_IP, TCP_SERVER_PORT)
    server.run_forever()


def main():
    # print("main")
    tcp_server_run()


if __name__ == "__main__":
    main()




