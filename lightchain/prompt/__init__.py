import json
from typing import List
from lightchain.object import Object
import logging
"""
Any prompt can be constructed from this abstract class. No need for particular prompt types or addition of few shot extensions.

Eventually write in Rust
"""

class Prompt(Object):
    def __init__(self, prompt : str, params : List[str] = None, name='Standard Prompt', description='Standard Prompt', inp_type : str = 'dict'):
        super().__init__(name=name, description=description)
        self.prompt = prompt
        self.params = params

        if params:
            for param in params: assert f'{{{param}}}' in prompt, f'Param {param} not found in prompt {prompt}'

        if inp_type == 'dict':
            self.construct = self.dict_construct
        elif inp_type == 'named':
            self.construct = self.named_construct
        else:
            logging.warning(f'Input type {inp_type} not recognized. Defaulting to dict.')
            self.construct = self.dict_construct
        
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
    
    def __call__(self, input, num_proc=4):
        if isinstance(input, list):
            return self.batch_construct(input, num_proc=num_proc)
        else:
            return self.construct(**input)
