# Scaling MongoDB Brain Dump

# Summary

Brain dump on scaling MongoDB databases, with a focus on building memories for agents via knowledge graphs. Based on a conversation with **Justin LaBreck,** Staff Developer Advocate ****from MongoDB, covering horizontal vs vertical scaling, sharding, replicas, RAM bottlenecks, and vector index overhead.

---

# Scaling MongoDB Brain Dump

I want to create a brain dump on scaling your database — general techniques — and then scope it on building memories for agents via knowledge graphs.

After my conversation with Justin from MongoDB, he basically walked me through the basics of what you need to scale your MongoDB database, or in general, to scale your database cluster.

## Vertical and Horizontal Scaling

There are two core ways of scaling your database, as with any other compute resources. There is vertical scaling, where you have your machine and you increase RAM, disk, CPU, GPU, and things like that. Usually in the context of databases, you need to increase the RAM, which is the most important one. And then you have horizontal scaling, which is done through sharding and partitioning your data. In theory, horizontal scaling can allow you infinite scale. You can always partition your data more granularly and introduce a new node in the cluster to scale it up. But the core issue with horizontal scaling is that the cluster gets more complicated, because there are more nodes in your cluster, in your network. The probability of getting a node in the right place gets lower, and things like that.

For example, Justin told me that a good standard practice is that usually one shard from the cluster can process about two terabytes of data. Also, usually one shard under the hood actually includes three nodes. This is a standard practice — not necessarily always the case — but the idea is that one shard usually has more replicas.

## Replicas and High Availability

So let me start from the beginning. You spin up your fresh MongoDB database, and instead of having just one replica, you usually have three replicas, where one is used for writes and two are used for reads. For high availability, you usually also want to go with a multi-cloud configuration — have one replica in AWS, another one in Azure, and another one in GCP. What's even more important is to have multiple availability zones, depending on where your clients are. Each replica can sit in different clouds and/or different availability zones. For example, one in a data center in Ireland, one in a data center on the east coast of the US, and one somewhere in Asia. The idea is that the data is closer to the user.

So this is basically one snapshot of your data within three replicas or more. Three is just a good standard practice, but you can introduce more replicas, like more read replicas per data snapshot.

## Sharding

And then you introduce sharding. You partition your data. Usually one partition can hold up to two terabytes of data. You shard it across multiple shards, where each shard has three replicas or more. You can see how the number of nodes can quickly explode. If you have only one shard, you have three nodes. If you have two shards, you have six nodes. Three shards means nine nodes at the minimum, and so on and so forth.

So these are the basic ideas behind scaling your database.

## RAM as the Biggest Bottleneck

Now, let's talk more about memory, because usually memory in the context of databases is the biggest bottleneck. Why? Because RAM is the most expensive resource. Disk, on the other hand, is cheaper. You can very easily scale disk because it's cost-effective, but RAM is costly. So all your designs should prioritize the design around RAM because it's the most scarce resource.

Again, based on my discussion with Justin, usually a shard can process up to two billion items of around two terabytes of data without starting to have issues, such as the maximum integer cap that can be processed on 32 or 64 bits. I have to double-check this, but the idea is that there's a physical constraint where on one shard, you can process up to two terabytes of data.

## RAM Lifecycle: Index vs Data

Now back to RAM. As I said, assume that on one shard, we have two terabytes of data, up to two billion items. The issue is that for each collection within your data, you need to bring the following items into memory. You have your actual data — your actual collections or tables — and then you have your indexes. Your indexes help you query your data. There's a lifecycle between RAM and disk where, if your data is not accessed frequently, it gets moved to disk. But when your data starts to get queried, it gets moved into RAM in a cache. So in RAM, you'll have the index plus the data itself.

If the data is not being queried, you have only the index in RAM. But when some part of the data starts getting queried, you bring the data from disk into RAM to cache it. So you end up with two representations of your data in RAM: the index and the slice of the data itself that's being queried. That's why it's super important how you query your data — if you query more data than you need, more data than necessary gets cached, your RAM starts hitting a bottleneck faster, which then propagates into query latency, query performance, and things like that.

## Vector Indexes and RAM Overhead

