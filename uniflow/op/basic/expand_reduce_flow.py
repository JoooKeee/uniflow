from uniflow.flow.flow import Flow
from expand_op import ExpandOp
from reduce_op import ReduceOp
from uniflow.node import Node

class ExpandReduceFlow(Flow):

    def __init__(self, name: str = None):
        super().__init__()
        self.expand_op = ExpandOp()
        self.reduce_op = ReduceOp()

    def run(self, input_node: Node) -> Node:
        expanded_nodes = self.expand_op(input_node)
        reduced_node = self.reduce_op(expanded_nodes)
        return reduced_node