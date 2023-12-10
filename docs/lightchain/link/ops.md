# Ops

[Lightchain Index](../../README.md#lightchain-index) /
[Lightchain](../index.md#lightchain) /
[Link](./index.md#link) /
Ops

> Auto-generated documentation for [lightchain.link.ops](../../../lightchain/link/ops.py) module.

- [Ops](#ops)
  - [CAT](#cat)
    - [CAT().logic](#cat()logic)
  - [Chain](#chain)
  - [ForkChain](#forkchain)
    - [ForkChain().__call__](#forkchain()__call__)
  - [SequentialChain](#sequentialchain)
    - [SequentialChain().__call__](#sequentialchain()__call__)
    - [SequentialChain().logic](#sequentialchain()logic)
  - [get_link](#get_link)

## CAT

[Show source in ops.py:144](../../../lightchain/link/ops.py#L144)

#### Signature

```python
class CAT(Link):
    def __init__(self, char="\n") -> None: ...
```

### CAT().logic

[Show source in ops.py:149](../../../lightchain/link/ops.py#L149)

#### Signature

```python
def logic(self, *args: Union[List[str], str], **kwargs: Dict[Any, str]) -> Any: ...
```



## Chain

[Show source in ops.py:31](../../../lightchain/link/ops.py#L31)

The Chain class represents a sequence of operations (Links) to be performed in a specific order.
It inherits from both the Link and Operation classes.

#### Attributes

- `name` *str* - The name of the Chain object. Default is 'Chain'.
- `arity` *Arity* - The matchpy arity of the Chain object. Effectively can it take >2 operands Default is Arity.polyadic.
- `links` *dict* - A dictionary mapping link names to Link objects. It is populated in the initializer.

#### Arguments

- `operands` *Iterable* - An iterable of objects to be coerced into Link objects and added to the Chain.
- `**kwargs` - Additional keyword arguments are passed to the super class initializers.

#### Signature

```python
class Chain(Link, Operation):
    def __init__(self, operands: Iterable, **kwargs): ...
```



## ForkChain

[Show source in ops.py:111](../../../lightchain/link/ops.py#L111)

The ForkChain class represents a set of operations (Links) to be performed in parallel.

#### Attributes

- `name` *str* - The name of the ForkChain object. Default is 'Forked Chain'.

#### Arguments

- `operands` *Iterable* - An iterable of objects to be coerced into Link objects and added to the Chain.
- `**kwargs` - Additional keyword arguments are passed to the super class initializers.

#### Signature

```python
class ForkChain(Chain):
    def __init__(self, operands: Iterable, **kwargs): ...
```

#### See also

- [Chain](#chain)

### ForkChain().__call__

[Show source in ops.py:126](../../../lightchain/link/ops.py#L126)

Applies each link in the Chain to the input in parallel.

#### Arguments

- `*args` - The input to the Chain.
- `**kwargs` - Additional keyword arguments are passed to the link.

#### Returns

- `Any` - The output of the Chain.

#### Signature

```python
def __call__(self, *args, **kwargs) -> Any: ...
```



## SequentialChain

[Show source in ops.py:61](../../../lightchain/link/ops.py#L61)

The SequentialChain class represents a sequence of operations (Links) to be performed in a specific order.
It inherits from the Chain class.

#### Attributes

- `name` *str* - The name of the SequentialChain object. Default is 'Sequential Chain'.

#### Arguments

- `operands` *Iterable* - An iterable of objects to be coerced into Link objects and added to the Chain.
- `**kwargs` - Additional keyword arguments are passed to the super class initializers.

#### Signature

```python
class SequentialChain(Chain):
    def __init__(self, operands: Iterable, **kwargs): ...
```

#### See also

- [Chain](#chain)

### SequentialChain().__call__

[Show source in ops.py:97](../../../lightchain/link/ops.py#L97)

Calls the 'logic' method with the given arguments.

#### Arguments

- `*args` - The input to the Chain.
- `**kwargs` - Additional keyword arguments are passed to the link.

#### Returns

- `Any` - The output of the Chain.

#### Signature

```python
def __call__(self, *args, **kwargs) -> Any: ...
```

### SequentialChain().logic

[Show source in ops.py:80](../../../lightchain/link/ops.py#L80)

Implements the logic of the SequentialChain. It applies each link in the Chain to the input in order.

#### Arguments

- `args` *Any* - The input to the Chain.
- `**kwargs` - Additional keyword arguments are passed to the link.

#### Returns

- `Any` - The output of the Chain.

#### Signature

```python
def logic(self, args, **kwargs): ...
```



## get_link

[Show source in ops.py:8](../../../lightchain/link/ops.py#L8)

Coerces a given object into a chainable Link object if possible.

#### Arguments

- `link` *Any* - The object to be coerced into a Link object.

#### Returns

- `Any` - The coerced Link object if possible, otherwise raises a ValueError.

#### Raises

- `ValueError` - If the passed object cannot be coerced into a Link object.

#### Signature

```python
def get_link(link) -> Any: ...
```