# -*- coding:utf-8 -*-

import struct


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

