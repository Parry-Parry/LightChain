from abc import ABC, abstractmethod
from typing import Any
from lightchain.pipeline import SequentialPipeline, ForkPipeline

class Object(ABC):
    name = 'Object'

    def __init__(self, name='Entity', description='Some Standard Entity') -> None:
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

    def __init__(self, model, model_kwargs = {}, name='Model', description='Some Standard Model') -> None:
        super().__init__(name=name, description=description)
        self.model = model
        self.model_kwargs = model_kwargs