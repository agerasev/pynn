#!/usr/bin/python3

from queue import Queue

from .node import Node


class Network(Node):
	class Fetcher:
		def __init__(self, outer, index):
			self.outer = outer
			self.index = index

		def __call__(self, chan, signal):
			self.outer.signals.put(((self.index, chan), signal))

	def ready(self):
		for i, node in enumerate(self.nodes):
			node.emit = self.Fetcher(self, i)

	def run(self):
		while not self.signals.empty():
			(src, signal) = self.signals.get()
			dst = self.links[src]
			if dst[0] < 0:
				self.emit(dst[1], signal)
			else:
				self.nodes[dst[0]].push(dst[1], signal)

	def __init__(self, **opt):
		Node.__init__(self)
		self.nodes = opt.get('nodes', [])
		self.links = opt.get('links', {})
		self.signals = Queue()
		self.ready()

	def push(self, chan, signal):
		if chan == 0:  # broadcast
			for node in self.nodes:
				node.push(0, signal)
		else:
			self.outer.signal.put(((-1, chan), signal))
			self.run()
