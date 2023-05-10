from typing import List

import numpy as np
from lightchain.prompt import Prompt
from lightchain.object import Model
from lightchain.chain import Chain
from lightchain.memory import DictMemory
from lightchain.pipeline import ForkPipeline

# Path: tests/deliberate/chain.py

class Intermediate(Chain):
    prefix = "The other agents have now responded to the question, do you agree with what they have said? \n If you believe that you now align with the other agents answers, output '[END]' otherwise continue the discussion"
    def __init__(self, model : Model, params : dict = None):
        super().__init__(model=model, params=params, memory=DictMemory(maxlen=1000))
    
    def __call__(self, input : dict):
        prompt = self.memory['previous'] + self.prefix
        for key, value in input.items():
            prompt += f'\n Agent {key} responded: {value}'
        
        response = self.model(prompt)
        text = response.item() 
        # Think about how to keep track of the previous prompt if they have agreed
        self.memory['previous'] += prompt + f'\n{text}'
        if '[END]' not in text: self.memory['current'] = text 
        return response


class DeliberatePrompt(Prompt):
    prefix = 'You are an agent which works with other agents to agree on a concept \n You will be given a question, give your answer:'
    def __init__(self):
        super().__init__(self.prefix + '\n question: {question} \n answer:', ['question'], name='Entry to deliberate', description='Provides template to begin discussion')
        self.prompt = Prompt()
    
    def __call__(self, question : str):
        return self.prompt.construct(question=question)

class Deliberator:
    def __init__(self, models : List[Model]) -> None:
        self.agents = ForkPipeline(models)
        self.intermediate = ForkPipeline([Intermediate(model) for model in models])
        self.entry = DeliberatePrompt()

        self.intial_chain = self.entry >> self.agents
    
    def __call__(self, question : str):
        responses = self.intial_chain(question)
        
        while True:
            responses = self.intermediate(responses)
            text = [response.item() for response in responses]
            if np.all('[END]' in text):
                break

        # if complete: 
        output = ''
        for agent in self.intermediate.chains():
            out = agent.memory['current']
            output += f'\n Agent {agent.name} responded: {out}'
        return output