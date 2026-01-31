from qdrant_client import QdrantClient
from qdrant_module.qdrant_module import wait_for_qdrant
from sentence_transformers import SentenceTransformer



client: QdrantClient = QdrantClient(host = "localhost",port = 6333)

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)


sentences = ["This is an example sentence", "Each sentence is converted"]

def main():
    wait_for_qdrant(client)
    #It takes time to load the sentence transformer model here
    #It is not the embeding that is costly
    print("Environment ready")
    embeddings = model.encode(sentences)
    print(embeddings)

    















if __name__ == "__main__":
    main()