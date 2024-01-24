from typing import Any, Callable, Sequence
from uniflow.node import Node
from uniflow.op.op import Op
import copy

class ExpandOp(Op):
    def __init__(self, name: str = None, expand_func: Callable[[int, Any], int] = None):
        super().__init__(name=name)
        self._expand_func = expand_func if expand_func else lambda index, node: index < len(node.value_dict) // 2

    def _split_node(self, node: Node) -> Sequence[Node]:
        dict1, dict2 = dict(), dict()
        value_dict = node.value_dict if type(node.value_dict) == dict else node.value_dict[0]
        for index, key in enumerate(value_dict.keys()):
            if self._expand_func(index, node):
                dict1[key] = copy.deepcopy(value_dict[key])
            else:
                dict2[key] = copy.deepcopy(value_dict[key])
        return [
            Node(name=self.unique_name(), value_dict=dict1, prev_nodes=[node]),
            Node(name=self.unique_name(), value_dict=dict2, prev_nodes=[node]),
        ]

    def __call__(self, nodes: Sequence[Node] | Node) -> Sequence[Node]:
        if isinstance(nodes, Node):
            return self._split_node(nodes)
        else:
            output_nodes = []
            for node in nodes:
                output_nodes.extend(self._split_node(node))
            return output_nodes
