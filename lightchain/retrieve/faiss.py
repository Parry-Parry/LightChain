from .memory import Memory

class FaissIndex(Memory):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)