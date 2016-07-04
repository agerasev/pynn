#!/usr/bin/python3

from queue import Queue

from .node import Node


class Network(Node):
	class Fetcher:
		def __init__(self, outer, index):
			self.outer = outer
			self.index = index

		def __call__(self, chan, signal):
			self.outer.queue.put(((self.index, chan), signal))

	def run(self):
		while not self.queue.empty():
			(src, signal) = self.queue.get()
			dst = self.links[src]
			# print(dst)
			if dst[0] < 0:
				self.emit(dst[1], signal)
			else:
				try:
					self.nodes[dst[0]].push(dst[1], signal)
				except Exception as e:
					e.args = ('node %d: ' % dst[0]) + str(e.args[0]),
					raise

	def __init__(self, nodes, paths, **opt):
		Node.__init__(self)
		self.nodes = nodes

		self.paths = paths
		self.links = {}
		for src, dst in paths:
			self.links[src] = dst
			self.links[dst] = src

		self.queue = Queue()
		for i, node in enumerate(self.nodes):
			node.emit = self.Fetcher(self, i)

	def push(self, chan, signal):
		if chan == 0:  # broadcast
			for node in self.nodes:
				node.push(0, signal)
		else:
			self.queue.put(((-1, chan), signal))
		self.run()
