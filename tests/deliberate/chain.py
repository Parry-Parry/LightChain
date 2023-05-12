from typing import List

import numpy as np
from lightchain.prompt import Prompt
from lightchain.object import Model
from lightchain.chain import Chain
from lightchain.memory import BufferMemory, DictMemory
from lightchain.pipeline import ForkPipeline

# Path: tests/deliberate/chain.py

class Intermediate(Chain):
    prefix = "The other agents have now responded to the question, do you agree with what they have said? \n If you believe that you now align with the other agents answers, output '[END]' otherwise continue the discussion and explain your thinking"
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


class DeliberatePrompt(Prompt):
    prefix = 'You are an agent which works with other agents to agree on a concept \n You will be given a question, give your answer:'
    def __init__(self):
        super().__init__(self.prefix + '\n question: {question} \n answer:', ['question'], name='Entry to deliberate', description='Provides template to begin discussion')
        self.prompt = Prompt()
    
    def __call__(self, question : str):
        return self.prompt.construct(question=question)

class Deliberator(Chain):
    def __init__(self, model : Model, num_agents : int = 3, name='Deliberator Chain', description='Recieves a question and uses multiple agents with seperate memories to discuss and agree on a concept') -> None:
        super.__init__(model=model, memory=BufferMemory(), name=name, description=description)
        self.num_agents = num_agents
        self.agents = ForkPipeline([model for _ in range(num_agents)])
        self.entry = DeliberatePrompt()

        self.intial_chain = self.entry >> self.agents
    
    def __call__(self, question : str):
        self.memory.append(question)
        responses = self.intial_chain(question)
        self.intermediate = ForkPipeline([Intermediate(f'{DeliberatePrompt.prefix}\n {question}', self.model, name=str(i)) for i in range(self.num_agents)])
        
        while True:
            responses = self.intermediate(responses)
            self.memory.extend([f'Agent {key} responded: {value}' for key, value in responses.items()])
            text = [response.item() for response in responses]
            if np.all('[END]' in text):
                break

        # if complete: 
        output = ''
        for agent in self.intermediate.chains():
            out = agent.memory['current']
            output += f'\n Agent {agent.name} responded: {out}'
        return output
