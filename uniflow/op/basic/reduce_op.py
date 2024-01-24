from typing import Sequence, Callable

from uniflow.node import Node
from uniflow.op.op import Op

class ReduceOp(Op):

    def __init__(self, name: str = None, combine_func: Callable[[dict, dict], dict] = None):
        super().__init__(name=name)
        self._combine_func = combine_func if combine_func else self._default_combine_func

    def _default_combine_func(self, dict1, dict2):
        combined_dict = {}
        for (k1, v1), (k2, v2) in zip(dict1.items(), dict2.items()):
            combined_key = f"{k1} {k2}"
            combined_value = f"{v1} {v2}"
            combined_dict[combined_key] = combined_value
        return combined_dict

    def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:
        if len(nodes) != 2:
            raise ValueError("ReduceOp expects exactly two input nodes")

        expand_1, expand_2 = nodes
        value_dict_1 = expand_1.value_dict
        value_dict_2 = expand_2.value_dict

        combined_dict = self._combine_func(value_dict_1, value_dict_2)

        reduce_1 = Node(name=self.unique_name(), value_dict=combined_dict, prev_nodes=[expand_1, expand_2])

        return [reduce_1]
