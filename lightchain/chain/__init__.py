from abc import ABC, abstractmethod

from lightchain.prompt import Prompt
from ..prompt import Prompt
from typing import Union, Optional

"""
Notion would be that you can move parsing of output into each chain given that you have a specific CoT use case.
"""

class Chain(ABC):
    def __init__(self, memory=None, prompt : Optional[Prompt] = None):
        self.memory = memory
        self.prompt = prompt
        self.params = prompt.params if prompt else None
    
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

class MultiChain(Chain):
    '''
    Chain that can be used to select from multiple chains based on a prompt.
    '''
    def __init__(self, chain_descriptions : dict, memory=None):
        super().__init__(memory)
        self.chains = chain_descriptions
        self.prefix = 'You have the following options with usage descriptions, output the name of the option that best fits the task: \n'
    
    def __call__(self, input):
        out = input
        prefix = self.prefix
        for chain, desc in self.chains:
            prefix += f'name: {chain} description: {desc} \n'
        return prefix + f'task: {out}'

class SwitchBoardChain(Chain):
    '''
    Chain that will apply a specific chain based on a parsed use.
    '''
    def __init__(self, chains : dict):
        super().__init__()
        self.chains = chains
        self.available_chains = list(chains.keys())
    
    def parse(self, chain):
        for availible_chain in self.available_chains:
            if availible_chain in chain: return availible_chain

    def __call__(self, input, chain):
        return self.chains[self.parse(chain)](input)

class SequentialChain(Chain):
    def __init__(self, chains, memory=None):
        super().__init__(memory)
        self.chains = chains
    
    def __call__(self, input):
        out = input
        for link in self.chain:
            out = link(out)
        return out