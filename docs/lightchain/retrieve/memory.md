# Memory

[Lightchain Index](../../README.md#lightchain-index) /
[Lightchain](../index.md#lightchain) /
[Retrieve](./index.md#retrieve) /
Memory

> Auto-generated documentation for [lightchain.retrieve.memory](../../../lightchain/retrieve/memory.py) module.

- [Memory](#memory)
  - [ConversationMemory](#conversationmemory)
    - [ConversationMemory().insert](#conversationmemory()insert)
    - [ConversationMemory().single_insert](#conversationmemory()single_insert)
  - [DictMemory](#dictmemory)
    - [DictMemory().clear](#dictmemory()clear)
    - [DictMemory().insert](#dictmemory()insert)
    - [DictMemory().logic](#dictmemory()logic)
  - [Memory](#memory-1)
    - [Memory().insert](#memory()insert)
  - [StringLengthBuffer](#stringlengthbuffer)
    - [StringLengthBuffer().clear](#stringlengthbuffer()clear)
    - [StringLengthBuffer().extend_essential](#stringlengthbuffer()extend_essential)
    - [StringLengthBuffer().get_maximum_context](#stringlengthbuffer()get_maximum_context)
    - [StringLengthBuffer().insert](#stringlengthbuffer()insert)
    - [StringLengthBuffer().logic](#stringlengthbuffer()logic)
    - [StringLengthBuffer().set_essential](#stringlengthbuffer()set_essential)

## ConversationMemory

[Show source in memory.py:134](../../../lightchain/retrieve/memory.py#L134)

The ConversationMemory class is a concrete implementation of the StringLengthBuffer class that buffers a conversation.

#### Signature

```python
class ConversationMemory(StringLengthBuffer):
    def __init__(
        self,
        model_id: str,
        input_prefix: str = "Human:",
        output_prefix: str = "AI:",
        context_length: int = 20,
        join: str = "\n",
        essential: str = None,
    ) -> None: ...
```

#### See also

- [StringLengthBuffer](#stringlengthbuffer)

### ConversationMemory().insert

[Show source in memory.py:171](../../../lightchain/retrieve/memory.py#L171)

#### Signature

```python
def insert(self, item: Union[Tuple[Any, Any], List[Tuple[Any, Any]]]) -> None: ...
```

### ConversationMemory().single_insert

[Show source in memory.py:160](../../../lightchain/retrieve/memory.py#L160)

Inserts the given item into the main buffer. The item is a tuple where the first element is the user input and the second element is the AI output.

#### Arguments

item (Tuple[Any, Any]): The item to insert into the main buffer.

#### Signature

```python
def single_insert(self, item: Tuple[Any, Any]) -> None: ...
```



## DictMemory

[Show source in memory.py:18](../../../lightchain/retrieve/memory.py#L18)

The DictMemory class is a concrete implementation of the Memory class using a dictionary as the underlying data structure.

#### Signature

```python
class DictMemory(Memory):
    def __init__(self, **kwargs) -> None: ...
```

#### See also

- [Memory](#memory)

### DictMemory().clear

[Show source in memory.py:35](../../../lightchain/retrieve/memory.py#L35)

Clears the buffer.

#### Signature

```python
def clear(self) -> None: ...
```

### DictMemory().insert

[Show source in memory.py:29](../../../lightchain/retrieve/memory.py#L29)

Inserts the given keyword arguments into the buffer.

#### Signature

```python
def insert(self, **kwargs) -> None: ...
```

### DictMemory().logic

[Show source in memory.py:41](../../../lightchain/retrieve/memory.py#L41)

Retrieves the values associated with the given keys from the buffer.

#### Signature

```python
def logic(self, keys) -> Any: ...
```



## Memory

[Show source in memory.py:6](../../../lightchain/retrieve/memory.py#L6)

The Memory class is an abstract base class for memory operations.
It provides methods for inserting data and calling the memory.

#### Signature

```python
class Memory(Link):
    def __init__(self, **kwargs) -> None: ...
```

### Memory().insert

[Show source in memory.py:14](../../../lightchain/retrieve/memory.py#L14)

#### Signature

```python
@abstractmethod
def insert(self, *args, **kwargs) -> None: ...
```



## StringLengthBuffer

[Show source in memory.py:49](../../../lightchain/retrieve/memory.py#L49)

The StringLengthBuffer class is a concrete implementation of the DictMemory class that buffers strings of a certain length.

#### Signature

```python
class StringLengthBuffer(DictMemory):
    def __init__(
        self, context_length: int, model_id: str, join: str = "\n", essential=None
    ) -> None: ...
```

#### See also

- [DictMemory](#dictmemory)

### StringLengthBuffer().clear

[Show source in memory.py:105](../../../lightchain/retrieve/memory.py#L105)

Clears the main buffer.

#### Signature

```python
def clear(self) -> None: ...
```

### StringLengthBuffer().extend_essential

[Show source in memory.py:84](../../../lightchain/retrieve/memory.py#L84)

Sets the essential text.

#### Arguments

- `text` *str* - The new essential text.

#### Signature

```python
def extend_essential(self, text: str) -> None: ...
```

### StringLengthBuffer().get_maximum_context

[Show source in memory.py:111](../../../lightchain/retrieve/memory.py#L111)

Gets the maximum context that can be included in the buffer, given a new string.

#### Arguments

- `new_string` *str, optional* - The new string to consider when calculating the maximum context. Defaults to ''.

#### Returns

- `str` - The maximum context that can be included in the buffer.

#### Signature

```python
def get_maximum_context(self, new_string="") -> str: ...
```

### StringLengthBuffer().insert

[Show source in memory.py:95](../../../lightchain/retrieve/memory.py#L95)

Inserts the given item into the main buffer. If the item is a list, each element is inserted individually.

#### Arguments

- `item` *Any* - The item to insert into the main buffer.

#### Signature

```python
def insert(self, item: Any) -> None: ...
```

### StringLengthBuffer().logic

[Show source in memory.py:131](../../../lightchain/retrieve/memory.py#L131)

#### Signature

```python
def logic(self, text: str) -> str: ...
```

### StringLengthBuffer().set_essential

[Show source in memory.py:73](../../../lightchain/retrieve/memory.py#L73)

Sets the essential text.

#### Arguments

- `text` *str* - The new essential text.

#### Signature

```python
def set_essential(self, text: str) -> None: ...
```