from abc import abstractmethod

from lightchain.prompt import Prompt
from lightchain.object import Model, Object
from typing import List, Optional

class Chain(Object):
    def __init__(self, model : Model = None, memory=None, prompt : Optional[Prompt] = None, name : str = 'chain', description : str = 'Some Chain'):
        self.model = model
        self.memory = memory
        self.prompt = prompt
        self.params = prompt.params if prompt else None
        
    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class LambdaChain(Chain):
    def __init__(self, func : callable):
        super().__init__(model=func, name=func.__name__, description=func.__doc__)

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

class SwitchBoardChain(Chain):
    '''
    Chain that can be used to select from multiple chains based on a prompt.
    '''
    def __init__(self, model : Model, chains : List[Chain], memory=None, name : str = 'switchboard', description : str = 'Some Switchboard'):
        super().__init__(model=model, memory=memory, name=name, description=description)
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
        if isinstance(input, list):
            keys = [self.parse(self.model(prefix + f'task: {o}')) for o in out]
            return [self.lookup[key](o) for key, o in zip(keys, out)]
        if isinstance(input, str):
            key = self.parse(self.model(prefix + f'task: {out}'))
            return self.lookup[key](out)

        raise ValueError(f'Input {input} of type {type(input)} is not supported by SwitchBoardChain')