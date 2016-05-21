import pika
from .utils import encode
from app import app, celery


class SandBoxRpcClient(object):
    def __init__(self,  ch):
        self.ch = ch
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.ch, durable=True)

    def call(self, submit_id, result_path, data_path, judge_path):
        rpc_body = encode(submit_id, result_path, data_path, judge_path)
        for i in range(5):
            try:
                app.logger.info("try!! %s %s %s %s" % (submit_id, result_path, data_path, judge_path))
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

        app.logger.info("local!! %s %s %s %s" % (submit_id, result_path, data_path, judge_path))
        #convert to local judge. that's a sync way!
        from .sandbox_server import SandBoxService
        SandBoxService.local_exec(submit_id, result_path, data_path, judge_path)

from .sandbox_server import SandBoxService

@celery.task
def async_call(submit_id, result_path, data_path, judge_path):
    SandBoxService.local_exec(submit_id, result_path, data_path, judge_path)