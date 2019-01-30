package channel

import (
	"log"
	"runtime/debug"
	"net"
)

type TcpServer struct {
	RemoteHost string
	*log.Logger
	Conn *net.Conn
	Fn func(packet []byte)
}

func (s* TcpServer) Connect() error{
	conn, err := net.Dial("tcp", s.RemoteHost)
	if err != nil {
		return err
	}
	s.Conn = &conn
	s.Println("TCP服务器连接成功")
	return nil
}

func (s *TcpServer) ServiceForever() {
	go func() {
		defer func() {
			if e := recover(); e != nil {
				s.Printf("TcpService crashed err:%s \ntrance:%s", e, string(debug.Stack()))
			}
		}()
		buf := make([]byte, 1024 * 8)
		for {
			n, e := (*s.Conn).Read(buf)
			if e != nil {
				(*s.Conn).Close()
				panic(e)
			}
			s.Printf("n:%d %s", n, string(buf[0:n]))
			s.Fn(buf[0:n])
		}
	}()
}
