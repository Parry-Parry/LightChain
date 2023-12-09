from abc import abstractmethod
from typing import Any
from functools import wraps
from forge import fsignature

class Link(object):
    """
    A base class for creating pipeline operations.
    It provides methods for chaining operations in a sequential or forked manner.
    
    Attributes:
        name (str): The name of the Link object. Default is 'Link'.
        description (str): The description of the Link object. Default is 'A Link'.
        signature (str): The signature of the logic method. It is set in the initializer.
    """

    name = 'Link'
    description = 'A Link'
    def __init__(self, **kwargs) -> None:
        """
        Initializes the Link object. Any keyword arguments passed are set as attributes of the object.
        """
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
    
    @abstractmethod
    def logic(self, *args : Any, **kwargs : Any) -> Any:
        raise NotImplementedError
    
    def __call__(self, *args, **kwargs) -> Any:
        self.logic(*args, **kwargs)

def chainable(cls, call='__call__', name='External Object', description="We don't know what this is but it's probably important"):
    """
    Wraps a class to make it chainable in a pipeline. The wrapped class inherits from the Link class.

    Args:
        cls (type): The class to be wrapped.
        call (str or callable, optional): The method of the class to be called when the object is called. If a callable is passed, it is used directly. Defaults to '__call__'.
        name (str, optional): The name of the Link object. 
        description (str, optional): The description of the Link object.

    Returns:
        Wrapper: The wrapped class.
    """
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
