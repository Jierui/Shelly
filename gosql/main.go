package main

import (
	"./db"
	"fmt"
	//"time"
	//"strconv"
)

func main(){
	//InserData()
	QueryData()
	//fmt.Println(time.Now().Unix())
}

func InserData2Table(appid,groupid,personid,faceid string, feature []byte){
	err := db.MysqlDb.Exec("INSERT INTO tbidentify(appid,groupid,personid,faceid,feature) VALUES(?,?,?,?,?)",
		appid,groupid,personid,faceid,feature)
	if err != nil{
		fmt.Printf("InserData err:%v\n",err)
	}
}

func InserData(){
	appid := "123456"
	groupid := "hello"
	personid := "jie"
	faceid := "1234"
	//updatetime := strconv.FormatInt(time.Now().UnixNano(), 10)
	feature := []byte("hello world")
	InserData2Table(appid,groupid,personid,faceid,feature)
}

func QueryData(){
	raw,err := db.MysqlDb.Query("select appid,groupid,personid,faceid,updatetime as hello,feature from tbidentify")
	if err != nil{
		fmt.Printf("query err:%v\n", err)
		return
	}
	fmt.Println(raw)
	fmt.Println(len(raw))
	for _, d := range raw{
		appid := d["appid"].(string)
		fmt.Println(appid)
		groupid := d["groupid"].(string)
		fmt.Println(groupid)
		updatetime := d["hello"].(string)
		fmt.Println(updatetime)
		feature := d["feature"].(string)
		fmt.Println(string(feature))
	}
}


