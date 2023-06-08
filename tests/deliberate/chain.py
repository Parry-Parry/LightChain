from typing import List

import numpy as np
from lightchain.prompt import Prompt
from lightchain.object import Model
from lightchain.chain import Chain
from lightchain.memory import BufferMemory, DictMemory
from lightchain.pipeline import ForkPipeline

# Path: tests/deliberate/chain.py
# https://arxiv.org/abs/2305.14325 now following these clever people as its scooped!

class DeliberatePrompt(Prompt):
    long = "Using the solutions from other agents as additional information, can you give an updated response...."
    short = ''
    def __init__(self, prompt: str, params: List[str] = None, name='Standard Prompt', description='Standard Prompt', long=False):
        super().__init__(prompt, params, name, description)
        self.prefix = self.long if long else self.short

class Intermediate(Chain):
    def __init__(self, initial : str, model : Model, params : dict = None, name='0'):
        super().__init__(model=model, params=params, memory=DictMemory(maxlen=1000), name=name)
        self.memory['buffer'] = f'{initial}\n'
    
    def __call__(self, input : dict):
        input = {k : v for k, v in input.items() if k != self.name}
        prompt = self.memory['buffer'] + self.prefix
        for key, value in input.items():
            prompt += f'Agent {key} responded: {value}\n'
        
        response = self.model(prompt)
        text = response.item() 
        # Think about how to keep track of the previous prompt if they have agreed
        self.memory['buffer'] += prompt + f'\n{text}'
        if '[END]' not in text: self.memory['current'] = text 
        return response

class Deliberator(Chain):
    def __init__(self, model : Model, num_agents : int = 3, name='Deliberator Chain', description='Recieves a question and uses multiple agents with seperate memories to discuss and agree on a concept', long=False) -> None:
        super.__init__(model=model, memory=BufferMemory(), name=name, description=description)
        self.num_agents = num_agents
        self.agents = ForkPipeline([model for _ in range(num_agents)])
        self.entry = Prompt.fromstring('')
        self.deliberation_prompt = Prompt.fromstring('', params=['responses'])
        self.agreement_check = Prompt.fromstring('', params=['responses'])

        self.intial_chain = self.entry >> self.agents
    
    def __call__(self, question : str, long=False):
        self.memory.append(question)
        responses = self.intial_chain(question)
        self.intermediate = ForkPipeline([Intermediate(f'{DeliberatePrompt.prefix}\n {question}', self.model, name=str(i)) for i in range(self.num_agents)])
        
        while True:
            responses = self.intermediate(responses)
            self.memory.extend([f'Agent {key} responded: {value}' for key, value in responses.items()])
            text = [response.item() for response in responses]
            if 'bar' in self.agreement_check(responses=text): break

        # if complete: 
        output = ''
        for agent in self.intermediate.chains():
            out = agent.memory['current']
            output += f'\n Agent {agent.name} responded: {out}'
        return output
