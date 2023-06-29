import json
from typing import List
from lightchain.object import Object
from typing import Optional, List
import logging

"""
Any prompt can be constructed from this abstract class. No need for particular prompt types
"""

class Prompt(Object):
    def __init__(self, prompt : str, params : List[str] = None, name='Standard Prompt', description='Standard Prompt'):
        super().__init__(name=name, description=description)
        self.prompt = prompt
        self.params = params

        if params:
            for param in params: assert f'{{{param}}}' in prompt, f'Param {param} not found in prompt {prompt}'
        
    def __str__(self):
        return self.prompt

    def __repr__(self):
        return f'Prompt(prompt={self.prompt}, params={self.params})'
    
    @staticmethod
    def fromjson(json_str):
        return json.loads(json_str, object_hook=lambda x: Prompt(**x))
    
    @staticmethod
    def fromstring(string : str, params=None, name='Standard Prompt', description='Standard Prompt'):
        return Prompt(prompt=string, params=params, name=name, description=description)
    
    def tojson(self):
        return json.dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    def construct(self, **kwargs):
        for key in kwargs: 
            if key not in self.params:
                logging.warning(f'Key {key} not found in params {self.params}')
                kwargs.pop(key)
        return self.prompt.format(**kwargs)
    
    def batch_construct(self, params : List[dict], num_proc : int = None):
        '''
        Ensure that params is a list of dicts and large enough to justify overhead of multiprocessing
        '''
        from multiprocessing import Pool, cpu_count
        if num_proc is None: num_proc = cpu_count()
        with Pool(num_proc) as p:
            return p.map(self.construct, params)
    
    def __call__(self, inp, num_proc=4):
        if isinstance(inp, list):
            return self.batch_construct(inp, num_proc=num_proc)
        else:
            return self.construct(**inp)

class FewShotPrompt(Prompt):
    def __init__(self, prompt : str, few_shot_constructor : Prompt, params : List[str], name='Few Shot Prompt', description='Few Shot Prompt', examples : Optional[List[List[dict]]] = None):
        if 'examples' not in params: params.append('examples')
        super().__init__(prompt=prompt, params=params, name=name, description=description)
        self.few_shot_constructor = few_shot_constructor
        
        if examples: 
            if isinstance(examples, dict): examples = [examples]
        self.examples = examples if examples else [{'examples' : ''}]
    
    def __call__(self, params, examples=None, num_proc=4):
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

        if isinstance(params, list):
            return self.batch_construct(params, num_proc=num_proc)
        else:
            return self.construct(examples, **params)
    

        