from abc import abstractmethod
from typing import Any
from lightchain import Link
import logging

class Memory(Link):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    @abstractmethod
    def insert(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError

class DictMemory(Memory):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.BUFFER = {}

    def insert(self, **kwargs) -> None:
        self.BUFFER.update(kwargs)
    
    def clear(self) -> None:
        self.BUFFER = {}

    def __call__(self, keys) -> Any:
        if isinstance(keys, list):
            return [self.BUFFER[key] for key in keys]
        return self.BUFFER[keys]

class StringLengthBuffer(DictMemory): 
    def __init__(self, context_length : int, model_id : str, join: str = '\n', essential=None) -> None:
        super().__init__(join)
        from transformers import AutoTokenizer
        self.BUFFER['main'] = []
        self.BUFFER['essential'] = essential if essential else ''
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self._max_length = context_length
        self._default_length = len(self.tokenizer.encode(self.BUFFER['essential'])) if essential else 0

        assert self._default_length <= self._max_length, f'Essential text must be less than {self._max_length} tokens.'
    
    def set_essential(self, text : str) -> None:
        assert len(self.tokenizer.encode(text)) <= self._max_length, f'Essential text must be less than {self._max_length} tokens.'
        self.BUFFER['essential'] = text
        self._default_length = len(self.tokenizer.encode(self.BUFFER['essential']))

    def extend_essential(self, text : str) -> None:
        if len(self.tokenizer.encode(text + self.JOIN)) + len(self.BUFFER['essential']) <= self.length:
            logging.WARN(f'Essential text must be less than {self.length} characters. No Change Made')
        else: self.BUFFER['essential'] += self.join + text

    def insert(self, item : Any) -> None:
        if isinstance(item, list): self.BUFFER['main'].extend(item)
        else: self.BUFFER['main'].append(item)

    def clear(self) -> None:
        self.BUFFER['main'] = []

    def get_maximum_context(self, new_string='') -> str:
        essential_len = self._default_length + len(self.tokenizer.encode(new_string))
        current_len = essential_len
        for i, item in enumerate(self.BUFFER['main'][::-1]):
            item_len = len(self.tokenizer.encode(item))
            if current_len + item_len + 1 > self._max_length:
                return self.JOIN.join([*self.BUFFER['essential'], *self.BUFFER['main'][:i:-1], new_string])
            else:
                current_len += item_len + 1
        return self.JOIN.join([*self.BUFFER['essential'], *self.BUFFER['main'], new_string])
    
    def __call__(self, text : str):
        return self.get_maximum_context(text)
        
class ConversationMemory(StringLengthBuffer):
    def __init__(self, 
                 model_id : str,
                 input_prefix : str = 'Human:', 
                 output_prefix : str = 'AI:', 
                 context_length : int = 20, 
                 join: str = '\n',
                 essential : str = None) -> None:
        super().__init__(context_length=context_length, model_id=model_id, join=join, essential=essential)
        self.input_prefix = input_prefix
        self.output_prefix = output_prefix
    
    def insert(self, item : Any) -> None:
        user, ai = item 
        self.BUFFER['main'].append(self.input_prefix + user)
        self.BUFFER['main'].append(self.output_prefix + ai)
    
    def extend(self, items : Any) -> None:
        for item in items:
            self.insert(item)