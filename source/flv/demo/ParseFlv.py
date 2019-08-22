# -*- coding: UTF-8 -*-
import FlvParser
file_path = 'D:\\tmp-data\\orign\\plat_c.flv'
file = open(file_path, 'rb')
data = file.read()
flv_parser = FlvParser.FlvParse(data)
flv_parser.parse()
