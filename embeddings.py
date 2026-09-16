from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks_metadata = []

    def build_index(self, chunks):
        if not chunks:
            return
        
        self.chunks_metadata = chunks
        texts = [chunk['text'] for chunk in chunks]
        
        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]
        
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        print(f"Index built with {len(chunks)} chunks.")

    def retrieve(self, query, top_k=3):
        if self.index is None:
            return []
        
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks_metadata):
                result = self.chunks_metadata[idx].copy()
                result['distance'] = float(distances[0][i])
                results.append(result)
        return results
