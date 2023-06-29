import types
from lightchain.prompt import Prompt
from lightchain.chain import Chain, LambdaChain
from matchpy import Wildcard
from lightchain.object.objects import Model, Object
from lightchain.object.pipelines import SequentialPipeline, ForkPipeline, Pipeline

def get_chain(chain) -> Chain:

    if isinstance(chain, Wildcard):
        return chain
    if isinstance(chain, Chain):
        return chain
    if isinstance(chain, Model):
        return chain
    if isinstance(chain, Prompt):
        return chain
    if isinstance(chain, list):
        return SequentialPipeline(chain)
    if isinstance(chain, types.FunctionType):
        return LambdaChain(chain)
    
    raise ValueError("Passed parameter %s of type %s cannot be coerced into a chain" % (str(chain), type(chain)))