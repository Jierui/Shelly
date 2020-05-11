# -*- coding: UTF-8 -*-
import FlvParser


def predeal_flv_header(data):
    file_path_1 = 'D:\\tmp-data\\orign\\gb_m.flv'
    fd = open(file_path_1, 'wb')
    offset = 0
    while True:
        signature = data[offset] == 0x46 and data[offset + 1] == 0x4c and data[offset + 2] == 0x56
        if signature:
            d = data[offset:]
            fd.write(d)
            fd.close
            return d
        offset += 1


file_path = 'D:\\tmp-data\\63-d\\nometa.flv'
file = open(file_path, 'rb')
data = file.read(300)
d = predeal_flv_header(data)
flv_parser = FlvParser.FlvParse(d)
flv_parser.parse()
