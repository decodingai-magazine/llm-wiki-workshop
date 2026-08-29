# MongoDB Notes on Scaling (from the meeting)

# Questions

After looking at the video you sent me relative to scaling and making MongoDB more resilient, it made me curious to get more details about my scenario, where I want to build a unified memory for agents using GraphRAG and how far I can scale it using MongoDB. For more context, I am not using the LangChain GraphRAG implementation, but building something from scratch. I am building an immutable log collection where I push all the extracted entities and relationships from my graph and a materialized view, where I aggregate the logs into the actual queryable knowledge graph. Hence, here are my questions:

1. How big can my immutable logs collection get (in orders of magnitude of records)? I expect this to grow at the order of millions of documents if not more, thus I am curious to get some numbers relative to how large the collection can get, how many reads it supports, with how many shards and at what cost/latency.
2. As I materialize the immutable logs into the knowledge graph collection, I am currently using the `$merge` operator to do the sync between the two collections. As before, I am curious how:
    1. How far can I go with this method in terms of the number of records before I have cost / latency issues?
    2. What is the latency expected between syncing the immutable logs and graph collections through the `$merge` operator?
    3. As this collection will be hit with writes by the end, I am curious about some numbers around how many shards I need per how many writes.
3. I am curious if I took the correct approach to materialize the immutable logs into the queryable KG collection through the `$merge` operator. Are there any better ways to do this?

# Notes

- No reason to flag anything in MongoDB as “immutable”. The immutability should be handled on the application side, not the database size.
- Deploy on Atlas
    - Automatically configures a replica set with a minimum of 3 replica sets (for high availability)
        - always writing to primary
        - Common config:
            - multi-cloud (AWS, Azure, GCP)
            - multiple availability zones (e.g., 2 in AWS)
            - each replica will be in different availablity zones or multi-clouds
- Scaling:
    - Sharding for infine scale
        - Benefits: infinite scale
        - Cons: The cluster is more complicated (e.g., in vector space the indexes become too large)
        - E.g., Shard the cluster in 2 TB of data
        - Each shard will have their replicas (2 shards → 6 nodes)
    - MongoS (s for shards): it’s a router you connect to
- Lucine (the vector search index - aka mongot) is capped at:
    - ~2B items per shard (due to the integer cap) → every shard will have some of the data
    - Machine size (e.g., if the machine has 4 GB memory)
    - scaling: vertical (upgrading the machine) + horizontal (sharding)
    - usually scaling vertically exponentially increases the cost while scaling horizontally scales costs linearly
- Mongod + mongot compete for memory
    - inverted indexes can be the same size of your data or larger (e.g., 10 GB of data, 10 GB of mongot and 10GB of RAM → mongod slower)
    - inverted indexes can be larger than your data because they index every word in the documents rather than B-Tree that index only a few words
- Logging as we rarely read on it will mostly stay on disk not in RAM
    - from a disk point of view this is fine
    - from a RAM point of view this is an issue
    - to avoid pulling stuff from the immutable log collection into memory if we don’t specify into the $merge operation a date or do it only on the new data to scope down the data that is in memory.
    - in Atlas we can have a dedicated search node (mongot) not competiting anymore on RAM with the mongod node
- Options to create the materialize view:
    - craft the $merge operation to use it only on ops from the last 20 seconds
    - if we have to run it on data from a month ago then this causes problem on the RAM availability
    - if we sync rarely having two collections is totally fine. It becomes a problem when we need to pull a lot of data from both where both have to exist in RAM
    - Having a single copy is “good practice” as it’s easier
    - It all has to do with RAM
    - If we are using the $materialized view, we have the following issues:
        - when do I run it?
        - have to be super careful to run aggregations and filters not to load the old data in RAM
    - ops:
        - insert
        - update
        - upsert (insert + update)
    - graphLookUp:
        - as it’s recursive the index is already in memory → making it super fast
        - The $match - $in operator for the node entry points can start being slow when having the order of magnitude of thousands of IDs, but when <100-1000 should be fine
