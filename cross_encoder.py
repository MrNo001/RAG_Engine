from dataclasses import dataclass

from sentence_transformers import CrossEncoder

from data_prep.passages import Passage


@dataclass(frozen=True)
class Reranked:
    passage: Passage
    score: float


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        self.model_name = model_name
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, passages: list[Passage], top_k: int) -> list[Reranked]:
        pairs = [(query, p.text) for p in passages]
        scores = self.model.predict(pairs)
        items = [Reranked(passage=passages[i], score=float(scores[i])) for i in range(len(passages))]
        items.sort(key=lambda x: x.score, reverse=True)
        return items[:top_k]

