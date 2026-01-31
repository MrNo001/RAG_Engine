from pathlib import Path

from data_prep.passages import Document, Passage, DatasetBuilder


def getPassages(docsPath:Path, passagesPath:Path) -> list[Passage]:

    if(passagesPath.exists()):
        return DatasetBuilder.load_passages_jsonl(passagesPath)
    else:
        docs:list[Document] = DatasetBuilder.load_documents_jsonl(docsPath)
        passages:list[Passage] = DatasetBuilder.build_passages(docs,chunk_size = 200,chunk_overlap = 20,)

def main():
    docs_path = Path("dataset/simple_wikipedia_sample.jsonl")
    passages_path = Path("dataset/passages.jsonl")

    

if __name__ == "__main__":
    main()