from collections import deque
from typing import Any
import json

"""
Uses Deque for simple memory management, can set maxlen to None if using for some more complex storage.
"""

class Memory:
    def __init__(self, maxlen : int, join : str = '\n') -> None:
        self.buffer = deque(maxlen=maxlen)
        self.join = join

    def insert(self, item : Any) -> None:
        self.buffer.append(item)

    def extend(self, items : Any) -> None:
        self.buffer.extend(items)
    
    def tojson(self):
        return json.dumps(self, default=lambda x: x.__dict__, 
            sort_keys=True, indent=4)
    
    def clear(self) -> None:
        self.buffer.clear()

class BufferMemory(Memory):
    def __init__(self, maxlen : int = 20, join : str = '\n') -> None:
        super.__init__(maxlen, join)

    def __str__(self) -> str:
        return f'{self.join}'.join([str(item) for item in self.buffer])
    
class IOMemory(Memory):
    def __init__(self, input_prefix : str = 'Human:', output_prefix : str = 'AI:', maxlen: int = 20, join: str = '\n') -> None:
        super().__init__(maxlen, join)
        self.input_prefix = input_prefix
        self.output_prefix = output_prefix
    
    def __str__(self) -> str:
        return f'{self.join}'.join([f'{self.input_prefix} {str(i)} \n {self.output_prefix} {str(o)}' for i, o in self.buffer])
    

    
