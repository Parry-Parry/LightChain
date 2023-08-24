import types
from matchpy import Wildcard
from abc import ABC, abstractmethod
from typing import Any, Iterable
from matchpy import Operation, Arity

class Object(ABC):
    name = 'Object'

    def __init__(self, name : str = 'Entity', description : str = 'Some Standard Entity') -> None:
        super().__init__()
        self.name = name
        self.description = description

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        raise NotImplementedError
    
    def __rshift__(self, right):
        return SequentialPipeline(self, right)
    
    def __lshift__(self, left):
        return SequentialPipeline(left, self)
    
    def __or__(self, right):
        return ForkPipeline(self, right)

def get_chain(chain) -> Any:
    from lightchain.prompt import Prompt
    from lightchain.chain import Chain, LambdaChain
    if isinstance(chain, Wildcard):
        return chain
    if isinstance(chain, Chain):
        return chain
    if isinstance(chain, Prompt):
        return chain
    if issubclass(type(chain), Object):
        return chain
    if isinstance(chain, list):
        return SequentialPipeline(chain)
    if isinstance(chain, types.FunctionType):
        return LambdaChain(chain)
    
    raise ValueError("Passed parameter %s of type %s cannot be coerced into a chain" % (str(chain), type(chain)))

class Pipeline(Object, Operation):
    name = 'Pipeline'
    arity = Arity.polyadic

    def __init__(self, operands : Iterable, **kwargs):
        super().__init__(operands=operands, **kwargs)
        self.chains = list(map(lambda x : get_chain(x), operands) )

    def __getitem__(self, i) -> Any:
        return self.chains[i]

    def __len__(self) -> int:
        return len(self.chains)

    @abstractmethod
    def __call__(self, input) -> Any:
        raise NotImplementedError

class SequentialPipeline(Pipeline):
    name = 'Sequential Chain Pipeline'

    def __init__(self, operands : Iterable, **kwargs):
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
    def __init__(self, operands : Iterable, **kwargs):
        super().__init__(operands=operands, **kwargs)

    def __call__(self, input) -> Any:
        if isinstance(input, dict):
            return {k : self(v) for k, v in input.items()}
        return {chain.name : chain(input) for chain in self.chains}