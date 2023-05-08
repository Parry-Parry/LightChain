from abc import ABC, abstractmethod

from lightchain.prompt import Prompt
from lightchain.object import Object
from typing import Optional

"""
Notion would be that you can move parsing of output into each chain given that you have a specific CoT use case.
"""

class Chain(Object):
    def __init__(self, model=None, memory=None, prompt : Optional[Prompt] = None, name='chain', description='Some Chain'):
        self.model = model
        self.memory = memory
        self.prompt = prompt
        self.params = prompt.params if prompt else None
        
    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class LambdaChain(Chain):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class SwitchBoardChain(Chain):
    '''
    Chain that can be used to select from multiple chains based on a prompt.
    '''
    def __init__(self, model, chains, memory=None):
        super().__init__(model=model, memory=memory)
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
        >>> chain = SwitchBoardChain(LLM, [chain1, chain2, chain3])
        >>> out = chain(input)
        '''
        out = input
        prefix = self.prompt
        for name, chain in self.lookup.items():
            prefix += f'name: {name} description: {chain.description} \n'
        key = self.parse(self.model(prefix + f'task: {out}'))
        return self.lookup[key](out)