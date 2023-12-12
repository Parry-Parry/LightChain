from abc import abstractmethod
from typing import Any, Union
from functools import wraps, partial
from inspect import signature

class Link(object):
    """
    A base class for creating Chain operations.
    It provides methods for chaining operations in a sequential or forked manner.
    
    Attributes:
        name (str): The name of the Link object. Default is 'Link'.
        description (str): The description of the Link object. Default is 'A Link'.
        signature (str): The signature of the logic method. It is set in the initializer.
    """

    __name__ = 'Link'
    __doc__ = 'A Link'
    def __init__(self, **kwargs) -> None:
        """
        Initializes the Link object. Any keyword arguments passed are set as attributes of the object.
        """
        self._signature = signature(self.logic)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __rshift__(self, right):
        from lightchain.link.ops import SequentialChain
        return SequentialChain(self, right)
    
    def __lshift__(self, left):
        from lightchain.link.ops import SequentialChain
        return SequentialChain(left, self)
    
    def __or__(self, right):
        from lightchain.link.ops import ForkChain
        return ForkChain(self, right)
    
    @property
    def signature(self):
        return self._signature
    
    @abstractmethod
    def logic(self, *args : Any, **kwargs : Any) -> Any:
        """
        The logic of the Link object. It is implemented in a subclass.
        """
        raise NotImplementedError
    
    def __call__(self, *args, **kwargs) -> Any:
        self.logic(*args, **kwargs)

def chainable(cls : Union[callable, Any], call='__call__', **func_kwargs):
    """
    Wraps a class to make it chainable in a Chain. The wrapped class inherits from the Link class.

    Args:
        cls (callable or Any): The class or function to be wrapped.
        call (str or callable, optional): The method of the class to be called when the object is called. If a callable is passed, it is used directly. Defaults to '__call__'.
        name (str, optional): The name of the Link object. 
        description (str, optional): The description of the Link object.

    Returns:
        Wrapper: The wrapped class.
    """

    @wraps(cls)
    class Wrapper(Link):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__()
            if isinstance(cls, callable):
                self.obj, self.logic = cls, cls
            else:
                self.obj = cls(*args, **kwargs)
                self.logic = getattr(self.obj, call) 
                self._signature = signature(self.logic)
            if kwargs: self.logic = partial(self.logic, **func_kwargs)
    return Wrapper() if isinstance(cls, callable) else Wrapper
