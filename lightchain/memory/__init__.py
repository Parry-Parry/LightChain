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

class BufferMemory(QueueMemory):
    def __init__(self, maxlen : int = 20, join : str = '\n') -> None:
        super.__init__(maxlen, join)

    def __str__(self) -> str:
        return f'{self.join}'.join([str(item) for item in self.buffer])
    
class ConversationMemory(QueueMemory):
    def __init__(self, 
                 input_prefix : str = 'Human:', 
                 output_prefix : str = 'AI:', 
                 maxlen: int = 20, 
                 join: str = '\n') -> None:
        super().__init__(maxlen, join)
        self.input_prefix = input_prefix
        self.output_prefix = output_prefix
    
    def __str__(self) -> str:
        return f'{self.join}'.join([f'{self.input_prefix} {str(i)} \n {self.output_prefix} {str(o)}' for i, o in self.buffer])
    

    

