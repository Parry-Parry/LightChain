from abc import abstractmethod
import types
from typing import Any, Iterable
from matchpy import Wildcard, Operation, Arity
from chain import Chain, LambdaChain

def get_chain(chain) -> Chain:

    if isinstance(chain, Wildcard):
        return chain
    if isinstance(chain, Chain):
        return chain
    if isinstance(chain, list):
        return SequentialPipeline(chain)
    if isinstance(chain, types.FunctionType):
        return LambdaChain(chain)
    
    raise ValueError("Passed parameter %s of type %s cannot be coerced into a chain" % (str(chain), type(chain)))

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
            out = chain(out)
        return out

class ForkPipeline(Pipeline):
    name = 'Forked Chain Pipeline'

    def __init__(self, operands : Iterable[Chain], **kwargs):
        super().__init__(operands=operands, **kwargs)

    def __call__(self, input) -> Any:
        return {chain.name : chain(input) for chain in self.chains}

