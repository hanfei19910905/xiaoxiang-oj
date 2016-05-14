if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from box import judge
data_fd = open("data.csv", 'r')
result_fd = open("result.csv", 'r')

data_id = 0
def gen_data(data_fd):
    data, ids = [], []
    first = True
    for f in data_fd:
        if first :
            first = False
            continue
        li = f.split(',', 1)
        if len(li) != 2:
            print('at least two columns in csv file.')
            exit(0)
        _id, _data = li[0], li[1]
        data.append(_data)
        try:
            ids.append(int(_id))
        except ValueError:
            print 'Invalid Input'
            exit(0)
    return ids, data

_ids1, _data = gen_data(data_fd)
_ids2, _result = gen_data(result_fd)

def check(ids1, ids2):
    if len(ids1) != len(ids2):
        print "row number doesn't match"
        exit(0)

    for i, id in enumerate(ids1):
        if id != ids2[i]:
            print "row number doesn't match"
            exit(0)

check(_ids1,_ids2)

print judge.evaluate(_ids1, _result, _data)
