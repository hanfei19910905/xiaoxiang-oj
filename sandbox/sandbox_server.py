import pika
import time
from app.models import Submission, Problem
from .utils import decode
from .sandbox_executor import SandBoxExecutor


class SandBoxService(object):

    @staticmethod
    def run(ch):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=ch, durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            ch.basic_ack(delivery_tag = method.delivery_tag)
            submit_id , prob_id, time_limit, mem_limit, source = decode(body)
            if submit_id is None:
                print("Fail!!!!")
                return
            prob = Problem.select().where(Problem.id == prob_id).get()
            ret = SandBoxExecutor.execute(submit_id, time_limit, mem_limit, source, prob.input, prob.output)
            submit = Submission.select().where(Submission.id==submit_id).get()
            submit.status = ret
            submit.save()

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback,
                              queue=ch)

        channel.start_consuming()