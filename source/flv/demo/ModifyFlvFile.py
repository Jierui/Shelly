import struct
read_file_path = r'D:\tmp-data\orign\plat.flv'
write_file_path = r'D:\tmp-data\orign\modify.flv'
read_file = open(read_file_path, 'rb')
data = read_file.read()
data_len = len(data)
write_file = open(write_file_path, 'wb')
offset = 0
print("data_len:%d" % data_len)
write_buffer = bytearray()
if data_len < 13:
    print("len error:")
    exit(1)
write_buffer.extend(data[0:13])
offset = offset + 13
while True:
    print(offset)
    d = data[offset]
    tag_type = d & 0x1F
    d = bytearray(data[offset + 1:offset + 4])
    d.insert(0, 0x00)
    data_size = struct.unpack(">I", d)[0]
    pos = offset + data_size + 11 + 4
    if pos > data_len:
        break
    if tag_type == 0x09:
        d = data[offset + 11]
        frame_type = ((d >> 4) & 0x0F)
        if frame_type == 2:
            if data_size > 50:
                write_buffer.extend(data[offset:pos])
            else:
                print("frame_type:%d size:%d" % (frame_type, data_size))
        else:
            write_buffer.extend(data[offset:pos])
    else:
        write_buffer.extend(data[offset:pos])
    offset = pos

write_file.write(write_buffer)

