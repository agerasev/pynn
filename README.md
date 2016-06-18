# PyARNN

Asynchronous Recurrent Neural Networks Library for Python3

## Classes

### Node
Base element is Node. It can receive abstract signals and emit new ones. Signals are given with identifier called channel.
+ push(self, chan, signal) - Method. Gives signal to node at channel.
+ emit(chan, signal) - Field imitating function. Release signal to node owner. Are set from outside, but are called only internally.

### Network
Network encapsulates interconnected nodes. Network is also Node. It fetches signals from nodes and delivers them to another ones via links.
+ nodes - List of nodes. Index of node is its id.
+ links - Dictionary contains routes from one node to another. Key is source, value is destination. Sources and destinations are represented by tuple of node id and channel.
+ signals - Queue of signals are waiting to be delivered to destination nodes (or to be emitted). Content structure: (source, signal)
+ __init__(self, **opt) - Sets opt['nodes'] as nodes and opt['links'] as links if exist or empty otherwise. Calls ready()
