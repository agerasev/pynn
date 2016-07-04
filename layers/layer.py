#!/usr/bin/python3

import numpy as np

from ..node import Node


class Layer(Node):
	def __init__(self, **opt):
		self.weight = opt.get('weight', None)
		self.memory = []
		self.count = 0
		if self.weight is not None:
			self.grad = np.zeros_like(self.weight)
			self.rate = opt['rate']
			self.clip = opt.get('clip', 5e0)
			if opt.get('adagrad', False):
				eps = opt.get('adagrad.eps', 1e-8)
				self.adagrad = np.zeros_like(self.grad) + eps

	def forward(self, data):
		raise NotImplementedError()

	def backward(self, data):
		raise NotImplementedError()

	def learn(self):
		if hasattr(self, 'grad'):
			np.clip(self.grad, -self.clip, self.clip, out=self.grad)
			if hasattr(self, 'adagrad'):
				self.adagrad += self.grad**2
				self.weight -= self.rate*self.grad/np.sqrt(self.adagrad)
			else:
				self.weight -= self.rate*self.grad
			self.grad = np.zeros_like(self.weight)

	def push(self, chan, signal):
		if chan == 0:  # broadcast
			if signal == 'learn':
				self.learn()
		elif chan == 1:  # input
			self.count += 1
			self.emit(2, self.forward(signal))
		elif chan == 2:  # output
			if self.count <= 0:
				raise Exception('Backward more than forward')
			self.count -= 1
			self.emit(1, self.backward(signal))
