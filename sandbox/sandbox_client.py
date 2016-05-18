import pika
from .utils import encode
from app import  app


class SandBoxRpcClient(object):
    def __init__(self,  ch):
        self.ch = ch
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.ch, durable=True)

    def call(self, submit_id, result_path, data_path, judge_path):
        app.logger.info("call!! %s %s %s %s" % (submit_id, result_path, data_path, judge_path))
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


