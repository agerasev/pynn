#!/usr/bin/python3

import numpy as np

from .layer import Layer


class Uniform(Layer):
	def __init__(self, **opt):
		Layer.__init__(self, **opt)

	def forward(self, data):
		return data

	def backward(self, data):
		return data


class Bias(Layer):
	def __init__(self, size, **opt):
		if opt.get('state', None) is None:
			opt['state'] = np.zeros(size)
		self.size = size
		Layer.__init__(self, **opt)

	def forward(self, data):
		return data + self.state

	def backward(self, data):
		self.grad += data
		return data


class Tanh(Layer):
	def __init__(self, **opt):
		Layer.__init__(self, **opt)

	def forward(self, data):
		out = np.tanh(data)
		self.memory.append(out)
		return out

	def backward(self, data):
		out = self.memory.pop()
		return data*(1 - out**2)
