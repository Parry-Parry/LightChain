from abc import ABC, abstractmethod
from typing import Any
from lightchain.object.pipelines import SequentialPipeline, ForkPipeline

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

class Model(Object):
    name = 'Model'
    def __init__(self, 
                 model : Any, 
                 generation_kwargs : dict = {}, 
                 name : str = 'Model', 
                 description : str = 'Some Standard Model') -> None:
        super().__init__(name=name, description=description)
        self.model = model
        self.generation_kwargs = generation_kwargs