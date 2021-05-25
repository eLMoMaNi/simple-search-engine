from indexer import Indexer
from retriever import Retriever

#indexer = Indexer('./cranfield_data.json')
#indexer.create_schema_file("schema.json")
retriever =Retriever("schema.json")
docs, =retriever.query("improved by introducing the empirical shock")
print(docs)