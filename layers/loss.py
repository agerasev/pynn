#!/usr/bin/python3

import numpy as np

from .scal import *


class EuclideanLoss(Uniform):
	def __init__(self, **opt):
		Uniform.__init__(self, **opt)
		self.loss = 0.0

	def forward(self, data):
		self.memory.append(data)
		return data

	def backward(self, data):
		err = self.memory.pop() - data
		self.loss += 0.5*np.sum(err**2)
		return err


class CrossEntropyLoss(Tanh):
	def __init__(self, **opt):
		Tanh.__init__(self, **opt)
		self.loss = 0.0

	def backward(self, data):
		out = self.memory.pop()
		self.loss -= np.sum((1 + data)*np.log(1 + out) + (1 - data)*np.log(1 - out))
		return out - data


class SoftmaxLoss(Softmax):
	def __init__(self, **opt):
		Softmax.__init__(self, **opt)
		self.loss = 0.0

	def forward(self, data):
		out = Softmax.forward(self, data)
		self.memory.append(out)
		return out

	def backward(self, data):
		out = self.memory.pop()
		if isinstance(data, int):
			self.loss += -np.log(out[data])
			err = np.copy(out)
			err[data] -= 1.0
		else:
			self.loss -= np.log(np.dot(out, data))
			err = out - data
		return err
