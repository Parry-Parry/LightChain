from abc import abstractmethod
from lightchain.object import Object
from typing import Any, List

class Chain(Object):
    '''
        A Chain is a wrapper for an arbitrary number of models, memories, and prompts. It is the primary interface for the user to interact with the LLM.
    '''
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    @abstractmethod
    def write(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def logic(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], dict):
            return {k : self(v, **kwargs) for k, v in args[0].items()}
        return self.logic(*args, **kwargs)

class SwitchBoardChain(Chain):
    '''
        Present the LLM with a list of options, and then return the output of the selected option.

        Usage:
        >>> LLM = Model()
        >>> chain = SwitchBoardChain(LLM, [chain1, chain2, chain3])
        >>> out = chain(input)
    '''
    prompt = 'You have the following options with usage descriptions, output the name of the option that best fits the task: \n'
    def __init__(self, model : Any, 
                 chains : List[Chain], 
                 name : str = 'Switchboard', 
                 description : str = 'Some Switchboard'):
        super().__init__(model=model, lookup={chain.name : chain for chain in chains}, name=name, description=description)
    
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