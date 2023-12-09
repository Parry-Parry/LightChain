# Chain

[Lightchain Index](../README.md#lightchain-index) /
[Lightchain](./index.md#lightchain) /
Chain

> Auto-generated documentation for [lightchain.chain](../../lightchain/chain.py) module.

- [Chain](#chain)
  - [SwitchBoardChain](#switchboardchain)
    - [SwitchBoardChain().logic](#switchboardchain()logic)
    - [SwitchBoardChain().parse](#switchboardchain()parse)

## SwitchBoardChain

[Show source in chain.py:5](../../lightchain/chain.py#L5)

Present the LLM with a list of options, and then return the output of the selected option.

Usage:

```python
>>> LLM = Model()
>>> chain = SwitchBoardChain(LLM, [chain1, chain2, chain3])
>>> out = chain(input)
```

#### Signature

```python
class SwitchBoardChain(Link):
    def __init__(
        self,
        model: Any,
        links: List[Link],
        name: str = "Switchboard",
        description: str = "Some Switchboard",
    ) -> None: ...
```

#### See also

- [Link](link/index.md#link)

### SwitchBoardChain().logic

[Show source in chain.py:25](../../lightchain/chain.py#L25)

#### Signature

```python
def logic(self, input: Tuple[List[str], str]) -> Any: ...
```

### SwitchBoardChain().parse

[Show source in chain.py:21](../../lightchain/chain.py#L21)

#### Signature

```python
def parse(self, input: str) -> str: ...
```