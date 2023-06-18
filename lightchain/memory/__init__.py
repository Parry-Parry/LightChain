from abc import abstractmethod
from collections import deque
from typing import Any
import json

class Memory:
    def __init__(self, 
                 buffer = None, 
                 maxlen : int = None, 
                 join : str = '\n') -> None:
        self.buffer = buffer
        self.maxlen = maxlen
        self.join = join
    
    def tojson(self):
        return json.dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    @abstractmethod
    def insert(self, item : Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def extend(self, items : Any) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError
    
class FaissMemory:
    def __init__(self, index) -> None:
        pass 
    def index():
        pass
    
    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return NotImplementedError

class QueueMemory(Memory):
    """
    Uses Deque for simple memory management, can set maxlen to None if using for some more complex storage.
    """
    def __init__(self, maxlen : int, join : str = '\n') -> None:
        super().__init__(buffer=deque(maxlen=maxlen), maxlen=maxlen, join=join)

    def insert(self, item : Any) -> None:
        self.buffer.append(item)

    def extend(self, items : Any) -> None:
        self.buffer.extend(items)
    
    def clear(self) -> None:
        self.buffer.clear()

class DictMemory(Memory):
    def __init__(self, join : str = '\n') -> None:
        super().__init__(buffer={}, maxlen=None, join=join)

    def insert(self, key : Any, item : Any) -> None:
        self.buffer[key] = item

    def extend(self, items : dict) -> None:
        self.buffer.update(items)
    
    def clear(self) -> None:
        self.buffer = {}

    def __call__(self, keys) -> Any:
        if isinstance(keys, list):
            return [self.buffer[key] for key in keys]
        return self.buffer[keys]

class BufferMemory(QueueMemory):
    def __init__(self, maxlen : int = 20, join : str = '\n') -> None:
        super.__init__(maxlen, join)

    def __str__(self) -> str:
        return f'{self.join}'.join([str(item) for item in self.buffer])

class StringLengthBuffer(DictMemory):
    def __init__(self, length : int, join: str = '\n', essential=None) -> None:
        super().__init__(join)
        self.length = length
        self.buffer['main'] = []
        self.buffer['essential'] = essential if essential else ''
    
    def set_essential(self, text : str) -> None:
        assert len(text) <= self.length, f'Essential text must be less than {self.length} characters.'
        self.buffer['essential'] = text
    
    def insert(self, item : Any) -> None:
        self.buffer['main'].append(item)

    def extend(self, items : Any) -> None:
        self.buffer['main'].extend(items)

    def clear(self) -> None:
        self.buffer['main'] = []

    def extend_essential(self, text : str) -> None:
        assert len(text) + len(self.buffer['essential']) <= self.length, f'Essential text must be less than {self.length} characters.'
        self.buffer['essential'] += self.join + text

    def get_maximum_context(self) -> str:
        essential_len = len(self.buffer['essential'])
        current_len = essential_len
        for i, item in enumerate(self.buffer['main'][::-1]):
            if essential_len + len(item) > self.length:
                return self.join.join[self.buffer['main'][:i:-1]]
            else:
                current_len += len(item)
        return self.join.join(self.buffer['main'])
    
    def __str__(self) -> str:
        return str(self.buffer['essential']) + self.join.join(self.get_maximum_context())
    
    def __call__(self, items):
        if isinstance(items, list):
            return self.extend(items)
        if isinstance(items, str):
            return self.insert(items)
        else:
            raise TypeError(f'Expected list or string, got {type(items)}')
    
    
class ConversationMemory(StringLengthBuffer):
    def __init__(self, 
                 input_prefix : str = 'Human:', 
                 output_prefix : str = 'AI:', 
                 maxlen: int = 20, 
                 join: str = '\n',
                 essential=None) -> None:
        super().__init__(length=maxlen, join=join, essential=essential)
        self.input_prefix = input_prefix
        self.output_prefix = output_prefix
    
    def insert(self, item : Any) -> None:
        usr, ai = item 
        self.buffer['main'].append(self.input_prefix + usr)
        self.buffer['main'].append(self.output_prefix + ai)
    
    def extend(self, items : Any) -> None:
        for item in items:
            self.insert(item)
    
    
    
    

    

