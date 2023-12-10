from .memory import Memory

class FaissEmbeddingMemory(Memory):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)