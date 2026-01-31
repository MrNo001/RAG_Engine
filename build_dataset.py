from pathlib import Path

from data_prep.passages import Document, Passage, DatasetBuilder


 


def buildPassages(docsPath:Path, 
                passagesPath:Path,
                chunk_size = 800,
                chunk_overlap = 120,
                max_chunks_per_doc = 12):
        docs:list[Document] = DatasetBuilder.load_documents_jsonl(docsPath)
        passages:list[Passage] = DatasetBuilder.build_passages(docs,
                                                                chunk_size = chunk_size,
                                                                chunk_overlap = chunk_overlap,
                                                                max_chunks_per_doc = max_chunks_per_doc)
        DatasetBuilder.save_passages_jsonl(passages,passagesPath);
        print("Successfully completed passage building")


def main():
    docs_path = Path("dataset/simple_wikipedia_sample.jsonl")
    passages_path = Path("dataset/passages.jsonl")
    
    buildPassages(docs_path,passages_path)
    return;

if __name__ == "__main__":
    main()