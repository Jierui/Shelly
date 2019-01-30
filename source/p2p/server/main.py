# -*- coding:utf-8 -*-
import p2p.TcpServer
import p2p.Logger
import proto.proto_handler
TCP_SERVER_IP = ""
TCP_SERVER_PORT = 9999


def tcp_server_run():
    server = p2p.TcpServer.TcpServer(TCP_SERVER_IP, TCP_SERVER_PORT, proto.proto_handler.tcp_handler)
    server.run_forever()


def main():
    p2p.Logger.init_logger()
    p2p.Logger.log.info("服务器开始运行")
    tcp_server_run()


if __name__ == "__main__":
    main()




