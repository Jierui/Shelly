package db

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"sync"
	"fmt"
)

var(
	dbname = "ac2049"
	tbname = "tbidentify"
	ip = "127.0.0.1"
	port = "3306"
	user = "root"
	pwd = "lj199335"
)

type Mysql struct{
	DbName string
	TbName string
	Ip string
	Port string
	mysql *sql.DB
	dbInitOnce sync.Once
	User string
	PassWord string
}

var MysqlDb = Mysql{DbName:dbname, TbName:tbname, Ip:ip, Port:port, User:user, PassWord:pwd}


func (s *Mysql) Exec(query string, args ...interface{}) (error){
	var err error
	s.dbInitOnce.Do(func(){
		s.mysql, err = sql.Open("mysql",fmt.Sprintf("%s:%s@tcp(%s:%s)/%s",s.User, s.PassWord, s.Ip, s.Port,s.DbName))
		if err != nil{
			fmt.Println("sql.open err %v\n", err)
			panic(err.Error())
		}
		err = s.mysql.Ping()
		if err != nil{
			fmt.Printf("ping err:%v\n", err)
			panic(err.Error())
		}
		fmt.Println("Initialize DB success\n")
	})
	_, err = s.mysql.Exec(query, args...)
	if err != nil{
		fmt.Printf("Exec failed:%v\n", err)
		return err
	}
	return nil
}

func (s *Mysql) Query(query string, args ...interface{}) ([]map[string]interface{}, error){
	var err error
	s.dbInitOnce.Do(func(){
		s.mysql, err = sql.Open("mysql",fmt.Sprintf("%s:%s@tcp(%s:%s)/%s",s.User, s.PassWord, s.Ip, s.Port,s.DbName))
		if err != nil{
			fmt.Println("sql.open err %v\n", err)
			panic(err.Error())
		}
		err = s.mysql.Ping()
		if err != nil{
			fmt.Printf("ping err:%v\n", err)
			panic(err.Error())
		}
		fmt.Println("Initialize DB success\n")
	})
	rows, err := s.mysql.Query(query, args...)
	if err != nil{
		fmt.Printf("query failed:%v\n", err)
		return nil, err
	}
	columns, err := rows.Columns()
	if err != nil{
		fmt.Printf("Columns err:%v", err)
		return nil,err
	}
	defer rows.Close()
	count := len(columns)
	tableData := make([]map[string]interface{},0)
	values := make([]interface{}, count)
	valuesPtrs := make([]interface{}, count)
	for rows.Next(){
		for i := 0; i< count; i++{
			valuesPtrs[i] = &values[i]
		}
		rows.Scan(valuesPtrs...)
		entry := make(map[string]interface{})
		for i, col := range columns{
			var v interface{}
			val := values[i]
			//fmt.Println(val)
			b, ok := val.([]byte)
			if ok{
				v = string(b)
			}else{
				v = val
			}
			entry[col] = v
			//fmt.Println(col,v)
		}
		tableData = append(tableData, entry)
	}
	return tableData, nil
}
