import json
"""
Any prompt can be constructed from this abstract class. No need for particular prompt types or addition of few shot extensions.

Eventually write in Rust
"""
class Prompt:
    def __init__(self, prompt, params=None):
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
    
    def batch_construct(self, params):
        return [self.construct(**param) for param in params]