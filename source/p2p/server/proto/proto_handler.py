# -*- coding:utf-8 -*-

import proto.proto_pack
import common.Logger
import proto.proto_no
import common.session
import common.error_code
import common.constants
tcpHandlerMap = {}


def tcp_handler(conn, mask, data):
    parser = proto.proto_pack.UnpackParser(data)
    protocal = parser.get_word()
    common.Logger.log.info("收到协议：%x" % protocal)
    if protocal in tcpHandlerMap:
        tcpHandlerMap[protocal](conn, parser)
    else:
        common.Logger.info("收到未知协议 %x" % protocal)


def udp_handler(sock, data, addr):
    parser = proto.proto_pack.UnpackParser(data)
    # UDP包前两个字节 表示长度
    data_len = parser.get_word()
    pro = parser.get_word()
    pack_parser = proto.proto_pack.PackParser()
    if pro == proto.proto_no.P2P_LOGIN:
        instance = parser.get_string()
        pack_parser.gene_word(proto.proto_no.P2P_LOGIN)
        # user = common.session.user_manager.get_user(instance)
        exists = common.session.user_manager.update_user(instance, addr)
        if exists:
            pack_parser.gene_word(common.error_code.OK)
        else:
            pack_parser.gene_word(common.error_code.INSTANCE_NOT_EXISTS)
        sock.send_to(pack_parser.generate_buf(), addr)
    elif pro == proto.proto_no.P2P_HEARTBIT:
        instance = parser.get_string()
        user = common.session.user_manager.get_user(instance)
        if user is not None:
            pack_parser.gene_word(proto.proto_no)
            sock.send_to(pack_parser.generate_buf(), addr)
        else:
            common.Logger.log.warn("非法UDP包 addr: {0} len: {1}".format(addr, len(data)))
    else:
        common.Logger.log.warn("非法协议 UDP包 addr: {0} len: {1}".format(addr, len(data)))


def s2c_login(conn, parser):
    instance = parser.get_string()
    common.Logger.log.info("register instance : %s" % instance)
    pack_parser = proto.proto_pack.PackParser()
    pack_parser.gene_word(proto.proto_no.S2C_LOGIN)
    user = common.session.user_manager.get_user(instance)
    if user is not None:
        common.Logger.log.info("%s 注册成功" % instance)
        pack_parser.gene_word(common.error_code.INSTANCE_IS_EXISTS)
    else:
        common.Logger.log.info("%s 注册失败", instance)
        pack_parser.gene_word(common.error_code.OK)
        common.session.user_manager.add_user(instance, conn)
        pack_parser.gene_string("%s:%d" % (common.constants.UDP_SERVER_IP, common.constants.UDP_SERVER_PORT))
    common.session.send_data(pack_parser.generate_buf())


def s2c_request_p2p_connection(conn, parser):
    self_instance = parser.get_string()
    instance = parser.get_string()
    user = common.session.user_manager.get_user(instance)
    pack_parser = proto.proto_pack.PackParser()
    pack_parser.gene_word(proto.proto_no.S2C_REQUEST_P2P_CONNECTION)
    if user is None:
        pack_parser.gene_word(common.error_code.INSTANCE_NOT_EXISTS)
    elif user.udp_address is None:
        pack_parser.gene_word(common.error_code.NOT_KNOWN_UDP_ADDR)
    else:
        s2c_deliver_ping(self_instance)
        pack_parser.gene_word(common.error_code.OK)
        pack_parser.gene_string("%s:%d" % user.udp_address)
    common.session.send_data(conn, pack_parser.generate_buf())


# def s2c_deliver_ping(conn, parser):
#     pass

def s2c_deliver_ping(self_instance):
    user = common.session.user_manager.get_user(self_instance)
    pack_parser = proto.proto_pack.PackParser()
    pack_parser.gene_word(proto.proto_no.S2C_DELIVER_PING)
    if user is None:
        pack_parser.gene_word(common.error_code.INSTANCE_NOT_EXISTS)
    elif user.udp_address is None:
        pack_parser.gene_word(common.error_code.NOT_KNOWN_UDP_ADDR)
    else:
        pack_parser.gene_word(common.error_code.OK)
        pack_parser.gene_string("%s:%d" % user.udp_address)
    user.send(pack_parser.generate_buf())


def tcp_handler_init():
    tcpHandlerMap[proto.proto_no.S2C_LOGIN] = s2c_login
    # tcpHandlerMap[proto.proto_no.S2C_DELIVER_PING] = c2s_deliver_ping
    tcpHandlerMap[proto.proto_no.S2C_REQUEST_P2P_CONNECTION] = s2c_request_p2p_connection
