from json import dumps, loads
from typing import Optional, List, Any
from re import findall
from lightchain.link import Link

class AutoPrompt(Link):
    """
    The AutoPrompt class represents a self-parsing prompt. It inherits from the Link class.

    Attributes:
        pattern (str): The regex pattern used to parse the prompt.
        prompt (str): The prompt string.
        params (list): The parameters found in the prompt string.
        name (str): The name of the AutoPrompt object. Default is 'AutoPrompt'.
        description (str): The description of the AutoPrompt object. Default is 'Self Parsing Prompt'.

    Args:
        prompt (str): The prompt string.
        name (str, optional): The name of the AutoPrompt object. Defaults to 'AutoPrompt'.
        description (str, optional): The description of the AutoPrompt object. Defaults to 'Self Parsing Prompt'.
    """
    pattern = r"\{([^}]+)\}"
    def __init__(self, 
                 prompt : str, 
                 name='AutoPrompt', 
                 description='Self Parsing Prompt') -> None:
        """
        Initializes the AutoPrompt object. It parses the prompt string and finds the parameters.
        """
        super().__init__(name=name, description=description)
        self.prompt = prompt
        self.params = findall(self.pattern, prompt)
    
    @staticmethod
    def from_json(json_str : str) -> 'AutoPrompt':
        return loads(json_str, object_hook=lambda x: AutoPrompt(**x))
    
    @staticmethod
    def from_string(string : str, name : str = 'AutoPrompt', description : str = 'Self Parsing Prompt') -> 'AutoPrompt':
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