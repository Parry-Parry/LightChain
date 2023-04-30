from abc import ABC, abstractmethod
from ..prompt import Prompt
from typing import Union, Optional

"""
Notion would be that you can move parsing of output into each chain given that you have a specific CoT use case.
"""

class Chain(ABC):
    def __init__(self, memory=None, prompt : Optional[Prompt] = None):
        self.memory = memory
        self.prompt = prompt
        self.params = prompt.params
    
    @abstractmethod
    def _get_keys(self, input : str) -> dict:
        raise NotImplementedError

    def _parse(self, input : Union[str, dict]) -> str:
        if isinstance(input, str):
            return self.get_prompt_keys(input)
        elif isinstance(input, dict):
            return input
        else:
            raise TypeError(f'Input type {type(input)} not supported')
        
    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class SequentialChain(Chain):
    def __init__(self, chains, memory=None):
        super().__init__(memory)
        self.chains = chains
    
    def __call__(self, input):
        out = input
        for link in self.chain:
            out = link(out)
        return out