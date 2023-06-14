
def parse_ranking(df)
    pass 

def parse_chains(out, chains : List[str]):
    return [' '.join(map(lambda x : item[x], chains)) for item in out]

class Llama(Model):
    def __init__(model, keep_prompt=False):
        super.__init__(model=model)
        self.keep_prompt
    def __call__(input):
        if isinstance(input, list): 
            pass 
        else: 
            pass 