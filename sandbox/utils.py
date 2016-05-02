import json


def encode(submit_id, result_path, data_path, judge_path):
    request = {
        "submit_id": submit_id,
        "result_path": result_path,
        "data_path": data_path,
        "judge_path": judge_path,
    }
    return bytes(json.dumps(request), encoding='utf-8')


def decode(body):
    request =json.loads(str(body, encoding='utf-8'))
    if not {"submit_id", "result_path", "data_path", "judge_path"}.issubset(request.keys()):
        return None, None, None, None, None
    return request["submit_id"], request["result_path"], request["data_path"], request["judge_path"]