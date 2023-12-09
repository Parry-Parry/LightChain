from abc import abstractmethod
from typing import Any
from functools import wraps
from forge import fsignature

class Link(object):
    name = 'Link'
    description = 'A Link'
    def __init__(self, **kwargs) -> None:
        self.signature = fsignature(self.logic)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __rshift__(self, right):
        from lightchain.link.ops import SequentialPipeline
        return SequentialPipeline(self, right)
    
    def __lshift__(self, left):
        from lightchain.link.ops import SequentialPipeline
        return SequentialPipeline(left, self)
    
    def __or__(self, right):
        from lightchain.link.ops import ForkPipeline
        return ForkPipeline(self, right)
    
    def logic(self, *args : Any, **kwargs : Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        self.logic(*args, **kwargs)

def chainable(cls, call='__call__', name='External Object', description="We don't know what this is but it's probably important"):
    @wraps(cls)
    class Wrapper(Link):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(name=name, description=description)
            self.obj = cls(*args, **kwargs)
            self.func = getattr(self.obj, call) if not isinstance(call, callable) else call
            self.signature = fsignature(self.func)
    
        def logic(self, *args : Any, **kwargs : Any) -> Any:
            return self.func(*args, **kwargs)
    return Wrapper

class SkipLink(Link):
    name = 'Skip'
    signature = 'I'
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def logic(self, *args, **kwargs) -> Any:
        return args, kwargs
