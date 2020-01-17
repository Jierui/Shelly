package main

/*
#cgo CFLAGS: -I../libmpeg/include
#cgo LDFLAGS: -L../libs -lmpeg
#include <stdlib.h>
#include "mpeg-ps.h"
#include "mpeg-ts.h"
#include "mpeg-ts-proto.h"
#include <stdio.h>

int onTsPacket(void* param, int program, int stream, int codecid, int flags, int64_t pts, int64_t dts, void* data, size_t bytes);

int onTsCallback(void* param, int program, int stream, int codecid, int flags, int64_t pts, int64_t dts, const void* data, size_t bytes);
*/
import "C"

import (
	// "fmt"
	"unsafe"
	"os"
	"log"
	"reflect"
	"time"
)

//导出C函数
//export onTsPacket
func onTsPacket(param unsafe.Pointer, program, stream, avtype, flags C.int, pts, dts C.int64_t, data unsafe.Pointer, bytes C.size_t) C.int {
	//log.Println("avtype:", avtype, pts, dts)
	return 0
}



func main() {
	// dir, _ := os.Getwd()
	// fmt.Println(dir)
	file, err := os.Open("../test.ts") // For read access.
	if err != nil {
		log.Fatal(err)
	}
	old := time.Now().UnixNano()
	var ioTime int64
	data := make([]byte, 188)
	ts := C.ts_demuxer_create((C.ts_demuxer_onpacket)(C.onTsCallback), C.NULL)
	for{
		oldTime := time.Now().UnixNano()
		count, err := file.Read(data)
		ioTime += time.Now().UnixNano() - oldTime
		if err != nil {
			log.Println(err);
			break;
		}
		if count != 188 {
			log.Println("break:", count)
			break;
		}
		p := (*reflect.SliceHeader)(unsafe.Pointer(&data))
		C.ts_demuxer_input(ts, (*C.uchar)(unsafe.Pointer(p.Data)),188)
	}
	C.ts_demuxer_flush(ts);
	C.ts_demuxer_destroy(ts);
	log.Println(time.Now().UnixNano() - old)
	log.Println(ioTime)
	log.Println("down")
}
