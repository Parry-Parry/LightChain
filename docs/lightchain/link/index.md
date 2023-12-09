# Link

[Lightchain Index](../../README.md#lightchain-index) /
[Lightchain](../index.md#lightchain) /
Link

> Auto-generated documentation for [lightchain.link](../../../lightchain/link/__init__.py) module.

- [Link](#link)
  - [Link](#link-1)
    - [Link().logic](#link()logic)
  - [SkipLink](#skiplink)
    - [SkipLink().logic](#skiplink()logic)
  - [chainable](#chainable)
  - [Modules](#modules)

## Link

[Show source in __init__.py:6](../../../lightchain/link/__init__.py#L6)

A base class for creating pipeline operations.
It provides methods for chaining operations in a sequential or forked manner.

#### Attributes

- `name` *str* - The name of the Link object. Default is 'Link'.
- `description` *str* - The description of the Link object. Default is 'A Link'.
- `signature` *str* - The signature of the logic method. It is set in the initializer.

#### Signature

```python
class Link(object):
    def __init__(self, **kwargs) -> None: ...
```

### Link().logic

[Show source in __init__.py:39](../../../lightchain/link/__init__.py#L39)

#### Signature

```python
@abstractmethod
def logic(self, *args: Any, **kwargs: Any) -> Any: ...
```



## SkipLink

[Show source in __init__.py:71](../../../lightchain/link/__init__.py#L71)

#### Signature

```python
class SkipLink(Link):
    def __init__(self, **kwargs) -> None: ...
```

#### See also

- [Link](#link)

### SkipLink().logic

[Show source in __init__.py:77](../../../lightchain/link/__init__.py#L77)

#### Signature

```python
def logic(self, *args, **kwargs) -> Any: ...
```



## chainable

[Show source in __init__.py:46](../../../lightchain/link/__init__.py#L46)

Wraps a class to make it chainable in a pipeline. The wrapped class inherits from the Link class.

#### Arguments

- `cls` *type* - The class to be wrapped.
call (str or callable, optional): The method of the class to be called when the object is called. If a callable is passed, it is used directly. Defaults to '__call__'.
- `name` *str, optional* - The name of the Link object.
- `description` *str, optional* - The description of the Link object.

#### Returns

- `Wrapper` - The wrapped class.

#### Signature

```python
def chainable(
    cls,
    call="__call__",
    name="External Object",
    description="We don't know what this is but it's probably important",
): ...
```



## Modules

- [Ops](./ops.md)