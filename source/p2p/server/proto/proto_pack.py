# -*- coding:utf-8 -*-

import struct
DATA_LEN = 2
STATE_NORMAL = 0
STATE_GET_LEN = 1
STATE_GET_DATA = 2


class PackParser:

    def __init__(self):
        self.buff = bytearray()

    def gene_char(self, c):
        self.buff.extend(struct.pack(">b", c))

    def gene_word(self, word):
        self.buff.extend(struct.pack(">H", word))

    def gene_string(self, s):
        str_len = len(s)
        self.gene_word(str_len)
        self.buff.extend(struct.pack("{0}s".format(str_len), s.encode()))

    def generate_buf(self):
        return self.buff


class UnpackParser:

    def __init__(self, data):
        self.buff = data
        self.index = 0

    def get_word(self):
        tmp_data = self.buff[self.index:self.index+2]
        d = struct.unpack(">H", tmp_data)
        self.index = self.index + 2
        return d[0]

    def get_string(self):
        str_len = self.get_word()
        tmp_data = self.buff[self.index:self.index+str_len]
        s = struct.unpack("{0}s".format(str_len), tmp_data)
        self.index = self.index + str_len
        return s[0]


class ReadProto:
    def __init__(self):
        self.data = bytearray()
        self.state = STATE_NORMAL
        self.data_len = 0

    def read(self, data):
        self.data.extend(data)
        state = self.state
        while True:
            d = self.process_data()
            if d[1] == self.state:
                return None
            self.state = d[1]
            if self.state == STATE_GET_DATA:
                self.state = STATE_NORMAL
                return d[0]

    def process_data(self):
        if self.state == STATE_NORMAL:
            if len(self.data < 2):
                return None, self.state
            tmp_data = self.data[0:2]
            tup = struct.unpack(">H", tmp_data)
            self.data_len = tup[0]
            self.data = self.data[2:]
            return STATE_GET_LEN
        elif self.state == STATE_GET_LEN:
            if len(self.data) < self.data_len:
                return None, self.state
            d = self.data[0, self.data_len]
            self.data = self.data[self.data_len:]
            return d, STATE_GET_DATA


