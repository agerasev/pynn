#!/usr/bin/python3

from ..node import Node


class Fork(Node):
	def __init__(self, **opt):
		Node.__init__(self, **opt)
		self.slot = [None]*2

	def clear(self):
		self.slot[0] = None
		self.slot[1] = None

	def push(self, chan, signal):
		if chan == 1:
			self.emit(2, signal)
			self.emit(3, signal)
		elif chan == 2 or chan == 3:
			i = chan - 2
			if self.slot[i] is not None:
				raise Exception('slot is not empty')
			self.slot[i] = signal
			if self.slot[0] is not None and self.slot[1] is not None:
				self.emit(1, self.slot[0] + self.slot[1])
				self.clear()
		elif chan == 0:
			if signal == 'clear.slot':
				self.clear()
