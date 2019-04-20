package channel

import (
	"net"
	"strconv"
	"runtime/debug"
	"log"
)

type UdpServer struct {
	Conn *net.UDPConn
	*log.Logger
	Fn func(data []byte, addr net.Addr)
}

func (s *UdpServer) Listen(bindAddr string) (net.Conn, error) {
	host, port, _ := net.SplitHostPort(bindAddr)
	p, _ := strconv.Atoi(port)
	addr := net.UDPAddr{IP:net.ParseIP(host), Port: p}
	conn, err := net.ListenUDP("udp", &addr)
	s.Conn = conn
	return conn, err
}


func (s *UdpServer) RunUdpService() {
	go func(){
		defer func(){
			if e := recover(); e != nil {
				s.Printf("UdpService crashed err:%s \ntrance:%s", e, string(debug.Stack()))
			}
		}()
		buff := make([]byte, 1024)
		n, d, e := s.Conn.ReadFrom(buff)
		if e != nil {
			s.Printf("Recv UDP packet err :%v", e)
		}else {
			s.Fn(buff[0:n], d)
		}
	}()
}

func (s* UdpServer) SendTo(data []byte, addr net.Addr) {
	s.Conn.WriteTo(data, addr)
}


