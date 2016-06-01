if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from box import judge
data_fd = open("data.csv", 'r')
result_fd = open("result.csv", 'r')


def gen_data(data_fd):
    data, ids = [], []
    first = True
    id_idx, target_idx = -1, -1
    di = ','
    for j, f in enumerate(data_fd):
        if first :
            if f.find(',') != -1:
                li = f.split(',')
            else:
                li = f.split('\t')
                di = '\t'
            for i, st in enumerate(li):
                if st.lower() == 'id':
                    id_idx = i
                elif st.lower() == 'target':
                    target_idx = i
            first = False
            continue
        li = f.split(di)
        if len(li) < 1:
            print('at least one column in csv file.')
            exit(0)
        _data = li[target_idx]
        data.append(_data)
        if id_idx == -1:
            _id = j
        else:
            _id = int(li[id_idx])
        try:
            ids.append(int(_id))
        except ValueError:
            print 'Invalid ID'
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

try:
    print judge.evaluate(_ids1, _data, _result)
except Exception as e:
    print e
