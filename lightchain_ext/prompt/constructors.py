import json
from typing import Optional, List
import logging
import re
from lightchain.object import Object

"""
Any prompt can be constructed from this abstract class. No need for particular prompt types

TODO:
    - Add flexible support for multiple examples per prompt
"""

class Prompt(Object):
    pattern = r"\{([^}]+)\}"
    def __init__(self, 
                 prompt : str, 
                 name='Standard Prompt', 
                 description='Standard Prompt'):
        super().__init__(name=name, description=description)
        self.prompt = prompt
        self.params = re.findall(self.pattern, prompt)
        
    def __str__(self):
        return self.prompt

    def __repr__(self):
        return f'Prompt(prompt={self.prompt}, params={self.params}, name={self.name}, description={self.description})'
    
    def __dict__(self):
        return {'prompt' : self.prompt, 'name' : self.name, 'description' : self.description}
    
    @staticmethod
    def fromjson(json_str):
        return json.loads(json_str, object_hook=lambda x: Prompt(**x))
    
    @staticmethod
    def fromstring(string : str, name='Standard Prompt', description='Standard Prompt'):
        return Prompt(prompt=string, name=name, description=description)
    
    def tojson(self):
        return json.dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    def construct(self, kwargs):
        arguments = {}
        for key in kwargs.keys(): 
            if key not in self.params:
                logging.warning(f'Key {key} not found in params {self.params}')
            else:
                arguments[key] = kwargs[key]
        try:
            return self.prompt.format(**arguments)
        except KeyError as e:
            logging.ERROR(f'Missing Args, Error: {e}')
            return ""
    
    def __call__(self, inp):
        if isinstance(inp, list):
            return list(map(self.construct, inp))
        else:
            return self.construct(inp)

class FewShotPrompt(Prompt):
    def __init__(self, 
                 prompt : str, 
                 few_shot_constructor : Prompt, 
                 name='Few Shot Prompt', 
                 description='Few Shot Prompt', 
                 examples : Optional[List[List[dict]]] = None):
        super().__init__(prompt=prompt, name=name, description=description)
        if 'examples' not in self.params: self.params.append('examples')
        self.few_shot_constructor = few_shot_constructor
        
        if examples: 
            if isinstance(examples, dict): examples = [examples]
        self.examples = examples if examples else [{'examples' : ''}]
    
    def __call__(self, params, examples=None):
        if examples is None: examples = self.examples
        if examples and isinstance(examples, dict): examples = [examples]

        if len(examples) != 1: # Assumes list of lists of dicts
            assert len(params) == len(examples), f'Number of example sets {len(examples)} does not match number of param sets {len(params)}'
            examples = map(lambda x : '\n'.join(self.few_shot_constructor(x)), examples)
            params = [{'examples' : example, **param} for example, param in zip(examples, params)]
        else:
            examples = examples[0]
            assert isinstance(examples, dict), f'Examples must be a dict or list of dicts, not {type(examples)}'
            params = [{'examples' : self.few_shot_constructor(examples), **param} for param in params]

        return self.construct(params)
    

        