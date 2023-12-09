# Memory

[Lightchain Index](../../README.md#lightchain-index) /
[Lightchain](../index.md#lightchain) /
[Retrieve](./index.md#retrieve) /
Memory

> Auto-generated documentation for [lightchain.retrieve.memory](../../../lightchain/retrieve/memory.py) module.

- [Memory](#memory)
  - [ConversationMemory](#conversationmemory)
    - [ConversationMemory().extend](#conversationmemory()extend)
    - [ConversationMemory().insert](#conversationmemory()insert)
  - [DictMemory](#dictmemory)
    - [DictMemory().clear](#dictmemory()clear)
    - [DictMemory().insert](#dictmemory()insert)
  - [Memory](#memory-1)
    - [Memory().insert](#memory()insert)
  - [StringLengthBuffer](#stringlengthbuffer)
    - [StringLengthBuffer().clear](#stringlengthbuffer()clear)
    - [StringLengthBuffer().extend_essential](#stringlengthbuffer()extend_essential)
    - [StringLengthBuffer().get_maximum_context](#stringlengthbuffer()get_maximum_context)
    - [StringLengthBuffer().insert](#stringlengthbuffer()insert)
    - [StringLengthBuffer().set_essential](#stringlengthbuffer()set_essential)

## ConversationMemory

[Show source in memory.py:77](../../../lightchain/retrieve/memory.py#L77)

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

### ConversationMemory().extend

[Show source in memory.py:94](../../../lightchain/retrieve/memory.py#L94)

#### Signature

```python
def extend(self, items: Any) -> None: ...
```

### ConversationMemory().insert

[Show source in memory.py:89](../../../lightchain/retrieve/memory.py#L89)

#### Signature

```python
def insert(self, item: Any) -> None: ...
```



## DictMemory

[Show source in memory.py:18](../../../lightchain/retrieve/memory.py#L18)

#### Signature

```python
class DictMemory(Memory):
    def __init__(self, **kwargs) -> None: ...
```

#### See also

- [Memory](#memory)

### DictMemory().clear

[Show source in memory.py:26](../../../lightchain/retrieve/memory.py#L26)

#### Signature

```python
def clear(self) -> None: ...
```

### DictMemory().insert

[Show source in memory.py:23](../../../lightchain/retrieve/memory.py#L23)

#### Signature

```python
def insert(self, **kwargs) -> None: ...
```



## Memory

[Show source in memory.py:6](../../../lightchain/retrieve/memory.py#L6)

#### Signature

```python
class Memory(Link):
    def __init__(self, **kwargs) -> None: ...
```

### Memory().insert

[Show source in memory.py:10](../../../lightchain/retrieve/memory.py#L10)

#### Signature

```python
@abstractmethod
def insert(self, *args, **kwargs) -> None: ...
```



## StringLengthBuffer

[Show source in memory.py:34](../../../lightchain/retrieve/memory.py#L34)

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

[Show source in memory.py:60](../../../lightchain/retrieve/memory.py#L60)

#### Signature

```python
def clear(self) -> None: ...
```

### StringLengthBuffer().extend_essential

[Show source in memory.py:51](../../../lightchain/retrieve/memory.py#L51)

#### Signature

```python
def extend_essential(self, text: str) -> None: ...
```

### StringLengthBuffer().get_maximum_context

[Show source in memory.py:63](../../../lightchain/retrieve/memory.py#L63)

#### Signature

```python
def get_maximum_context(self, new_string="") -> str: ...
```

### StringLengthBuffer().insert

[Show source in memory.py:56](../../../lightchain/retrieve/memory.py#L56)

#### Signature

```python
def insert(self, item: Any) -> None: ...
```

### StringLengthBuffer().set_essential

[Show source in memory.py:46](../../../lightchain/retrieve/memory.py#L46)

#### Signature

```python
def set_essential(self, text: str) -> None: ...
```