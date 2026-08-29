# Walkthrough throw the ingestion and retrieval logic

- Crawl articles and ingest your personal docs into a data warehouse (also implemented with MongoDB)
- Then further process it into a memory pipeline: clean the docs, transform them into knowledge graph objects using a graph extractor to extract entities and relationship triplets + an embedding model to embed the summary of the doc + attach other useful metadata such as the author, source URI, creation date, etc.
- Then load everything into a MongoDB database that supports everything: documents, knowledge graph hops, semantic search, text search, metadata filters, etc.
- The trick relies on properly structured your data model + ingestion/retrieval pipelines to support all these scenarios
- A super simple setup to structure your document and user ontology is to:
    - Compute a summary for each document
    - Embed the summary (to avoid chunking, which can get complicated to do it right)
    - Keep the authors for the documents to connect them to the user’s ontology
    - Keep the references to other documents as connections between the document ontology
- Then when doing queries, you can use semantic search to quickly find similar documents (or communites of documents), and ultimately traverse from these initial points to find more similar documents.
- Because we are using semantic search we can avoid having “topics” or “domain” entities as they are super hard to organize and scale well. Ultimately clusters of embeddings do that naturally.
- And you can do all of this only with MongoDB!
