from qdrant_client import QdrantClient
from qdrant_module.qdrant_module import wait_for_qdrant
from sentence_transformers import SentenceTransformer
from qdrant_client.http import models as qmodels

import numpy as np
import json

client: QdrantClient = QdrantClient(host = "localhost",port = 6333)

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)


sentences = ["This is an example sentence", "Each sentence is converted"]   

def main():
    wait_for_qdrant(client)
    #It takes time to load the sentence transformer model here
    #It is not the embeding that is costly
    print("Environment ready")
    # embeddings = model.encode(sentences)
    # print(embeddings)

    # #store the embeding into a qdrant collection
    # vectors = np.asarray(embeddings, dtype=np.float32)
    test_sentences = json.load(open("dataset/test_data.jsonl"))
    test_sentences = test_sentences["sentences"]
  
    embeddings = model.encode(test_sentences)
    vectors = np.asarray(embeddings, dtype=np.float32)
    dim = int(vectors.shape[1]) #384

    if(client.collection_exists(collection_name = "test_collection")):
        client.delete_collection(collection_name = "test_collection")
    client.create_collection(collection_name = "test_collection", vectors_config = qmodels.VectorParams(size = dim, distance = qmodels.Distance.COSINE))

    next_id = 1
    upsert_batch = 100
    for start in range(0, len(test_sentences), upsert_batch):
        end = min(len(test_sentences), start + upsert_batch)
        batch_points: list[qmodels.PointStruct] = []
        for i in range(start, end):
            pid = next_id
            next_id += 1
            payload = {"text": test_sentences[i]}
            batch_points.append(
                qmodels.PointStruct(
                    id=pid,
                    vector=vectors[i].tolist(),
                    payload=payload,
                )
            )
        client.upsert(collection_name="test_collection", points=batch_points)


    #search the collection

    query_text = "What is a cat?"
    #encode the query text
    query_vector = model.encode([query_text], normalize_embeddings=True)[0]
    query_vector = np.asarray(query_vector, dtype=np.float32).tolist()


    results = client.query_points(collection_name="test_collection", query=query_vector, limit=3 ,with_payload=True,with_vectors=True)
    for result in results.points:
        print(f"ID: {result.id}, Payload: {result.payload}, Score: {result.score}")

    


 




if __name__ == "__main__":
    main()