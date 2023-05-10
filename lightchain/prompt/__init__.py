import json
from typing import List
from lightchain.object import Object
"""
Any prompt can be constructed from this abstract class. No need for particular prompt types or addition of few shot extensions.

Eventually write in Rust
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
    
    def tojson(self):
        return json.dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    def construct(self, **kwargs):
        for key in kwargs: assert key in self.params, f'Param {key} not found in params {self.params}'
        return self.prompt.format(**kwargs)
    
    def batch_construct(self, params : List[dict], num_proc : int = None):
        '''
        Ensure that params is a list of dicts and large enough to justify overhead of multiprocessing
        '''
        from multiprocessing import Pool, cpu_count
        if num_proc is None: num_proc = cpu_count()
        with Pool(num_proc) as p:
            return p.map(self.construct, params)
    
    def __call__(self, input, num_proc=5):
        if isinstance(input, list):
            return self.batch_construct(input, num_proc=num_proc)
        else:
            return self.construct(**input)
