from abc import abstractmethod
from typing import Any, List, Tuple, Union
from lightchain import Link
import logging

class Memory(Link):
    """
    The Memory class is an abstract base class for memory operations.
    It provides methods for inserting data and calling the memory.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    @abstractmethod
    def insert(self, *args, **kwargs) -> None:
        raise NotImplementedError

class DictMemory(Memory):
    """
    The DictMemory class is a concrete implementation of the Memory class using a dictionary as the underlying data structure.
    """
    def __init__(self, **kwargs) -> None:
        """
        Initializes the DictMemory object. It also initializes an empty dictionary as the buffer.
        """
        super().__init__(**kwargs)
        self.BUFFER = {}

    def insert(self, **kwargs) -> None:
        """
        Inserts the given keyword arguments into the buffer.
        """
        self.BUFFER.update(kwargs)
    
    def clear(self) -> None:
        """
        Clears the buffer.
        """
        self.BUFFER = {}

    def logic(self, keys) -> Any:
        """
        Retrieves the values associated with the given keys from the buffer.
        """
        if isinstance(keys, list):
            return [self.BUFFER[key] for key in keys]
        return self.BUFFER[keys]

class StringLengthBuffer(DictMemory): 
    """
    The StringLengthBuffer class is a concrete implementation of the DictMemory class that buffers strings of a certain length.
    """
    def __init__(self, context_length : int, model_id : str, join: str = '\n', essential=None) -> None:
        """
        Initializes the StringLengthBuffer object. It also initializes the tokenizer and checks that the essential text is not too long.

        Args:
            context_length (int): The maximum length of the buffer in terms of the number of tokens.
            model_id (str): The identifier of the model used for tokenization.
            join (str, optional): The string used to join the buffered strings when they are retrieved. Defaults to '\n'.
            essential (str, optional): An essential string that is always included in the buffer. Defaults to None.
        """
        super().__init__(join)
        from transformers import AutoTokenizer
        self.BUFFER['main'] = []
        self.BUFFER['essential'] = essential if essential else ''
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self._max_length = context_length
        self._default_length = len(self.tokenizer.encode(self.BUFFER['essential'])) if essential else 0

        assert self._default_length <= self._max_length, f'Essential text must be less than {self._max_length} tokens.'
    
    def set_essential(self, text : str) -> None:
        """
        Sets the essential text.

        Args:
            text (str): The new essential text.
        """
        assert len(self.tokenizer.encode(text)) <= self._max_length, f'Essential text must be less than {self._max_length} tokens.'
        self.BUFFER['essential'] = text
        self._default_length = len(self.tokenizer.encode(self.BUFFER['essential']))

    def extend_essential(self, text : str) -> None:
        """
        Sets the essential text.

        Args:
            text (str): The new essential text.
        """
        if len(self.tokenizer.encode(text + self.JOIN)) + len(self.BUFFER['essential']) <= self.length:
            logging.WARN(f'Essential text must be less than {self.length} characters. No Change Made')
        else: self.BUFFER['essential'] += self.join + text

    def insert(self, item : Any) -> None:
        """
        Inserts the given item into the main buffer. If the item is a list, each element is inserted individually.

        Args:
            item (Any): The item to insert into the main buffer.
        """
        if isinstance(item, list): self.BUFFER['main'].extend(item)
        else: self.BUFFER['main'].append(item)

    def clear(self) -> None:
        """
        Clears the main buffer.
        """
        self.BUFFER['main'] = []

    def get_maximum_context(self, new_string='') -> str:
        """
        Gets the maximum context that can be included in the buffer, given a new string.

        Args:
            new_string (str, optional): The new string to consider when calculating the maximum context. Defaults to ''.

        Returns:
            str: The maximum context that can be included in the buffer.
        """
        essential_len = self._default_length + len(self.tokenizer.encode(new_string))
        current_len = essential_len
        for i, item in enumerate(self.BUFFER['main'][::-1]):
            item_len = len(self.tokenizer.encode(item))
            if current_len + item_len + 1 > self._max_length:
                return self.JOIN.join([*self.BUFFER['essential'], *self.BUFFER['main'][:i:-1], new_string])
            else:
                current_len += item_len + 1
        return self.JOIN.join([*self.BUFFER['essential'], *self.BUFFER['main'], new_string])
    
    def logic(self, text : str) -> str:
        return self.get_maximum_context(text)
        
class ConversationMemory(StringLengthBuffer):
    """
    The ConversationMemory class is a concrete implementation of the StringLengthBuffer class that buffers a conversation.
    """
    def __init__(self, 
                 model_id : str,
                 input_prefix : str = 'Human:', 
                 output_prefix : str = 'AI:', 
                 context_length : int = 20, 
                 join: str = '\n',
                 essential : str = None) -> None:
        """
        Initializes the ConversationMemory object.

        Args:
            model_id (str): The identifier of the model used for tokenization.
            input_prefix (str, optional): The prefix for user inputs. Defaults to 'Human:'.
            output_prefix (str, optional): The prefix for AI outputs. Defaults to 'AI:'.
            context_length (int, optional): The maximum length of the buffer in terms of the number of tokens. Defaults to 20.
            join (str, optional): The string used to join the buffered strings when they are retrieved. Defaults to '\n'.
            essential (str, optional): An essential string that is always included in the buffer. Defaults to None.
        """
        super().__init__(context_length=context_length, model_id=model_id, join=join, essential=essential)
        self.input_prefix = input_prefix
        self.output_prefix = output_prefix
    
    def single_insert(self, item : Tuple[Any, Any]) -> None:
        """
        Inserts the given item into the main buffer. The item is a tuple where the first element is the user input and the second element is the AI output.

        Args:
            item (Tuple[Any, Any]): The item to insert into the main buffer.
        """
        user, ai = item 
        self.BUFFER['main'].append(self.input_prefix + user)
        self.BUFFER['main'].append(self.output_prefix + ai)
    
    def insert(self, item : Union[Tuple[Any, Any], List[Tuple[Any, Any]]]) -> None:
        if isinstance(item, list): 
            for i in item: self.single_insert(i)
        else: self.single_insert(item)