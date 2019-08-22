# -*- coding: UTF-8 -*-
import struct

class FlvParse:

    def __init__(self, data):
        self.type = 1
        if data is not None:
            self.data = data
            self.data_len = len(data)
        else:
            self.data = bytearray()
        self.data_offset = 0
        self.tag_header_length = 11
        self.hasVideo = False
        self.hasAudio = False

    def parse(self):
        self.flvHeader()
        while True:
            tagh = self.tagHeader()
            if tagh is None:
                break
            r = self.tagBody(tagh)
            if r is False:
                break
            print()

    def flvHeader(self):
        print("FLV Header:")
        signature = self.data[0] == 0x46 and self.data[1] == 0x4c and self.data[2] == 0x56
        if not signature:
            raise RuntimeError("Signature Error")
        tag_type = self.data[3]
        self.hasAudio = tag_type & 0x04 > 0
        self.hasVideo = tag_type & 0x01 > 0
        print("video:", self.hasVideo)
        print("audio:", self.hasAudio)
        self.data_offset = self.data_offset + 9
        self.data_offset = self.data_offset + 4
        print("FLV Body:\n")


    def tagHeader(self):
        if self.data_offset + self.tag_header_length > self.data_len:
            return None
        tagHeader = TagHeader()
        tagHeader.type = self.data[self.data_offset] & 0x1F
        if tagHeader.type == 0x08:
            print("AudioTag:")
        elif tagHeader.type == 0x09:
            print("VideoTag:")
        elif tagHeader.type == 0x12:
            print("ScriptTag:")
        else:
            print("unknown tag type")
        # 3bytes
        data = bytearray(self.data[self.data_offset+1:self.data_offset + 4])
        data.insert(0, 0x00)
        tagHeader.dataSize = struct.unpack(">I", data)[0]
        self.data_offset = self.data_offset + self.tag_header_length
        return tagHeader

    def tagBody(self, tag_header):
        if self.data_offset + tag_header.dataSize > self.data_len:
            return False
        # print("TagBody:")
        print("Media Data Size: %d " % tag_header.dataSize)
        if tag_header.type == 0x09:
            d = self.data[self.data_offset]
            print("FrameType:%d" % ((d >> 4) & 0x0F))
            print("CodecID:%d" % (d & 0x0F))
            d = self.data[self.data_offset + 1]
            print("AVCPacketType:%d" % d)
            d = self.data[self.data_offset + 5 + 4]
            print("NalType:%d" % (d & 0x1F))
        elif tag_header.type == 0x08:
            d = self.data[self.data_offset]
            print("SoundFormat:%d " % ((d >> 4) & 0x0F))
            print("SoundRate:%d " % ((d >> 2) & 0x03))
            print("SoundSize:%d " % ((d >> 1) & 0x02))
            print("SoundType:%d " % (d & 0x01))
            d = self.data[self.data_offset + 1]
            print("AACpacketType:%d", (d & 0xFF))
        elif tag_header.type == 0x12:
            pass
        else:
            print("unknown body:")

        self.data_offset = self.data_offset + tag_header.dataSize

        if self.data_offset + 4 > self.data_len:
            return False
        tmpData = self.data[self.data_offset: self.data_offset+4]
        tagsize = struct.unpack(">I", tmpData)[0]
        print("PreTagSize:%d" % tagsize)
        self.data_offset = self.data_offset + 4
        return True

class TagHeader:
    def __init__(self):
        self.type = None
        self.dataSize = None

