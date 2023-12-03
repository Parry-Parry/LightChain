from abc import abstractmethod
from typing import Any

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