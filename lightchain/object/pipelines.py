from abc import ABC, abstractmethod
from typing import Any
from typing import Any, Iterable
from lightchain.chain import Chain
from matchpy import Operation, Arity
from lightchain.object import get_chain

class Pipeline(Operation):
    name = 'Pipeline'
    arity = Arity.polyadic

    def __init__(self, operands : Iterable[Chain], **kwargs):
        super().__init__(operands=operands, **kwargs)
        self.chains = list(map(lambda x : get_chain(x), operands) )

    def __getitem__(self, i) -> Chain:
        return self.chains[i]

    def __len__(self) -> int:
        return len(self.chains)

    @abstractmethod
    def __call__(self, input) -> Any:
        raise NotImplementedError

class SequentialPipeline(Pipeline):
    name = 'Sequential Chain Pipeline'

    def __init__(self, operands : Iterable[Chain], **kwargs):
        super().__init__(operands=operands, **kwargs)

    def __call__(self, input) -> Any:
        out = input
        for chain in self.chains:
            if isinstance(out, dict):
                out = {k : chain(v) for k, v in out.items()}
            else: 
                out = chain(out)
        return out

class ForkPipeline(Pipeline):
    name = 'Forked Chain Pipeline'
    def __init__(self, operands : Iterable[Chain], **kwargs):
        super().__init__(operands=operands, **kwargs)

    def __call__(self, input) -> Any:
        if isinstance(input, dict):
            return {k : self(v) for k, v in input.items()}
        return {chain.name : chain(input) for chain in self.chains}