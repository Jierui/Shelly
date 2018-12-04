# _*_ coding=utf-8 _*_
import pika
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)

# 获取信道
channel = conn_broker.channel()

# 声明交换器
channel.exchange_declare(exchange="hello-exchange", exchange_type="direct",
                         passive=False, auto_delete=False, durable=True)

# 声明队列
channel.queue_declare(queue="hello-queue")
# 绑定交换器
channel.queue_bind(queue="hello-queue", exchange="hello-exchange", routing_key="hola")

# 用户处理传入消息的函数


def msg_consumer(channel_local, method, header, body):
    channel_local.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer")
        # 停止消费
        channel.stop_consuming()
    else:
        print(header)
        print(body)
    return


# 订阅消费者
channel.basic_consume(msg_consumer, queue="hello-queue", consumer_tag="hello-consumer")
# 开始消费
channel.start_consuming()
