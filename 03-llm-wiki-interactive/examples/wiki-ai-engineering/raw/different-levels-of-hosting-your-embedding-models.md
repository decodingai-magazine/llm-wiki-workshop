# Different Levels of Hosting Your Embedding Models

1. Writing tests (unit, integration, regression): Mocked
2. For dev (running locally or on cloud dev machines which are usually lighter and don’t have access to powerful GPUs): 
    - To keep it simple: Hugging Face Transformers or Sentence Transformers
    - If you want to squeeze the most out of it: Ollama, llama.cpp
    - **Note 1:** I’ll avoid using vLLM here, even if you host it through Docker and you are using it in production as it quickly becomes a mess to port it around different dev machines. For example, it doesn’t has precompiled binaries for apple sillicon, which most devs use. Thus, it’s just easier to run the embedding model through the mentions above for a sweet dev experience.
    - **Note 2:** Here we made the assumption that your end goal is to host and run the embedding model during ingestion to process medium to big data. When building clients that only need to run the retrieval step, you can leverage llama.cpp or Ollama as well.
3. For production, when you want to scale and process small to big data. Here there are multiple levels as well:
    - Small to medium data (easiest to implement and maintain): Hook to an API that hosts your open-source embedding model
    - Medium data (medium to implement and maintain): Serve the embedding model yourself using vLLM and host it using a provider such as Modal, RunPod, [together.ai](http://together.ai), Vertex, AWS, etc.
    - Big data (medium to implement and hard to maintain): Serve the embedding model on a distributed inference cluster via Ray
    - Big data (easy to implement and maintain): Use auto-embed options that vector databases offer completely delegating the embedding computation to the vector database. With auto-embed, you just write a config on how you want your embeddings to look like on top of an existing collections and the vector database takes care of everything. This is super nice when using self managed vector databses
- When implementing this, the key to easily switch between the 3 options (tests, dev, prod) without changing any line of code is to keep your embedding model under a unified interface/abstraction (e.g., BaseEmbeddingModel) and implement yourself concrete implementations of each (e.g., MockedEmbeddingModel, SentenceTransformersEmbeddingModel, VoyageAPIEmbeddingModel, ModalEmbeddingModel, etc.). Like this through a config.yaml you can easily configure what type of model you  want to use depending on your setup. It’s super easy to implement and comes with many benefits:
    - You can easily configure your system for integration tests
    - You can easily setup your dev env
    - You can easily evaluate your best options for prod
    - …and it’s clean :)

For example, for my personal assistant example, which I am building from scratch, I am using MongoDB as my vector database and Voyage AI as my embedding models. Here is my current setup using fully open-source models from Hugging Face with 0 vendor lock-in: 

- Tests: Mocked
- Dev: Sentence Transformers (I tried vLLM first to unify running it with prod, but it quickly became a mess running it on my macbook)
- Prod: Serving via vLLM and hosting via Modal (super neat combo to get up and running at scale in hours)

Also, if necessary, I can easily switch to using Voyage AI’s API as a fall back plan.

Why I chose Voyage AI? Because:

- It natively integrates with MongoDB, thus it’s a natural choice
- they have some awesome embedding models that make your life so much easier such as the **Contextualized Chunk Embeddings** which solves all your chunking problems as contexual RAG is one of the best chunking methods out there relative to the cost/latency/performance trade-off + their **voyage-multimodal-3.5 multimodal** embedding model which can embed your whole stack of multimodal messages as they are regardless if they are text or images, which is extremely powerful when building RAG agents as it keeps the natural topology of the conversation
- Also, with this combo I have everything for my setup:
    - Hugging Face open-source models for dev and to host them myself via vLLM
    - Self-hosted models via their Voyage API (both embedding and reranking models)
    - Auto-embed possibility when I want to go big data
