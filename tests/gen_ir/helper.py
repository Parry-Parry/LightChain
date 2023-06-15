
from typing import List
from lightchain.object import Model
from lightchain.chain.terrier import TerrierChain

def parse_chains(out, chains : List[str]):
    return [' '.join(map(lambda x : item[x], chains)) for item in out]

class ExpansionChain(TerrierChain):
    def __init__(self, model, out_attr='text', examples_per_query : int = 3, name='Expansion Chain', description='Terrier Compatible GRF'):
        super().__init__(model, out_attr=out_attr, name=name, description=description)
        self.examples_per_query = examples_per_query
    def forward(self, input):
        input = input.copy()
        examples = input.groupby('qid').sample(self.examples_per_query)
        examples = examples.groupby('qid').apply(lambda x : x.to_dict('records')).to_dict()

        input[self.out_attr] = input.apply(lambda x : x['text'] + self.model(x['text'], examples[x['qid']]), axis=1)
        return input

class Llama(Model):
    def __init__(self, model, keep_prompt=False):
        super.__init__(model=model)
        self.keep_prompt = keep_prompt

    def __call__(input):
        if isinstance(input, list): 
            pass 
        else: 
            pass 