import queue 

class NodeType(type):
    NodeClass: list = []
    EventQueue: queue.Queue = queue.Queue()

    def __call__(cls, base, *args, **kwargs):
        inst = super().__call__(cls, base, *args, **kwargs)
        NodeType.NodeInstance += [inst]
        inst.set_event_queue(NodeType.EventQueue)
        return inst

class Node(metaclass = NodeType):
    def __init__(self):
        self.parent : "Node" 
        self.event_queue: queue.Queue

    def set_event_queue(self, event_queue):
        self.event_queue = event_queue