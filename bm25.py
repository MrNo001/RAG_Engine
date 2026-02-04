from __future__ import annotations
import re
from data_prep.passages import Passage
import pickle 

from pathlib import Path

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")

def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall((text or "").lower())

class BM25_Index:
    passages: list[Passage]

    #Index params
    corpus_size: int = 0 #in documents
    avgdl: float = 0.0
    doc_len: list[int] = []
    doc_freq: list[dict[str, int]] = {}
    idf: dict[str, float] = {}

    docs_with_token :dict[str, int] = {}

    def build_index(self,passages: list[Passage]) -> BM25_Index:
        corpus_tokens = [tokenize(p.text) for p in passages] #List of list of strings
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
                if token not in self.docs_with_token:
                    self.docs_with_token[token] = 0
                self.docs_with_token[token] +=1 ;

            self.corpus_size += 1;

        self.avgdl = doc_len_sum / self.corpus_size


def load_bm25(path: Path) -> BM25_Index:
    with path.open("rb") as f:
        obj = pickle.load(f)
        return obj

def save_bm25(index: BM25_Index, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(index, f)

class BM25:
    k1: float = 1.5
    b: float = 0.75
    epsilon: float = 0.25
    index: BM25_Index

    def _calc_idf(self, nd):
        """
        Calculates frequencies of terms in documents and in corpus.
        This algorithm sets a floor on the idf values to eps * average_idf
        """
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in nd.items():
            idf = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps



def test_bm25():
    


if __name__ == "__main__":
    test_bm25()