#! /usr/bin/python
import sys
def f1(labels,predicted):
	r = 0.0
	for i in range(len(labels)):
		n = 0.0;
		for m in predicted[i]:
			if m in labels[i]:
				n += 1.0;
		if n != 0.0:
			precision = n / len(predicted[i])
			recall = n /len(labels[i])
			r += 1.0/(1.0/precision + 1.0/recall)
	return r/len(labels)
def evaluate(ids,true_values,predict_values):
	labels = []
	predicted = []
	for i in range(len(ids)):
		viewed = set()
		ret = set()
		seg = true_values[i].strip().split(",")
		for m in seg :
			viewed.add(m)
		labels.append(m)
		seg = predict_values[i].strip().split(",")
		for m in seg:
			ret.add(m)
		predicted.append(m)
	return f1(labels,predicted)

