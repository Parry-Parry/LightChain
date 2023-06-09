from abc import abstractmethod

from lightchain.prompt import Prompt
from lightchain.object import Model, Object
from lightchain.memory import Memory
from typing import Any, List, Optional

class Chain(Object):
    '''
    Standard chain object

    Essentially a wrapper for a model, with a prompt and memory
    Composable using object ops
    '''
    def __init__(self, model : Model = None, memory : Memory = None, prompt : Optional[Prompt] = None, name : str = 'chain', description : str = 'Some Chain'):
        super().__init__(name=name, description=description)
        self.model = model
        self.memory = memory
        self.prompt = prompt
        self.params = prompt.params if prompt else None
    
    def write(self, input : Any) -> None:
        if self.memory: self.memory(input)

    @abstractmethod
    def logic(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        inp = args[0]
        if isinstance(inp, dict):
            return {k : self(v, **kwargs) for k, v in inp.items()}
        return self.logic(*args, **kwargs)

class LambdaChain(Chain):
    def __init__(self, func : callable):
        super().__init__(model=func, name=func.__name__, description=func.__doc__)

    def logic(self, *args, **kwargs):
        return self.model(*args, **kwargs)

class SwitchBoardChain(Chain):
    '''
        Present the LLM with a list of options, and then return the output of the selected option.

        Usage:
        >>> LLM = Model()
        >>> chain = SwitchBoardChain(LLM, [chain1, chain2, chain3])
        >>> out = chain(input)
        '''
    def __init__(self, model : Model, 
                 chains : List[Chain], 
                 memory : Memory = None, 
                 name : str = 'switchboard', 
                 description : str = 'Some Switchboard'):
        super().__init__(model=model, memory=memory, name=name, description=description)
        self.lookup = {chain.name : chain for chain in chains}
        self.prompt = 'You have the following options with usage descriptions, output the name of the option that best fits the task: \n'
    
    def parse(self, input : str):
        for chain in self.lookup.keys():
            if chain in input: return chain

    def logic(self, input):
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