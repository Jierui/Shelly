# -*- coding:utf-8 -*-
import p2p.TcpServer
import common.Logger
import proto.proto_handler
import p2p.UDPServer
import threading
import common.constants

TCP_SERVER_IP = ""
TCP_SERVER_PORT = 9999


def tcp_server_run():
    server = p2p.TcpServer.TcpServer(TCP_SERVER_IP, TCP_SERVER_PORT, proto.proto_handler.tcp_handler)
    server.run_forever()


def udp_server_run():
    server = p2p.UDPServer.UDPServer(common.constants.UDP_SERVER_IP, common.constants.UDP_SERVER_PORT,
                                     proto.proto_handler.udp_handler)
    th = threading.Thread(target=server.run)
    th.setDaemon(True)
    th.start()
    return th


def main():
    common.Logger.init_logger()
    common.Logger.log.info("服务器开始运行")
    proto.proto_handler.tcp_handler_init()
    th = udp_server_run()
    tcp_server_run()
    th.join(2)
    common.Logger.log.info("服务器停止运行")


if __name__ == "__main__":
    main()




