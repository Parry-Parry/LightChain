from functools import partial
from types import FunctionType
from matchpy import Wildcard, Operation, Arity
from abc import abstractmethod
from typing import Any, Iterable
from lightchain.object import Link, chainable

def get_link(link) -> Any:
    if isinstance(link, Wildcard):
        return link
    if issubclass(type(link), Link):
        return link
    if isinstance(link, FunctionType):
        return chainable(link)
    if isinstance(link, list):
        return SequentialPipeline(link)
    raise ValueError("Passed parameter %s of type %s cannot be coerced into a chain" % (str(link), type(link)))

class Pipeline(Link, Operation):
    name = 'Pipeline'
    arity = Arity.polyadic

    def __init__(self, operands : Iterable, **kwargs):
        super().__init__(operands=operands, **kwargs)
        self.links = [*map(get_link, operands)]

    def __getitem__(self, i) -> Any:
        return self.links[i]

    def __len__(self) -> int:
        return len(self.links)

    @abstractmethod
    def __call__(self, input) -> Any:
        raise NotImplementedError

class SequentialPipeline(Pipeline):
    name = 'Sequential Chain Pipeline'

    def __init__(self, operands : Iterable, **kwargs):
        super().__init__(operands=operands, **kwargs)

    def logic(self, args, **kwargs):
        out = args
        for link in self.links:
            if isinstance(out, dict): out = {k : link(v, **kwargs) for k, v in out.items()}
            else: out = link(out, **kwargs)
        return out

    def __call__(self, *args, **kwargs) -> Any:
        if len(args) == 1: return self.logic(args[0], **kwargs)
        else: return [*map(partial(self.logic, **kwargs), args)]

class ForkPipeline(Pipeline):
    name = 'Forked Chain Pipeline'
    def __init__(self, operands : Iterable, **kwargs):
        super().__init__(operands=operands, **kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        if args:
            if len(args) == 1: return [self(**inp) for inp in args[0]]
            else: return map(self, args)
        elif kwargs:
            if isinstance(args[0], dict): return {k : self(v, **kwargs) for k, v in args[0].items()}
            return {link.name : link(input) for link in self.link}