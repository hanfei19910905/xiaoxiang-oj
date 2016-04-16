import pika
import time
from app.models import Submission, User
from.utils import decode


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
            submit_id , user_id, time_limit, mem_limit, source = decode(body)
            if submit_id is None:
                print("Fail!!!!")
                return
            time.sleep(3)
            submit = Submission.select().where(Submission.id==submit_id).get()
            submit.status = 1
            submit.save()

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback,
                              queue=ch)

        channel.start_consuming()