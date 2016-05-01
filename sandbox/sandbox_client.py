import pika
from .utils import encode


class SandBoxRpcClient(object):
    def __init__(self,  ch):
        self.ch = ch
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=ch, durable=True)

    def call(self, submit_id, result_path, data_path, judge_path):

        rpc_body = encode(submit_id, result_path, data_path, judge_path)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.ch,
                                   properties=pika.BasicProperties(
                                         delivery_mode=2,
                                         ),
                                   body=rpc_body)
