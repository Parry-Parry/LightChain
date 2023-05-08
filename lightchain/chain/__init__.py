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
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class SwitchBoardChain(Chain):
    '''
    Chain that can be used to select from multiple chains based on a prompt.
    '''
    def __init__(self, chains, memory=None):
        super().__init__(memory)
        self.lookup = {chain.name : chain for chain in chains}
        self.prompt = 'You have the following options with usage descriptions, output the name of the option that best fits the task: \n'
    
    def parse(self, input):
        for chain in self.lookup.keys():
            if chain in input: return chain

    def __call__(self, input):
        '''
        Present the LLM with a list of options, and then return the output of the selected option.

        Usage:
        >>> LLM = Model()
        >>> chain = SwitchBoardChain([chain1, chain2, chain3])
        >>> potential = chain('I want to do some task')
        >>> chain.send(LLM(potential)))
        >>> out = next(chain)
        '''
        out = input
        prefix = self.prompt
        for name, chain in self.lookup.items():
            prefix += f'name: {name} description: {chain.description} \n'
        yield prefix + f'task: {out}'
        key = yield
        yield self.lookup[key](out)

class SequentialChain(Chain):
    def __init__(self, chains, memory=None):
        super().__init__(memory)
        self.chains = chains
    
    def __call__(self, input):
        out = input
        for link in self.chain:
            out = link(out)
        return out