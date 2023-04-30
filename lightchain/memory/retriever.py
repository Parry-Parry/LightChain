from abc import ABC, abstractmethod

"""
Simple Wrapper for a retriever. Not needed if direct call available on function passed to memory.
"""

class Retriever(ABC):
    def __init__(self, retriever) -> None:
        self.retriever = retriever

    @abstractmethod
    def __call__(self, *args, **kwargs) -> str:
        raise NotImplementedError