from abc import abstractmethod
from lightchain.chain import Chain
from lightchain.memory import Memory
from lightchain.object import Model
from lightchain.prompt import Prompt
from pyterrier import Transformer

class TerrierChain(Transformer, Chain):
    def __init__(self, model: Model = None, out_attr : str = 'text', memory: Memory = None, prompt: Prompt | None = None, name: str = 'TerrierChain', description: str = 'Chain Compatible with Terrier'):
        super(Chain).__init__(model, memory, prompt, name, description)
        super(Transformer).__init__()
        self.out_attr = out_attr
    
    @abstractmethod
    def transform(self, input):
        raise NotImplementedError
        