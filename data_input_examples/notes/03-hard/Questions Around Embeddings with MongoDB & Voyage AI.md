# Questions Around Embeddings with MongoDB & Voyage AI

**Questions 1:**

1. How do you recommend computing the embeddings? Within our code via the API/Hugging Face? Or directly within Atlas?
2. To make it as easy as possible to run the book's code without setting up any external services and make it free of charge, I want to first support running the open-source models via Hugging Face. Then, offer the possibility to switch to the Voyager API if necessary. Thus, I want to better understand the difference between the models available on Hugging Face and the ones available on the Voyage API.
3. What is the recommended way to host and run the Hugging Face open-source models for a production setup? Through Transformers, Sentence Transformers or directly through vLLM?

**Answers 2:**

- **voyage-nano (only open-weights model available on Hugging Face)**: Our smallest model, recommended for local development and testing. For production, we recommend using the larger models available via the Atlas Embedding and Reranking API or the Voyage API. For HF models, I've typically used them via Sentence Transformers.
- **Atlas Embedding and Reranking API**: One of the ways we've integrated Voyage models into the MongoDB ecosystem. API keys for this API can be obtained from the Atlas UI. This is meant for those who already have an Atlas account, existing customers, or new users who want to try out both MongoDB + Voyage AI.
- **Voyage AI API**: All of Voyage's models are available through this API as well. Great for folks who want to explore Voyage models independently, with an eye towards using them in production.
- **Auto-embedding**: Currently in public preview in MongoDB community edition, coming to Atlas soon. As the name suggests, it automatically adds embeddings to data in an Atlas collection. We've seen a lot of our enterprise customers ask for this capability, so seems like this is an attractive feature for production workloads.

Some resources:

- [https://www.mongodb.com/docs/api/doc/atlas-embedding-and-reranking-api/](https://www.mongodb.com/docs/api/doc/atlas-embedding-and-reranking-api/)
- [https://www.mongodb.com/company/blog/product-release-announcements/unlocking-ai-search-introducing-automated-embedding-in-mongodb-vector-search](https://www.mongodb.com/company/blog/product-release-announcements/unlocking-ai-search-introducing-automated-embedding-in-mongodb-vector-search)

---

**Questions 2:**

As the book is more community-based and not enterprise, for ease of use, do you recommend using the API or the auto-embedding option? As I will host the community version of MongoDB through Docker, I am interested in how portable the auto-embedding feature is across macos/linux/windows + x86/arm/gpus, etc. ?

I was thinking of using the Hugging Face option for dev, the api for prod, and just mentioning the auto-embedding option for enterprise and big data use cases, but I'm curious to hear your take on this.

**Answers 2:**

API would be the easiest overall. And agree with your thinking on just mentioning auto embedding for enterprise use cases.

The auto-embedding feature should work well with all the OSes, but it needs a fair bit of configuration to get things going while the feature is in public preview. I'd rather just mention it when it hits Atlas cloud, since that's what most enterprises will end up using anyway. I'll keep you posted when it's available on cloud!

---

**Questions 3:**

how many free credits do people get with the Voyage API? Either run through MongoDB Atlas or directly through Voyage.

**Answers 3:**

200 million free tokens!
