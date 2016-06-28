#!/usr/bin/python3

import numpy as np

from ..node import Node


class Layer(Node):
	def __init__(self, **opt):
		self.state = opt.get('state', None)
		self.memory = []
		self.count = 0
		if self.state is not None:
			self.grad = np.zeros_like(self.state)
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
				self.state -= self.rate*self.grad/np.sqrt(self.adagrad)
			else:
				self.state -= self.rate*self.grad
			self.grad = np.zeros_like(self.state)

	def push(self, chan, signal):
		if chan == 0:  # broadcast
			if signal == 'learn':
				self.learn()
		elif chan == 1:  # input
			self.count += 1
			self.emit(2, self.forward(signal))
		elif chan == 2:  # output
			if self.count > 0:
				self.count -= 1
				self.emit(1, self.backward(signal))
