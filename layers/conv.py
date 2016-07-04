#!/usr/bin/python

import numpy as np

from .layer import Layer


class Matrix(Layer):
	def __init__(self, size, **opt):
		self.size = size
		if opt.get('weight', None) is None:
			opt['weight'] = 0.01*np.random.randn(size[0], size[1])
		Layer.__init__(self, **opt)

	def forward(self, data):
		self.memory.append(data)
		return np.dot(data, self.weight)

	def backward(self, data):
		inp = self.memory.pop()
		self.grad += np.outer(inp, data)
		return np.dot(self.weight, data)
