package main

import (
	"flag"
	"io/ioutil"
	"encoding/json"
	"log"
	"os"
	"./channel"
	"runtime/debug"
)

var
(
	address          string
	registerInstance string
	remoteInstance   string
	confPath         string
)

func init() {
	flag.StringVar(&address, "r", "127.0.0.1:8899", "远程连接地址")
	flag.StringVar(&confPath, "conf", "", "本地配置文件地址")
	flag.StringVar(&registerInstance, "reg", "P2P_CLIENT_DEFAULT", "本机注册名称")
	flag.StringVar(&remoteInstance, "ri", "P2P_SERVER_DEFAULT", "连接远端主机")
}

func initConfig() error {
	data, err := ioutil.ReadFile(confPath)
	if err != nil {
		return err
	}
	result := struct {
		Address          string `json:"address"`
		RegisterInstance string `json:"register_instance"`
		RemoteInstance   string `json:"remote_instance"`
	}{}
	err = json.Unmarshal(data, &result)
	if err != nil {
		return err
	}
	address = result.Address
	registerInstance = result.RegisterInstance
	remoteInstance = result.RemoteInstance
	return nil
}

func handlePacket(data []byte) {

}

func main() {
	flag.Parse()
	var err error
	if confPath != "" {
		err = initConfig()
		if err != nil {
			println(err)
			return
		}
	}
	logger := log.New(os.Stdout, registerInstance + " ", log.Ldate | log.Ltime)
	flags := log.Ldate
	flags |= log.Ltime | log.Lshortfile
	logger.SetFlags(flags)
	logger.Println(address)
	logger.Println(registerInstance)
	logger.Println(remoteInstance)
	tcpServer := channel.TcpServer{RemoteHost:address, Logger:logger, Fn: handlePacket}
	tcpServer.Connect()
	tcpServer.ServiceForever()
	for {
		defer func() {
			if e := recover(); e != nil{
				logger.Printf("主程序异常%v, %s", e, string(debug.Stack()))
			}
		}()
	}
}
