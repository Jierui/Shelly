# -*- coding: UTF-8 -*-
import struct

def orb(x):
    if isinstance(x, int):
        return x
    return ord(x)

def print_str_bytes(data):
    s = ""
    tmps = None
    for x in data:
        ts = chr(x)
        # if tmps and tmps.isprintable() != ts.isprintable():
        #     s += " "
        if ts.isprintable():
            s += ts
        else:
            s += "%02x" % orb(x)
        tmps = ts
    return s


def print_hex(s):
    return "".join("%02x" % orb(x) for x in s)


class FlvParse:

    def __init__(self, data=None):
        self.type = 1
        # self.data_len = 0
        self.full_data = False
        if data is not None:
            self.data = data
            self.full_data = True
        else:
            self.full_data = False
            self.data = bytearray()
        self.data_offset = 0
        self.tag_header_length = 11
        self.hasVideo = False
        self.hasAudio = False
        self.max_data_size = 1024 * 1024 * 8   # 8M
        self.tag_header = TagHeader()
        self.step = 0
        self.last_video_timestamp = 0
        self.last_audio_timestamp = 0

    def parse(self, data=None):
        if not self.full_data and data is not None:
            self.data.extend(data)
        if self.step == 0:
            result = self.flvHeader()
            if not result:
                return False
        while True:
            if self.step == 1:
                tagh = self.tagHeader()
                if tagh is None:
                    break
            elif self.step == 2:
                r = self.tagBody()
                if r is False:
                    break
            else:
                print("step invalid:", self.step)
                exit(0)
            if not self.full_data and len(self.data) > self.max_data_size:
                self.data = bytearray(self.data[self.data_offset:])
                self.data_offset = 0

    def tagHeaderInit(self):
        self.tag_header.filter = 0
        self.tag_header.dataSize = 0
        self.tag_header.dataSize = 0
        self.tag_header.type = 0
        self.tag_header.timeStamp = 0
        self.tag_header.timeStampExtended = 0
        return self.tag_header

    def flvHeader(self):
        if len(self.data) < 13:
            return False
        print("FLV Header:", end=' ')
        signature = self.data[0] == 0x46 and self.data[1] == 0x4c and self.data[2] == 0x56
        if not signature:
            raise RuntimeError("Signature Error")
        tag_type = self.data[4]
        self.hasAudio = tag_type & 0x04 > 0
        self.hasVideo = tag_type & 0x01 > 0
        print("video:", self.hasVideo, end=' ')
        print("audio:", self.hasAudio, end=' ')
        self.data_offset = self.data_offset + 9
        self.data_offset = self.data_offset + 4
        print("\nFLV Body:")
        self.step = 1
        return True


    def tagHeader(self):
        if self.data_offset + self.tag_header_length > len(self.data):
            return None
        tagHeader = self.tagHeaderInit()
        tagHeader.filter = (self.data[self.data_offset] >> 5) & 0x01
        # print("filter:", tagHeader.filter, end=' ')
        tagHeader.type = self.data[self.data_offset] & 0x1F
        if tagHeader.type == 0x08:
            print("AudioTag:", end=' ')
        elif tagHeader.type == 0x09:
            print("VideoTag:", end=' ')
        elif tagHeader.type == 0x12:
            print("ScriptTag:", end=' ')
        else:
            print("unknown tag type:", tagHeader.type, end=' ')
        # 3bytes
        data = bytearray(self.data[self.data_offset+1:self.data_offset + 4])
        data.insert(0, 0x00)
        tagHeader.dataSize = struct.unpack(">I", data)[0]
        data = bytearray(self.data[self.data_offset+4:self.data_offset + 7])
        data.insert(0, 0x00)
        tagHeader.timeStamp = struct.unpack(">I", data)[0]
        tagHeader.timeStampExtended = self.data[self.data_offset + 7] & 0xFF
        if tagHeader.timeStampExtended != 0:
            tagHeader.timeStamp = tagHeader.timeStampExtended << 24 + tagHeader.timeStamp
        # print("dataSize:", tagHeader.dataSize, end=' ')
        print("timeStamp:", tagHeader.timeStamp, end=' ')
        if tagHeader.type == 0x08:
            if self.last_audio_timestamp == 0:
                delta = 0
            else:
                delta = tagHeader.timeStamp - self.last_audio_timestamp
            print("timestamp_delta:", delta, end=' ')
            self.last_audio_timestamp = tagHeader.timeStamp
        elif tagHeader.type == 0x09:
            if self.last_video_timestamp == 0:
                delta = 0
            else:
                delta = tagHeader.timeStamp - self.last_video_timestamp
            print("timestamp_delta:", delta, end=' ')
            self.last_video_timestamp = tagHeader.timeStamp
        if tagHeader.timeStampExtended != 0:
            print("timeStampExtended:", tagHeader.timeStampExtended, end=' ')
        self.data_offset = self.data_offset + self.tag_header_length
        self.step = 2
        return tagHeader

    def tagBody(self):
        tag_header = self.tag_header
        if self.data_offset + tag_header.dataSize + 4 > len(self.data):
            return False
        # print("TagBody:")
        # print("Media Data Size: %d " % tag_header.dataSize)
        if tag_header.type == 0x09:
            d = self.data[self.data_offset]
            print("FrameType:%d" % ((d >> 4) & 0x0F), end=' ')
            print("CodecID:%d" % (d & 0x0F), end=' ')
            d = self.data[self.data_offset + 1]
            print("AVCPacketType:%d" % d, end= ' ')
            d = self.data[self.data_offset + 5 + 4]
            # print("NalType:%d" % (d & 0x1F))
            print("data:" + print_hex(self.data[self.data_offset+5:self.data_offset+5+16]), end=' ')
        elif tag_header.type == 0x08:
            d = self.data[self.data_offset]
            print("SoundFormat:%d " % ((d >> 4) & 0x0F), end=' ')
            print("SoundRate:%d " % ((d >> 2) & 0x03), end=' ')
            print("SoundSize:%d " % ((d >> 1) & 0x01), end=' ')
            print("SoundType:%d " % (d & 0x01), end=' ')
            d = self.data[self.data_offset + 1]
            print("AACpacketType:", (d & 0xFF), end=' ')
            print("data:" + print_hex(self.data[self.data_offset+2:self.data_offset+2+16]), end=' ')
        elif tag_header.type == 0x12:
            print("data:" + print_str_bytes(self.data[self.data_offset:self.data_offset+tag_header.dataSize]), end=' ')
        else:
            print("unknown body:")

        print("dataSize:", tag_header.dataSize, end=' ')
        self.data_offset = self.data_offset + tag_header.dataSize
        # if self.data_offset + 4 > len(self.data):
        #     return False
        tmpData = self.data[self.data_offset: self.data_offset+4]
        tagsize = struct.unpack(">I", tmpData)[0]
        print("PreTagSize:%d" % tagsize)
        self.data_offset = self.data_offset + 4
        self.step = 1
        return True


class TagHeader:
    def __init__(self):
        self.filter = 0
        self.type = None
        self.dataSize = None
        self.timeStamp = 0
        self.timeStampExtended = 0

