from __future__ import annotations
import re
from data_prep.passages import Passage
import pickle 
import math
import numpy as np

from pathlib import Path

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")

def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall((text or "").lower())

class BM25:
    passages: list[Passage]

    #Index params
    corpus_size: int = 0 #in documents
    avgdl: float = 0.0
    doc_len: list[int] = []
    doc_freq: list[dict[str, int]] = {}
    idf: dict[str, float] = {}

    token_df_map :dict[str, int] = {}
    
    k1: float = 1.5
    b: float = 0.75
    epsilon: float = 0.25

    def __init__(self, passages:list[Passage], k1 = 1.5, b = 0.75, epsilon = 0.25,) -> None:
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.passages = passages
        

    def calc_idf(self, nd):
    
        idf_sum = 0
        negative_idfs = []
        for word, freq in nd.items():
            idf = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5))
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps
        return;

    def build_index(self,passages_text: list[str]) -> BM25:
        corpus_tokens = [tokenize(p.text) for p in passages_text] #List of list of strings
        doc_len_sum = 0

        for document in corpus_tokens:
            self.doc_len.append(len(document))
            doc_len_sum += len(document)

            current_freq = {}
            for token in document:
                if token not in current_freq:
                    current_freq[token] = 0
                current_freq[token] += 1;
            self.doc_freq.append(current_freq)

            for token,freq in current_freq.items():
                if token not in self.token_doc_:
                    self.token_df_map[token] = 0
                self.token_df_map[token] +=1 ;

            self.corpus_size += 1;

        self.avgdl = doc_len_sum / self.corpus_size
        self.calc_idf(self.token_df_map)
        return;
        
    def get_scores(self, query):

        score = np.zeros(self.corpus_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) / (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score

    

def load_bm25(path: Path) -> BM25:
    with path.open("rb") as f:
        obj = pickle.load(f)
        return obj

def save_bm25(index: BM25, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(index, f)
    


if __name__ == "__main__":
    test = load_bm25(Path("dataset/bm25_index.pkl"))
    print("hello")