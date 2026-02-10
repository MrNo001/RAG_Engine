from dataclasses import dataclass


@dataclass(frozen=True)
class RankedId:
    item_id: int
    rank: int  


def rrf_merge(*, runs: list[list[RankedId]], rrf_k: int = 60, top_k: int = 50,) -> list[tuple[int, float]]:

    scores: dict[int, float] = {}
    for run in runs:
        for rid in run:
            scores[rid.item_id] = scores.get(rid.item_id, 0.0) + 1.0 / (rrf_k + rid.rank)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:top_k]

