package channel


type Session struct {
	tcp *TcpClient
	udp *UdpServer
}

var Se *Session = nil