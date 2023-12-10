# Prompt

[Lightchain Index](../README.md#lightchain-index) /
[Lightchain](./index.md#lightchain) /
Prompt

> Auto-generated documentation for [lightchain.prompt](../../lightchain/prompt.py) module.

- [Prompt](#prompt)
  - [AutoPrompt](#autoprompt)
    - [AutoPrompt.from_json](#autopromptfrom_json)
    - [AutoPrompt.from_string](#autopromptfrom_string)
  - [StructPrompt](#structprompt)

## AutoPrompt

[Show source in prompt.py:6](../../lightchain/prompt.py#L6)

The AutoPrompt class represents a self-parsing prompt. It inherits from the Link class.

#### Attributes

- `pattern` *str* - The regex pattern used to parse the prompt.
- `prompt` *str* - The prompt string.
- `params` *list* - The parameters found in the prompt string.
- `name` *str* - The name of the AutoPrompt object. Default is 'AutoPrompt'.
- `description` *str* - The description of the AutoPrompt object. Default is 'Self Parsing Prompt'.

#### Arguments

- `prompt` *str* - The prompt string.
- `name` *str, optional* - The name of the AutoPrompt object. Defaults to 'AutoPrompt'.
- `description` *str, optional* - The description of the AutoPrompt object. Defaults to 'Self Parsing Prompt'.

#### Signature

```python
class AutoPrompt(Link):
    def __init__(
        self, prompt: str, name="AutoPrompt", description="Self Parsing Prompt"
    ) -> None: ...
```

#### See also

- [Link](link/index.md#link)

### AutoPrompt.from_json

[Show source in prompt.py:34](../../lightchain/prompt.py#L34)

#### Signature

```python
@staticmethod
def from_json(json_str: str) -> "AutoPrompt": ...
```

### AutoPrompt.from_string

[Show source in prompt.py:38](../../lightchain/prompt.py#L38)

#### Signature

```python
@staticmethod
def from_string(
    string: str, name: str = "AutoPrompt", description: str = "Self Parsing Prompt"
) -> "AutoPrompt": ...
```



## StructPrompt

[Show source in prompt.py:59](../../lightchain/prompt.py#L59)

#### Signature

```python
class StructPrompt(Link):
    def __init__(self, **kwargs) -> None: ...
```

#### See also

- [Link](link/index.md#link)