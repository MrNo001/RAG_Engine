

Qdrant - used for storing data alongside a embeded vector representation,
we run the service using a docker image 


[all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) - sentence-transfomer model ,maps an input to a 384 dim vector. Used for encoding semantic meaning.


QdrantClient - Qdrant uses REST Api for communicating with service,instead of setting up requests ourself we use QdrantClient
               We upsert the points in batches not to overload the Qdrant service,may have limited request body etc.
               If we swithc to gRPC which has a limit of 4mb per request it will still work

