#!/usr/bin/python3


class Node:
	def __init__(self, **opt):
		self.emit = None

	def push(self, chan, signal):
		raise NotImplementedError()
