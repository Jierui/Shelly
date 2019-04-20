# -*- coding:utf-8 -*-
import threading


class UserInfo:
    def __init__(self, instance):
        self.instance = instance
        self.udp_address = None
        self.conn = None

    def send(self, data):
        while True:
            n = self.conn.send(data)
            if n == len(data):
                return True
            data = data[n:]


class UserManager:
    def __init__(self):
        self.lock = threading.RLock()
        self.user_map = {}

    def add_user(self, instance, conn):
        self.lock.acquire()
        if instance in self.user_map:
            user = self.user_map[instance]
            user.conn = conn
        else:
            user = UserInfo()
            user.instance = instance
            user.conn = conn
            self.user_map[instance] = user
        self.lock.release()

    def remove_user(self, instance):
        self.lock.acquire()
        self.user_map.pop(instance)
        self.lock.release()

    def update_user(self, instance, addr):
        self.lock.acquire()
        if instance in self.user_map:
            user = self.user_map[instance]
            user.udp_address = addr
        self.lock.acquire()
        return user is not None

    def get_user(self, instance):
        user = None
        self.lock.acquire()
        if instance in self.user_map:
            # 这里可以进行浅拷贝操作
            # copy.copy
            user = self.user_map[instance]
        self.lock.release()
        return user

    def get_user_by_conn(self, conn):
        user = None
        self.lock.acquire()
        for k, v in self.user_map:
            if v.conn == conn:
                # 这里可进行浅拷贝操作
                user = v
                break
        self.lock.release()
        return user


user_manager = UserManager()


def send_data(conn, data):
    while True:
        n = conn.send(data)
        if n == len(data):
            return True
        data = data[n:]
