#include <stdint.h>
#include <stdlib.h>
//https://github.com/golang/go/issues/20639
int onTsPacket(void* param, int program, int stream, int codecid, int flags, int64_t pts, int64_t dts, void* data, size_t bytes);
int onTsCallback(void* param, int program, int stream, int codecid, int flags, int64_t pts, int64_t dts, const void* data, size_t bytes) {
	return onTsPacket(param, program, stream, codecid, flags, pts, dts, (void*)data, bytes);
}