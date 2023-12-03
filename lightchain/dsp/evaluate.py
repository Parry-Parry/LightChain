from lightchain import Object, Chain
from typing import Any

class Evaluator(Object):
    def __init__(self,
                 valset : Any,
                 inner_eval : Any):
        self.valset = valset
        self._inner_eval = inner_eval
    
    def _run_val(self, chain : Chain, inner_kwargs : Any = None):
        output = [chain(x) for x, _ in self.valset]
        target = [y for _, y in self.valset]
        return self._inner_eval(output, target, **inner_kwargs)