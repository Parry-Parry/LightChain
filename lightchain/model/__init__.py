from abc import ABC, abstractmethod

"""
Stupidly simple wrapper, will implement async wrapper later.
"""

class Model(ABC):
    def __init__(self, model) -> None:
        super().__init__()
        self.model = model 
    
    @abstractmethod
    def __call__(self, *args, **kwargs) -> str:
        raise NotImplementedError

