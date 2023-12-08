from json import dumps, loads
from typing import Optional, List, Any
from re import findall
from lightchain.link import Link

class AutoPrompt(Link):
    pattern = r"\{([^}]+)\}"
    def __init__(self, 
                 prompt : str, 
                 name='AutoPrompt', 
                 description='Self Parsing Prompt') -> None:
        super().__init__(name=name, description=description)
        self.prompt = prompt
        self.params = findall(self.pattern, prompt)
    
    @staticmethod
    def from_json(json_str) -> 'AutoPrompt':
        return loads(json_str, object_hook=lambda x: AutoPrompt(**x))
    
    @staticmethod
    def from_string(string : str, name='AutoPrompt', description='Self Parsing Prompt') -> 'AutoPrompt':
        return AutoPrompt(prompt=string, name=name, description=description)
    
    def __repr__(self) -> str:
        return f'Prompt(prompt={self.prompt}, params={self.params}, name={self.name}, description={self.description})'
    
    def __dict__(self) -> dict:
        return {'prompt' : self.prompt, 'name' : self.name, 'description' : self.description}
    
    def to_json(self) -> str:
        return dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    def __call__(self, *args : Optional[List[dict]], **kwargs : Optional[Any]) -> Optional[List[str]] or str:
        if args:
            if len(args) == 1: return [self(**inp) for inp in args[0]]
            else: return map(self, args)
        elif kwargs:
            if all(isinstance(item, list) for item in kwargs.values()):
                kwarg_combinations = [{k: v[i] for k, v in kwargs.items()} for i in range(len(kwargs[list(kwargs.keys())[0]]))]
                return [self.prompt.format(**item) for item in kwarg_combinations]
            else: return self.prompt.format(**kwargs)
        else: return self.prompt

class StructPrompt(Link):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        pass