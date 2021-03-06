package proto

const (
	// UDP protocl
	P2P_LOGIN uint16 = 0x01
	P2P_PING = 0x02
	P2P_PONG = 0x03
	P2P_DELIVER_PING = 0x04
	P2P_HELLO = 0x05
	P2P_HEARTBIT = 0x06

	// TCP protocl
	C2S_LOGIN = 0x01
	C2S_REQUEST_P2P_CONNECTION = 0x02
	C2S_DELIVER_PING = 0x03
)