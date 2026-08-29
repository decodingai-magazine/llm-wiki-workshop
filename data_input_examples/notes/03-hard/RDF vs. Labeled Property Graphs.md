# RDF vs. Labeled Property Graphs

**Comment:** RDF it’s actually easier to query as it’s composed of pure (entity, relationship, entity) triples with 0 metadata attached to them.

The cons are indeed that the size explodes, but the biggest con is that you need to know the whole data model with the attributes in advance. Thus, the upfront effort is larger. That’s why many people go with the Labeled Property graph version, which is more flexible and practical in the sense that you can start right away.

---

**Related to this post:**

Every graph is structured as a collection of (entity, relationship, entity) triplets.

But here’s the part most people overlook:

How you attach data to those triplets determines whether your system scales or collapses.

There are two main approaches:

**1/ RDF (Resource Description Framework)**

Every piece of metadata becomes its own triplet.

- Arthur → WORKS_AT → Google
- Arthur → HAS_NAME → "Arthur"
- Arthur → HAS_ROLE → "Engineer"

It's flexible… but the graph explodes in size very quickly.

**2/ Labeled Property Graphs**

You keep the triplet structure… but attach metadata directly to nodes and relationships.

Arthur {name: "Arthur", role: "Engineer"} → WORKS_AT → Google

This is:

- More compact.
- Easier to query.
- Much more practical.

And it explains why modern GraphRAG systems and agent stacks use property graphs.

But modeling the graph is only half the story...

The real challenge is extraction.

How do you map raw data into these triplets?

There are 3 extraction modes:

**Structured extraction (schema-guided)**

The LLM follows your ontology.

It extracts only the entities and relationships you defined.

→ Clean, consistent, production-ready

**Semi-structured extraction (deterministic)**

No LLM needed.

You already know the structure:

- Document → chunk relationships
- Authors
- References
- Links between data

This is how you build things like a Document Ontology.

→ Cheap, reliable, and often overlooked

**Unstructured extraction (no schema)**

The LLM invents its own entities and relationships.

It's useful for exploration but dangerous in production

Because:

- Labels drift
- Entities duplicate
- The graph becomes noise

Here's the simple rule of thumb:

- Unstructured → discovery
- Structured → production
- Semi-structured → free signal

Get this wrong…

And no amount of retrieval tuning will save you.

**P.S.** I go much deeper into this (with full system design) in my latest @Decoding AI Magazine issue:  “Building Agentic GraphRAG Systems”
