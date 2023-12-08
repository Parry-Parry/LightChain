from json import dumps, loads
from typing import Optional, List
from re import findall
from lightchain.object import Object

class AutoPrompt(Object):
    pattern = r"\{([^}]+)\}"
    def __init__(self, 
                 prompt : str, 
                 name='AutoPrompt', 
                 description='Self Parsing Prompt'):
        super().__init__(name=name, description=description)
        self.prompt = prompt
        self.params = findall(self.pattern, prompt)
    
    @staticmethod
    def from_json(json_str):
        return loads(json_str, object_hook=lambda x: AutoPrompt(**x))
    
    @staticmethod
    def from_string(string : str, name='AutoPrompt', description='Self Parsing Prompt'):
        return AutoPrompt(prompt=string, name=name, description=description)
    
    def __repr__(self):
        return f'Prompt(prompt={self.prompt}, params={self.params}, name={self.name}, description={self.description})'
    
    def __dict__(self):
        return {'prompt' : self.prompt, 'name' : self.name, 'description' : self.description}
    
    def to_json(self):
        return dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    def __call__(self, *args, **kwargs):
        if args:
            if len(args) == 1: return [self(**inp) for inp in args[0]]
            else: return map(self, args)
        elif kwargs:
            arguments = {k : v for k, v in kwargs.items() if k in self.params}
            try: return self.prompt.format(**arguments)
            except KeyError as e: raise KeyError(f'Missing Args, Error: {e}')
        else: return self.prompt

class StructPrompt(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass