# Ops

[Lightchain Index](../../README.md#lightchain-index) /
[Lightchain](../index.md#lightchain) /
[Link](./index.md#link) /
Ops

> Auto-generated documentation for [lightchain.link.ops](../../../lightchain/link/ops.py) module.

- [Ops](#ops)
  - [ForkPipeline](#forkpipeline)
    - [ForkPipeline().__call__](#forkpipeline()__call__)
  - [Pipeline](#pipeline)
  - [SequentialPipeline](#sequentialpipeline)
    - [SequentialPipeline().__call__](#sequentialpipeline()__call__)
    - [SequentialPipeline().logic](#sequentialpipeline()logic)
  - [get_link](#get_link)

## ForkPipeline

[Show source in ops.py:111](../../../lightchain/link/ops.py#L111)

The ForkPipeline class represents a set of operations (Links) to be performed in parallel.

#### Attributes

- `name` *str* - The name of the ForkPipeline object. Default is 'Forked Pipeline'.

#### Arguments

- `operands` *Iterable* - An iterable of objects to be coerced into Link objects and added to the pipeline.
- `**kwargs` - Additional keyword arguments are passed to the super class initializers.

#### Signature

```python
class ForkPipeline(Pipeline):
    def __init__(self, operands: Iterable, **kwargs): ...
```

#### See also

- [Pipeline](#pipeline)

### ForkPipeline().__call__

[Show source in ops.py:126](../../../lightchain/link/ops.py#L126)

Applies each link in the pipeline to the input in parallel.

#### Arguments

- `*args` - The input to the pipeline.
- `**kwargs` - Additional keyword arguments are passed to the link.

#### Returns

- `Any` - The output of the pipeline.

#### Signature

```python
def __call__(self, *args, **kwargs) -> Any: ...
```



## Pipeline

[Show source in ops.py:31](../../../lightchain/link/ops.py#L31)

The Pipeline class represents a sequence of operations (Links) to be performed in a specific order.
It inherits from both the Link and Operation classes.

#### Attributes

- `name` *str* - The name of the Pipeline object. Default is 'Pipeline'.
- `arity` *Arity* - The matchpy arity of the Pipeline object. Effectively can it take >2 operands Default is Arity.polyadic.
- `links` *dict* - A dictionary mapping link names to Link objects. It is populated in the initializer.

#### Arguments

- `operands` *Iterable* - An iterable of objects to be coerced into Link objects and added to the pipeline.
- `**kwargs` - Additional keyword arguments are passed to the super class initializers.

#### Signature

```python
class Pipeline(Link, Operation):
    def __init__(self, operands: Iterable, **kwargs): ...
```



## SequentialPipeline

[Show source in ops.py:61](../../../lightchain/link/ops.py#L61)

The SequentialPipeline class represents a sequence of operations (Links) to be performed in a specific order.
It inherits from the Pipeline class.

#### Attributes

- `name` *str* - The name of the SequentialPipeline object. Default is 'Sequential Pipeline'.

#### Arguments

- `operands` *Iterable* - An iterable of objects to be coerced into Link objects and added to the pipeline.
- `**kwargs` - Additional keyword arguments are passed to the super class initializers.

#### Signature

```python
class SequentialPipeline(Pipeline):
    def __init__(self, operands: Iterable, **kwargs): ...
```

#### See also

- [Pipeline](#pipeline)

### SequentialPipeline().__call__

[Show source in ops.py:97](../../../lightchain/link/ops.py#L97)

Calls the 'logic' method with the given arguments.

#### Arguments

- `*args` - The input to the pipeline.
- `**kwargs` - Additional keyword arguments are passed to the link.

#### Returns

- `Any` - The output of the pipeline.

#### Signature

```python
def __call__(self, *args, **kwargs) -> Any: ...
```

### SequentialPipeline().logic

[Show source in ops.py:80](../../../lightchain/link/ops.py#L80)

Implements the logic of the SequentialPipeline. It applies each link in the pipeline to the input in order.

#### Arguments

- `args` *Any* - The input to the pipeline.
- `**kwargs` - Additional keyword arguments are passed to the link.

#### Returns

- `Any` - The output of the pipeline.

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