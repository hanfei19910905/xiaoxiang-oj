import json


def encode(submit_id, prob_id, time_limit, mem_limit, source):
    request = {
        "submit_id": submit_id,
        "prob_id": prob_id,
        "time_limit": time_limit,
        "mem_limit": mem_limit,
        "source":source,
    }
    return bytes(json.dumps(request), encoding='utf-8')


def decode(body):
    request =json.loads(str(body, encoding='utf-8'))
    if not {"submit_id", "prob_id", "time_limit", "mem_limit", "source"}.issubset(request.keys()):
        return None, None, None, None, None
    return request["submit_id"], request["prob_id"], request["time_limit"], request["mem_limit"], request["source"]