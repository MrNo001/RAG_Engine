

Qdrant - used for storing data alongside a embeded vector representation,
we run the service using a docker image 


[all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) - sentence-transfomer model ,maps an input to a 384 dim vector. Used for encoding semantic meaning.


QdrantClient - Qdrant uses REST Api for communicating with service,instead of setting up requests ourself we use QdrantClient
               We upsert the points in batches not to overload the Qdrant service,may have limited request body etc.
               If we swithc to gRPC which has a limit of 4mb per request it will still work


BM25_Index - We use this data_object to store data about token frequency in passages.
             Contains fields: passages-original data unchanged,doc_len - list of all document lenghts,avgdl - average doc len
             corpus_size - number of passages processed,doc_freq - dictionary of each token in doc and its frequency
             idf - inverse document frequency, dictionary of all tokens in all of documents with their idf numbers

            Pickle dump works by going through object structure three and recursivly saving all fields

Corpus - The entire searchable universe,corpus_tokens is all of the text in the data returned as tokens