# _*_ coding=utf-8 _*_
import sys
import pika

# credentials 证书，文凭

# 建立代理服务器
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)

# 获得信道
channel = conn_broker.channel()

# 声明交换器
# passive=TRUE 如果队列存在，成功返回，如果队列不存在，不会主动创建，返回失败，可以用来查询队列是否存在
# auto_delete 当最后一个消费者取消队列时，队列移除
# exclusive = true 队列变为私有的，此时你的应用程序才会消费队列消息，对于限制一个队列只有一个消费者的时候很有帮助
# type 交换器的四种类型 分别为 direct,topic,fanout(类似广播),headers
# durable 决定了RabbitMQ是否在崩溃或者重启时重新创建队列或者交换器
# 持久化，如果消息要从重启中恢复 1.投递模式 delivery mode=2; 2.发送到持久化交换器； 3. 到达持久化队列
channel.exchange_declare(exchange="hello-exchange", exchange_type="direct",
                         passive=False, durable=True, auto_delete=False)

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

# 发布消息
channel.basic_publish(body=msg, exchange="hello-exchange",
                      properties=msg_props, routing_key="hola")
