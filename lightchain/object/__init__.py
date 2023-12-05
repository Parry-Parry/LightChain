from abc import abstractmethod
from typing import Any
from functools import wraps

class Object(object):
    name = 'Object'
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        raise NotImplementedError
    
    def __rshift__(self, right):
        from lightchain.object.ops import SequentialPipeline
        return SequentialPipeline(self, right)
    
    def __lshift__(self, left):
        from lightchain.object.ops import SequentialPipeline
        return SequentialPipeline(left, self)
    
    def __or__(self, right):
        from lightchain.object.ops import ForkPipeline
        return ForkPipeline(self, right)

def chainable(cls):
    @wraps(cls)
    class Wrapper(Object):
        name = cls.__name__
        def __init__(self, *args, **kwargs) -> None:
            self._obj = cls(*args, **kwargs)
        
        def __call__(self, *args, **kwargs) -> Any:
            return self._obj(*args, **kwargs)
    return Wrapper