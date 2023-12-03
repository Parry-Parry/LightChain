import json
from typing import Optional, List
import logging
import re
from lightchain.object import Object

class AutoPrompt(Object):
    pattern = r"\{([^}]+)\}"
    def __init__(self, 
                 prompt : str, 
                 name='AutoPrompt', 
                 description='Self Parsing Prompt'):
        super().__init__(prompt=prompt, name=name, description=description)
        self.params = re.findall(self.pattern, prompt)
        
    def __str__(self):
        return f'Prompt(prompt={self.prompt}, params={self.params}, name={self.name}, description={self.description})'

    def __repr__(self):
        return f'Prompt(prompt={self.prompt}, params={self.params}, name={self.name}, description={self.description})'
    
    def __dict__(self):
        return {'prompt' : self.prompt, 'name' : self.name, 'description' : self.description}
    
    @staticmethod
    def from_json(json_str):
        return json.loads(json_str, object_hook=lambda x: AutoPrompt(**x))
    
    @staticmethod
    def from_string(string : str, name='AutoPrompt', description='Self Parsing Prompt'):
        return AutoPrompt(prompt=string, name=name, description=description)
    
    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    def construct(self, kwargs):
        arguments = {}
        for key in kwargs.keys(): 
            if key not in self.params: logging.warning(f'Key {key} not found in params {self.params}')
            else: arguments[key] = kwargs[key]
        try:
            return self.prompt.format(**arguments)
        except KeyError as e:
            raise KeyError(f'Missing Args, Error: {e}')
    
    def __call__(self, inp):
        if isinstance(inp, list):
            return list(map(self.construct, inp))
        else:
            return self.construct(inp)

class FewShotPrompt(AutoPrompt):
    def __init__(self, 
                 prompt : str, 
                 few_shot_constructor : AutoPrompt, 
                 name='Few Shot Prompt', 
                 description='Few Shot Prompt', 
                 default : Optional[List[List[dict]]] = None):
        super().__init__(prompt=prompt, name=name, description=description)
        self.few_shot_constructor = few_shot_constructor
        
        if default: 
            if isinstance(examples, dict): examples = [examples]
        self.default = examples if examples else [{'examples' : ''}]
    
    def __call__(self, inputs, examples=None):
        if examples is None: examples = self.default
        if examples and isinstance(examples, dict): examples = [examples]

        if len(examples) != 1: # Assumes list of lists of dicts
            assert len(inputs) == len(examples), f'Number of example sets {len(examples)} does not match number of parameter sets {len(inputs)}'
            examples = map(lambda x : '\n'.join(self.few_shot_constructor(x)), examples)
            inputs = [{'examples' : example, **params} for example, params in zip(examples, inputs)]
        else:
            assert isinstance(examples, dict), f'Examples must be a dict or list of dicts, not {type(examples)}'
            inputs = [{'examples' : self.few_shot_constructor(examples), **params} for params in inputs]
        return super()(inputs)

class StructPrompt(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)