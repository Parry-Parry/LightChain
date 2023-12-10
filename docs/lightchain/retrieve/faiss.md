# Faiss

[Lightchain Index](../../README.md#lightchain-index) /
[Lightchain](../index.md#lightchain) /
[Retrieve](./index.md#retrieve) /
Faiss

> Auto-generated documentation for [lightchain.retrieve.faiss](../../../lightchain/retrieve/faiss.py) module.

- [Faiss](#faiss)
  - [FaissEmbeddingMemory](#faissembeddingmemory)
    - [FaissEmbeddingMemory().insert](#faissembeddingmemory()insert)
    - [FaissEmbeddingMemory().load](#faissembeddingmemory()load)
    - [FaissEmbeddingMemory().logic](#faissembeddingmemory()logic)
    - [FaissEmbeddingMemory().max_id](#faissembeddingmemory()max_id)
    - [FaissEmbeddingMemory().save](#faissembeddingmemory()save)

## FaissEmbeddingMemory

[Show source in faiss.py:7](../../../lightchain/retrieve/faiss.py#L7)

#### Signature

```python
class FaissEmbeddingMemory(Memory):
    def __init__(
        self,
        faiss_object: Union[list, faiss.Index],
        encoder: Optional[Any],
        ngpu: int = 0,
        **kwargs
    ) -> None: ...
```

### FaissEmbeddingMemory().insert

[Show source in faiss.py:25](../../../lightchain/retrieve/faiss.py#L25)

#### Signature

```python
def insert(self, documents: Union[List[str], str]) -> None: ...
```

### FaissEmbeddingMemory().load

[Show source in faiss.py:20](../../../lightchain/retrieve/faiss.py#L20)

#### Signature

```python
def load(self, string: str) -> None: ...
```

### FaissEmbeddingMemory().logic

[Show source in faiss.py:43](../../../lightchain/retrieve/faiss.py#L43)

#### Signature

```python
def logic(
    self, query: Union[np.array, List[str], str], search_kwargs: dict
) -> Union[List[str], str]: ...
```

### FaissEmbeddingMemory().max_id

[Show source in faiss.py:16](../../../lightchain/retrieve/faiss.py#L16)

#### Signature

```python
@property
def max_id(self) -> int: ...
```

### FaissEmbeddingMemory().save

[Show source in faiss.py:40](../../../lightchain/retrieve/faiss.py#L40)

#### Signature

```python
def save(self, path: str) -> None: ...
```