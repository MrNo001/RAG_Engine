import json
from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen = True)
class Document:
    doc_id: str
    title: str
    text: str
    url: str

@dataclass(frozen = True)
class Passage:
    passage_id: int
    doc_id: str
    title: str
    url: str
    chunk_index: int
    text: str



def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    if chunk_size <= 0:
        return [text]
    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 4)

    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        start = max(0, end - overlap)
    return chunks
    

class DatasetBuilder:

    def load_documents_jsonl(path: Path) -> list[Document]:
        docs_list = []
        with open(path, "r") as doc_file:
            for line in doc_file:
                doc = json.loads(line)
                docs_list.append(Document(doc_id=doc["doc_id"],
                                        title=doc["title"],
                                        text=doc["text"],
                                        url=doc["url"]))
            return docs_list

    def build_passages(docs: list[Document],
    *,
    chunk_size: int,
    chunk_overlap: int,
    max_chunks_per_doc: int
    ) -> list[Passage]:
        passages: list[Passage] = []
        id_counter = 1
        for d in docs:
            chunks = chunk_text(d.text, chunk_size=chunk_size, overlap=chunk_overlap)[:max_chunks_per_doc]
            for j, ch in enumerate(chunks):
                passages.append(
                    Passage(
                        passage_id=id_counter,
                        doc_id=d.doc_id,
                        title=d.title,
                        url=d.url,
                        chunk_index=j,
                        text=ch,
                    )
                )
                id_counter += 1
        return passages

    def save_passages_jsonl(passages: list[Passage], out_path: Path) -> None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            for p in passages:
                f.write(
                    json.dumps(
                        {
                            "passage_id": p.passage_id,
                            "doc_id": p.doc_id,
                            "title": p.title,
                            "url": p.url,
                            "chunk_index": p.chunk_index,
                            "text": p.text,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )


    @staticmethod
    def load_passages_jsonl(path: Path, limit: int | None = None) -> list[Passage]:
        passages: list[Passage] = []
        with path.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if limit is not None and i >= limit:
                    break
                row = json.loads(line)
                passages.append(
                            Passage(
                                passage_id=int(row["passage_id"]),
                                doc_id=row["doc_id"],
                                title=row.get("title") or "",
                                url=row.get("url") or "",
                                chunk_index=int(row.get("chunk_index") or 0),
                                text=row["text"],
                            )
                )
        return passages