from abc import abstractmethod
from lightchain.link import Link
from typing import Any, List, Optional, Tuple

class SwitchBoardChain(Link):
    '''
        Present the LLM with a list of options, and then return the output of the selected option.

        Usage:
        >>> LLM = Model()
        >>> chain = SwitchBoardChain(LLM, [chain1, chain2, chain3])
        >>> out = chain(input)
    '''
    prompt = 'You have the following options with usage descriptions, output the name of the option that best fits the task: \n'
    def __init__(self, model : Any, 
                 links : List[Link], 
                 name : str = 'Switchboard', 
                 description : str = 'Some Switchboard') -> None:
        super().__init__(model=model, lookup={link.name : link for link in links}, name=name, description=description)
    
    def parse(self, input : str) -> str:
        for link in self.lookup.keys():
            if link in input: return link

    def logic(self, input : Tuple[List[str], str]) -> Any:
        out = input
        prefix = self.prompt
        for name, link in self.lookup.items():
            prefix += f'name: {name} description: {link.description} \n'
        if isinstance(input, list):
            keys = [self.parse(self.model(prefix + f'task: {o}')) for o in out]
            return [self.lookup[key](o) for key, o in zip(keys, out)]
        if isinstance(input, str):
            key = self.parse(self.model(prefix + f'task: {out}'))
            return self.lookup[key](out)

        raise ValueError(f'Input {input} of type {type(input)} is not supported by SwitchBoardChain')