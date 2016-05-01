import os
from app import app


class SandBoxExecutor(object):
    @staticmethod
    def compare(user_output, std_output):
        print("output", user_output, std_output)
        user_output = ''.join(user_output.split('\n'))
        std_output = ''.join(std_output.split('\n'))
        return user_output == std_output

    @staticmethod
    def execute(submit_id, result_path, data_path, judge_path):
        box_id = submit_id % 100
        init_cmd = 'isolate --init --box-id=%d' % box_id
        print("Exec init_cmd: ", init_cmd)
        ret = os.system(init_cmd)
        if ret != 0:
            print("Init Error")
            return "system error! create sandbox error! please submit again!", None
        box_path = '/tmp/box/' + str(box_id) + '/box/'
        os.symlink(result_path, os.path.join(box_path, 'result.csv'))
        os.symlink(data_path, os.path.join(box_path, 'data.csv'))
        os.symlink(judge_path, os.path.join(box_path, 'judge.py'))
        print('PYPY', app.config['PY_PATH'])
        os.symlink(app.config['PY_PATH'], os.path.join(box_path, 'main.py'))

        exec_cmd = '/usr/local/bin/isolate -e --box-id=' + str(box_id) + ' --run /usr/bin/python main.py' + " -t 60 -o res.log --meta=run.log"
        print("Exec exec_cmd: ", exec_cmd)
        ret_code = os.system(exec_cmd)
        if ret_code != 0:
            print ("Exec Error")
            return "Judge Exec error!!", None

        output_path = os.path.join( box_path , 'res.log')
        file_fd = open(output_path, 'r')
        user_output = file_fd.readline(limit = 1)
        try:
            score = float(user_output)
        except ValueError:
            return user_output, None

        return 'success', score


