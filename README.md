<p align="center">
  <img align="center" src="docs/img/chain_white.png" width="460px" />
</p>
<p align="left">

# LightChain - Stupidly Simple Chain Structures

LightChain is a tiny library to connect components in complex NLP tasks, designed for research and compatibility with literally anything.

## Install
```
pip install --upgrade git+https://github.com/Parry-Parry/LightChain.git
```

## The Most Basic Use Case

Use our AutoPrompt, which extracts your arguments and allows for the convenient passing of multiple examples.

```
from lightchain import AutoPrompt

prompt = AutoPrompt.from_string('You are a helpful assistant \n Write a response which answers the question \n Question: {} \n Response:')
value = prompt(text=text)
```

## More Complex Use Cases

Here are some of the powerful uses of LightChain. 

### The Notion of a Chain

We have two main abstractions in Lightchain. Chains are composed of links. A Link is always defined explicitly, whereas a Chain is generally implicit.

* Link: An atomic component of a system, its internals may be accessed but generally will only use __call__
* Chain: Multiple links, a chain can mix sequential and branching components to model any desired behaviour

### Defining a Link

Links are defined in two ways:
* Subclassing 'Link': When directly inheriting from Link, you have to overload the 'logic' function. This will allow LightChain to infer signatures and appropriately build your chain
* Using the @chainable decorator: This decorator allows anything that can be called to be used in a chain. This decorator optionally takes in a call attribute, which should be the underlying method to receive input in the chain. Logic is then implemented for you, and the signature of the Link is determined by the signature of the call attribute (__call__ by default)

### Defining a Chain

A chain is many connected links; crucially, they do not have to be sequential. We overload the '>>' operator to link chains sequentially and the '|' operator to branch to multiple links.

### Usage

Let's turn a HuggingFace model into a Link.

```
from lightchain import chainable, AutoPrompt
from transformers import AutoModelForCausalLM, AutoTokenizer

model_link = chainable(AutoModelForCausalLM, call='generate' name='Llama Model')
tokenize_link = chainable(AutoTokenizer, call='batch_encode', name='Llama Tokenizer')

MODEL_ID = 'meta-llama/Llama-2-7b-chat-hf'

llama = model_link(MODEL_ID) # If you need to add generation kwargs use functools.partial
llama_tokenizer = tokenize_link(MODEL_ID)
prompt = AutoPrompt.from_string('You are a helpful assistant \n Write a response which answers the question \n Question: {} \n Response:')

pipeline = prompt >> llama_tokenizer >> llama

output = pipeline(text="Do you think most prompting libraries are over-engineered?")
```

Now, let's take that previous pipeline and make it use RAG. We will explicitly define a link as we are going to interface with a more complex API (The wonderful PyTerrier)

```
from lightchain import Link
from typing import List, Tuple
import pyterrier as pt
if not pt.started(): pt.init()

from pyterrier import BatchRetrieve

prompt = AutoPrompt.from_string('You are a helpful assistant \n Write a response which answers the question given the context \n Question: {question} \n Context: {context} \n Response:')

@chainable(name='BM25', desc='A Lexical Model')
class BM25:
    def __init__(dataset : str, num_results : int = 10, text_attr : str = 'body'):
        text_ref = pt.get_dataset(dataset)
        self.transformer = pt.BatchRetrieve.from_dataset(dataset, "terrier_stemmed", wmodel="BM25") % num_results >> pt.text.get_text(text_ref, text_attr)

    def logic(text : Tuple[List[str], str]) -> Tuple[List[str], str]:
        # Let's keep it simple and return the full string
        import pandas as pd
        if isinstance(text, list):
            frame = pd.DataFrame({'qid' : [*range(len(text))], 'query' : text})
            docs = self.transformer(frame)
            context = docs.groupby('qid')['text'].agg(lambda x: ' '.join(x)).text.tolist()
        else: # assumes string
            docs = self.transformer.search(text)
            context = ''.join(docs.text.tolist())
        return {'question' : text, 'context' : context}

bm25 = BM25('msmarco_passage')

# Using our classes from before

pipeline = BM25 >> prompt >> llama_tokenizer >> llama

output = pipeline(text="Do you think most prompting libraries are over-engineered?")
```

Let's say we want to assess my RAG setup with a different model e.g. Mistral-7B, whilst also getting Llama output.

```
MODEL_ID = 'mistralai/Mistral-7B-Instruct-v0.1'
mistral = model_link(MODEL_ID, name='Mistral Model')
mistral_tokenizer = tokenizer_link(MODEL_ID, name='Mistral Tokenizer')

pipeline = bm25 >> prompt >> (mistral_tokenizer >> mistral) | (llama_tokenizer >> llama) 
```
