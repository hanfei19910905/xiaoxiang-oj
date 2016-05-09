#! /usr/bin/python
import sys
import math
def rmse(labels,predicted):
	r = 0.0
	for i in range(len(labels)):
		r += (predicted[i] - labels[i]) * (predicted[i] - labels[i])
	return math.sqrt(r/len(labels))
def evaluate(ids,true_values,predict_values):
	labels = []
	predicted = []
	for i in range(len(ids)):
		labels.append(float(true_values[i]))
		predicted.append(float(predict_values[i]))
	return rmse(labels,predicted)

