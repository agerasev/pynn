#!/usr/bin/python3

import numpy as np

from ..node import Node


class Fork(Node):
	def __init__(self, **opt):
		Node.__init__(self, **opt)
		self.slot = [None]*2

	def clear(self):
		for i in range(2):
			self.slot[i] = None

	def push(self, chan, signal):
		if chan == 1:
			for i in range(2):
				self.emit(2 + i, signal)
		elif chan == 2 or chan == 3:
			i = chan - 2
			if self.slot[i] is not None:
				raise Exception('slot is not empty')
			self.slot[i] = signal
			if self.slot[0] is not None and self.slot[1] is not None:
				self.emit(1, self.slot[0] + self.slot[1])
				self.clear()
		elif chan == 0:
			if signal == 'clear':
				self.clear()


class Depot(Node):
	def __init__(self, **opt):
		Node.__init__(self, **opt)
		self.weight = opt['weight']
		self.clear()

	def clear(self):
		self.slot = None
		self.count = 0

	def push(self, chan, signal):
		if chan == 1:
			if self.slot is not None:
				raise Exception('slot is not empty')
			self.slot = signal
		elif chan == 2:
			if self.count > 1:
				self.emit(1, signal)
				self.count -= 1
			else:
				self.count = 0
		elif chan == 0:
			if signal == 'emit':
				self.slot = self.weight
			elif signal == 'emit.error':
				if self.slot is not None:
					self.emit(1, np.zeros_like(self.slot))
			elif signal == 'release':
				if self.slot is None:
					raise Exception('slot is empty')
				self.emit(2, self.slot)
				self.slot = None
				self.count += 1
			elif signal == 'clear':
				self.clear()
