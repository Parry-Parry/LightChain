from lightchain.object import Model
from lightchain.chain.terrier import TerrierChain

class ExpansionChain(TerrierChain):
    def __init__(self, model, out_attr='expansion', examples_per_query : int = 3, name='Expansion Chain', description='Terrier Compatible GRF'):
        super().__init__(model, out_attr=out_attr, name=name, description=description)
        self.examples_per_query = examples_per_query
    def transform(self, input):
        input = input.copy() # input is a dataframe of qid, query, docno, text
        examples = input.groupby('qid').sample(n=self.examples_per_query, weights='score')
        examples = examples.groupby('qid').apply(lambda x : x.to_dict('records')).to_dict()

        # generate expansions for each unique query and make a dictionary of qid -> expansions
        queries = input[['qid', 'query']].unique()
        queries['expansion'] = queries.apply(lambda x : self.model({'text' : x['query']}, {'examples' : examples[x['qid']]}), axis=1)
        queries = queries.set_index('qid')['expansion'].to_dict()

        input[self.out_attr] = input.apply(lambda x : queries[x['qid']], axis=1)
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