from abc import abstractmethod
from collections import deque
from typing import Any
import json

class Memory:
    def __init__(self, 
                 buffer = None, 
                 maxlen : int = None, 
                 join : str = '\n') -> None:
        self.BUFFER = buffer
        self.MAXLEN = maxlen
        self.JOIN = lambda x : join.join(x) if isinstance(x, list) else x
    
    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)

    @staticmethod
    def from_json(json_str):
        return json.loads(json_str, object_hook=lambda x: Memory(**x))
    
    @abstractmethod
    def insert(self, item : Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def extend(self, items : Any) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

class QueueMemory(Memory):
    """
    Uses Deque for simple memory management, can set maxlen to None if using for some more complex storage.
    """
    def __init__(self, maxlen : int, join : str = '\n') -> None:
        super().__init__(buffer=deque(maxlen=maxlen), maxlen=maxlen, join=join)

    def insert(self, item : Any) -> None:
        self.BUFFER.append(item)

    def extend(self, items : Any) -> None:
        self.BUFFER.extend(items)
    
    def clear(self) -> None:
        self.BUFFER.clear()

    def __str__(self) -> str:
        return self.JOIN([str(item) for item in self.BUFFER])

class DictMemory(Memory):
    def __init__(self, join : str = '\n') -> None:
        super().__init__(buffer={}, maxlen=None, join=join)

    def insert(self, key : Any, item : Any) -> None:
        self.BUFFER[key] = item

    def extend(self, items : dict) -> None:
        self.BUFFER.update(items)
    
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
        assert len(self.tokenizer.encode(text + self.JOIN)) + len(self.BUFFER['essential']) <= self.length, f'Essential text must be less than {self.length} characters.'
        self.BUFFER['essential'] += self.join + text

    def insert(self, item : Any) -> None:
        self.BUFFER['main'].append(item)

    def extend(self, items : Any) -> None:
        self.BUFFER['main'].extend(items)

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
    
    def __str__(self) -> str:
        return self.get_maximum_context()
    
    def wrap(self, text : str) -> str:
        return self.get_maximum_context(text)
    
    def __call__(self, items):
        if isinstance(items, list):
            return self.extend(items)
        if isinstance(items, str):
            return self.insert(items)
        else:
            raise TypeError(f'Expected list or string, got {type(items)}')
    
    
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