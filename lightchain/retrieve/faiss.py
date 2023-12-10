from typing import Any, List, Union, Optional
from .memory import Memory
import faiss 
from faiss import index_factory
import numpy as np

class FaissEmbeddingMemory(Memory):
    def __init__(self, faiss_object : Union[list, faiss.Index], encoder : Optional[Any], ngpu : int = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        if isinstance(faiss_object, dict): self.index =  index_factory(*faiss_object)
        else: self.index = faiss_object
        self.encoder = encoder
        self.id2doc = {}
        self.resources = [faiss.StandardGpuResources() for _ in range(ngpu)] if ngpu > 0 else None
        
    @property
    def max_id(self) -> int:
        return self.index.ntotal if self.index.is_trained else 0
    
    def load(self, string : str) -> None:
        index = faiss.read_index(string)
        if self.resources: faiss.index_cpu_to_gpu_multiple_py(self.resources, index)
        self.index = index

    def insert(self, documents : Union[List[str], str]) -> None:
        if isinstance(documents, str): documents = [documents]
        if isinstance(documents, list): 
            if self.encoder is not None: 
                vectors = self.encoder(documents)
            else: raise ValueError('No encoder provided, pre-encode documents before inserting them into the memory.')

        ids = np.arange(self.max_id, self.max_id + len(vectors))
        # create id2doc mapping
        self.id2doc.update({id : doc for id, doc in zip(ids, documents)})
        
        if not self.index.is_trained:
            self.index.train(vectors)
        self.index.add_with_ids(vectors, ids)
    
    def save(self, path : str) -> None:
        faiss.write_index(self.index, path)

    def logic(self, query : Union[np.array, List[str], str], k : int = 1) -> Union[List[str], str]:
        if isinstance(query, str): query = [query]
        if isinstance(query, list): 
            if self.encoder is not None: 
                vectors = self.encoder(query)
            else: raise ValueError('No encoder provided, pre-encode queries before searching.')
        _, indices = self.index.search(vectors, k)
        if len(query) == 1: return [self.id2doc[index] for index in indices[0]]
        else: return [[self.id2doc[index] for index in query_indices] for query_indices in indices]