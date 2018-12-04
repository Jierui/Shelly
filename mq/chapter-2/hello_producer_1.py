# _*_ coding=utf-8 _*_
# import sys
import pika
# 带有确认功能的生成者
# credentials 证书，文凭

# 建立代理服务器
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)

# 获得信道
channel = conn_broker.channel()


def confirm_handler(frame):
    if type(frame.method) == pika.spec.Confirm.SelectOk:
        print("Channel in 'confirm' mode")
    elif type(frame.method) == pika.spec.Basic.Nack:
        if frame.method.delivery_tag in msg_ids:
            print("Message Lost")
    elif type(frame.method) == pika.spec.Basic.Ack:
        if frame.method.delivery_tag in msg_ids:
            print("Confirm received")
            msg_ids.remove(frame.method.delivery_tag)


# 将信道模式设置为confirm模式
channel.confirm_delivery()
msg_ids = []

# msg = sys.argv[1]
msg = "hello world"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

# 发布消息
channel.basic_publish(body=msg, exchange="hello-exchange",
                      properties=msg_props, routing_key="hola")
msg_ids.append(len(msg_ids) + 1)
channel.close()