This gets even trickier when you introduce vector indexes. For normal B-tree indexes that query standard fields within your collection — like indexing your ID and some other fields you want to filter and search — B-tree indexes are pretty efficient RAM-wise. But when you introduce vector indexes, you introduce inverted indexes, which basically index each word from your collection. This translates to the size of the index being equal to or bigger than the size of your data. So if you have 10 gigs of data, you have 10 gigs or more of index. Your RAM needs to be somewhere between 10 gigs and 20 gigs only for one collection.

## Implications for Knowledge Graph Design

That's where I want to go back to my knowledge graph design. If, for example, you have the append-only plus materialization design, which basically creates two snapshots of your data, and you already have just 10 gigs of data — with vector indexes, that means you have 10 gigs of data itself plus the duplicate, so 20 gigs, plus the indexes. It's already 40 gigs of RAM. I don't know if you want to pay for a 40 gigs of RAM machine. And then just for 10 gigs, you'd need to introduce sharding, and you over-complicate your whole infrastructure.

Now, for the append-only log, you don't need a vector index. You do the vector index on the materialized knowledge graph. But still, you're down to 30 gigs of RAM. You can do really smart filtering on the append-only log and avoid bringing the data into RAM. You can also keep the index very light. You can think about it this way: the append-only log will mostly stay on disk most of the time, and you basically get just the materialized view's index in RAM plus the data you actively query. You can reduce your whole structure to around 10 gigs of RAM if you're smart about it.

The thing is you need to be really careful about how you manage your append-only log — specifically what you query, and hence what you bring into RAM. If you have some bugs, or especially if you let LLMs write dynamic queries against your data, it's very easy for this to go off the rails and the performance of the database to drop.

So the biggest issue in reality is not necessarily the size of your data per se, but the size of data that you bring into RAM. Because for append-only logs, you rarely read the data. Probabilistically speaking, the data will mostly stay on disk, and you don't need fancy indexes on top of it. So it shouldn't be a bottleneck on RAM. But when it starts being a problem, the two collections will start competing for the same RAM on the same machine, and then you can get into trouble. To fix that, your infrastructure code just gets really complicated really fast.

## MongoDB Processes: mongod vs mongot

In the MongoDB setup, you have the `mongod` process, which is the normal database, and the `mongot` process, which handles the vector index. These two processes usually sit on the same machine and compete for the same RAM. If you want to fix this, you have to over-complicate your setup and move those indexes to different nodes. Then your number of nodes per shard doubles. Instead of having three nodes per shard, you have six nodes per shard. For two shards, you have 12 nodes. Your infrastructure explodes.

This is why you need to be really careful about the snapshots of your data when you work with data products in AI. Even at small scale, 10 gigs can be an issue. Even if good practices tell you to create many snapshots of transformations — raw data, transformed data, feature data for whatever models — you can see how this can quickly become an operational nightmare.

## Original Questions and Answers

Now back to my original questions. To conclude this conversation, I initially asked MongoDB: how big can my immutable logs collection get, in orders of magnitude of records? It can get really large — up to 2 billion items per shard. But the issue is not the size of the collection if it sits on disk, but how much of it you bring into RAM, competing against the materialized knowledge graph collection that you actually query. That's the actual issue: how you query those immutable logs. Otherwise, you can hold up to 2 billion items.

The second question: as I materialize the immutable logs into the knowledge graph collection, I'm currently using the merge operator to sync between data collections. The merge operator itself is fine, but you need to be really careful to merge just what changed and be super surgical about what you aggregate on each update, and how frequently you aggregate on each update. Because all these operations require bringing data into RAM, which adds overhead on your database cluster.

How far can I go with this method in terms of number of records before I have cost and latency issues? You can go up to 2 billion records per shard, and if you shard more, you can achieve infinite scale. But the issue, as I said, is how you actually query it.

What is the latency expected between syncing the immutable logs and graph collections through the merge operator? This is more of a design choice on how frequently you actually want to run that operation. If you run it super frequently, you put more pressure on the RAM. If you run it more rarely — say every 24 hours — you put less pressure on the RAM, but then your knowledge graph won't be that fresh. So it's a design choice based on how much RAM you actually have available.

The third question is about how many shards I need for a given number of writes. I think this is hard to answer without running stress tests, but the idea is that you can experiment with different shard configurations and see how they perform.

That's it. The brain dump is done.

# References

-
