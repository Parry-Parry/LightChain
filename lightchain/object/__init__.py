from abc import ABC, abstractmethod

"""
Stupidly simple wrapper, will implement async wrapper later.
"""

class Object(ABC):
    def __init__(self, component, name='Entity', description='Some Standard Component') -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.model = component
    
    @abstractmethod
    def __call__(self, *args, **kwargs) -> str:
        raise NotImplementedError

