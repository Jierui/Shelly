package channel

import (
	"net"
	"strconv"
)

type Udp struct {

}

func listenUdp(bindAddr string) (net.Conn, error) {
	host, port, _ := net.SplitHostPort(bindAddr)
	p, _ := strconv.Atoi(port)
	addr := net.UDPAddr{IP:net.ParseIP(host), Port: p}
	conn, err := net.ListenUDP("udp", &addr)
	return conn, err
}


func UdpService() {

}



