package proto

import (
	"encoding/binary"
	"fmt"
)

const UINT16_MAX  = ^uint16(0)

const(
	STATE_NORMAL uint8 = 0
	STATE_GET_LEN = 1
	STATE_GET_DATA = 2
)
type ProtoReader struct {
	Data []byte
	State uint8
	DataLen uint16
}


func (s *ProtoReader) Read(data []byte) ([]byte) {
	s.Data = append(s.Data, data...)
	state := s.State
	var d []byte
	for {
		d, state = s.processData()
		if state == STATE_GET_DATA {
			s.State = STATE_NORMAL
			return d
		} else if state == s.State {
			return nil
		}
		s.State = state
	}
}


func (s *ProtoReader) processData() ([]byte, uint8){
	if s.State == STATE_NORMAL {
		if len(s.Data) < 2 {
			return nil, s.State
		}
		len := binary.BigEndian.Uint16(s.Data[0:2])
		if len > UINT16_MAX {
			panic(fmt.Errorf("数据长度错误 %d", len))
		}
		s.DataLen = len
		s.Data = s.Data[2:]
		return nil, STATE_GET_LEN
	} else if s.State == STATE_GET_LEN {
		if uint16(len(s.Data)) < s.DataLen {
			return nil, s.State
		}
		d := s.Data[0: s.DataLen]
		s.Data = s.Data[s.DataLen:]
		return d, STATE_GET_DATA
	}
	return nil, s.State
}





