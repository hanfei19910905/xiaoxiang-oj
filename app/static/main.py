if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from box import judge
data_fd = open("data.csv", 'r')
result_fd = open("result.csv", 'r')

data_id = 0
data = []
for f in data_fd:
    data.append(f)
    data_id += 1

result_id = 0
result = []
for f in result_fd:
    result.append(f)
    result_id += 1

if data_id != result_id:
    print 'line number doesnot match!'
    exit(0)

print judge.evaluate([i for i in range(0, data_id)], result, data)
