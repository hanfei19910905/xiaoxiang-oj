import pika
from app.models import Submission, ProbUserStatic
from app import db
from .utils import decode
from .sandbox_executor import SandBoxExecutor


class SandBoxService(object):

    @staticmethod
    def local_exec(submit_id, result_path, data_path, judge_path):
        print("Exec!!!", submit_id, result_path, data_path, judge_path)
        if submit_id is None:
            print("Fail!!!!")
            return
        submit = Submission.query.filter_by(id = submit_id).first()
        if submit is not None:
            db.session.status = 'judging'
            db.session.commit()
        else:
            db.session.status = 'failed, system error!'
            db.session.commit()
            return
        ret, score = SandBoxExecutor.execute(submit_id, result_path, data_path, judge_path)
        submit.status = ret
        if ret == 'success':
            print('score', score)
            submit.score = score
            static = ProbUserStatic.query.filter_by(user_id = submit.user_id).filter_by(prob_id = submit.prob_id).first()
            if static is None:
                static = ProbUserStatic(user_id = submit.user_id, prob_id = submit.prob_id, score = score)
                db.session.add(static)
            elif static.score < score:
                static.score = score
        db.session.commit()

    @staticmethod
    def run(ch):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=ch, durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            ch.basic_ack(delivery_tag = method.delivery_tag)
            submit_id , result_path, data_path, judge_path = decode(body)
            SandBoxService.local_exec(submit_id , result_path, data_path, judge_path )

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback,
                              queue=ch)

        channel.start_consuming()