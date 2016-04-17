import os
import subprocess


class SandBoxExecutor(object):
    @staticmethod
    def compare(user_output, std_output):
        print("output", user_output, std_output)
        user_output = ''.join(user_output.split('\n'))
        std_output = ''.join(std_output.split('\n'))
        return user_output == std_output

    @staticmethod
    def execute(submit_id, time_limit, mem_limit, source, input, output):
        box_id = submit_id % 100
        init_cmd = 'isolate --init --box-id=%d' % box_id
        print("Exec init_cmd: ", init_cmd)
        ret = os.system(init_cmd)
        if ret != 0:
            print("Init Error")
            return -1
        box_path = '/tmp/box/' + str(box_id) + '/box/'
        source_path = box_path + 'tmp.py'
        file_fd = open(source_path, 'w')
        file_fd.write(source)
        file_fd.close()

        input_path = box_path + 'tmp_input'
        file_fd = open(input_path, 'w')
        file_fd.write(input)
        file_fd.close()

        exec_cmd = '/usr/local/bin/isolate -e -p=1 --box-id=' + str(box_id) + ' --run /usr/bin/python tmp.py' + ' -t ' + str(time_limit / 1000.0) + " -i tmp_input -o tmp_output --meta=run.log"
        print("Exec exec_cmd: ", exec_cmd)
        ret_code = os.system(exec_cmd)
        #ret_code = popen.wait()
        if ret_code != 0:
            print ("Exec Error")
            return -1

        output_path = box_path + 'tmp_output'
        file_fd = open(output_path, 'r')
        user_output = file_fd.read()

        ret_code = SandBoxExecutor.compare(user_output, output)
        if ret_code:
            return 1
        return 2


