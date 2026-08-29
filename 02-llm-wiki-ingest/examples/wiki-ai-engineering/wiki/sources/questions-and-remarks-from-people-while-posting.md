---
type: source
title: Questions And Remarks From People While Posting
description: Reader questions collected from posts — memory decay, wrong extractions, freshness at scale, ontology construction — plus one practitioner's GraphRAG success report.
origin: local
original_path: data_input_examples/notes/03-hard/Questions And Remarks From People While Posting.md
source_url: null
authors: []
published_date: null
raw_file: raw/questions-and-remarks-from-people-while-posting.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities: []
concepts:
  - "[[wiki/concepts/knowledge-freshness]]"
  - "[[wiki/concepts/knowledge-graph]]"
  - "[[wiki/concepts/agent-memory]]"
---

# Questions And Remarks From People While Posting

> [[raw/questions-and-remarks-from-people-while-posting|Raw]] · local

## Summary

A collected list of what readers actually asked, which makes it the wiki's best
inventory of unanswered problems. Three of the questions are the same question
from different angles: how do you handle memory decay and outdated information,
how do you handle *incorrect* information (whether from a bad source or a bad
extraction), and how do you keep the knowledge base fresh as inputs grow. Two more
ask for construction detail — how the document and user ontology is built, and
whether there is a practical how-to for a unified memory on MongoDB or PostgreSQL.

One remark is a report rather than a question: a practitioner who built an
institutional knowledge engine on GraphRAG, with nodes for documents, authors,
topics and priorities, and found the node structure to be what keeps up with
constantly changing business context.

## Key claims

- The most common reader question is about freshness and decay, not about retrieval quality. [[raw/questions-and-remarks-from-people-while-posting|cite]]
- Wrong information has two distinct sources — a bad ingested document, and a bad extraction from a correct one — and readers ask about both. [[raw/questions-and-remarks-from-people-while-posting|cite]]
- An independent practitioner reports GraphRAG's node structure as the thing that keeps up with changing business context. [[raw/questions-and-remarks-from-people-while-posting|cite]]

## Connections

- **Entities**: none
- **Concepts**: [[wiki/concepts/knowledge-freshness]], [[wiki/concepts/knowledge-graph]], [[wiki/concepts/agent-memory]]

> Synthesis: Every question here is about the *write* path staying honest over time, and the wiki answers almost none of them — that gap is the most useful thing this page records.
