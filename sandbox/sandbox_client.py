import pika
from .utils import encode


class SandBoxRpcClient(object):
    def __init__(self,  ch):
        self.ch = ch
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.ch, durable=True)

    def call(self, submit_id, result_path, data_path, judge_path):
        print('data_path', data_path)
        rpc_body = encode(submit_id, result_path, data_path, judge_path)
        for i in range(2):
            try:
                self.channel.basic_publish(exchange='',
                                           routing_key=self.ch,
                                           properties=pika.BasicProperties(
                                                 delivery_mode=2,
                                                 ),
                                           body=rpc_body)
                return
            except pika.exceptions.ConnectionClosed:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host='localhost'))

                self.channel = self.connection.channel()

                self.channel.queue_declare(queue=self.ch, durable=True)

        #convert to local judge. that's a sync way!
        from .sandbox_server import SandBoxService
        SandBoxService.local_exec(submit_id, result_path, data_path, judge_path)


