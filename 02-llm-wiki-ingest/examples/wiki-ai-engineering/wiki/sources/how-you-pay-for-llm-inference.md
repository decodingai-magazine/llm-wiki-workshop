---
type: source
title: How You Pay for LLM Inference
description: The overlooked cost dimension — per-token versus GPU-hour, and serverless versus reserved — worked through with napkin math on a 1,000-document job.
origin: local
original_path: data_input_examples/notes/03-hard/How You Pay for LLM Inference.md
source_url: null
authors: []
published_date: null
raw_file: raw/how-you-pay-for-llm-inference.md
created: 2026-08-29T10:00:00Z
timestamp: 2026-08-29T10:00:00Z
entities:
  - "[[wiki/entities/modal]]"
concepts:
  - "[[wiki/concepts/inference-economics]]"
  - "[[wiki/concepts/provider-abstraction]]"
  - "[[wiki/concepts/agent-harness]]"
---

# How You Pay for LLM Inference

> [[raw/how-you-pay-for-llm-inference|Raw]] · local

## Summary

Cost conversations stop at token prices and subscriptions; this note argues the
interesting variable is the *payment model*. Two decisions follow.

**Per-token versus GPU-time.** Hosted APIs bill per token, which suits interactive
work. Agents are not interactive in that sense — they read whole repositories,
process thousands of documents, run long loops. The worked example: 1,000
documents at 30,000 input tokens each is ~30M input and ~500K output tokens,
roughly $97 at Claude Sonnet pricing; serving an open model at ~3,000 tokens/sec
on an H200 finishes in under three hours at $4.54/hour — about $13. Napkin math,
explicitly labelled as such, but a 7x gap survives a lot of imprecision.

**Serverless versus reserved GPUs.** Reserved is cheaper per hour but you reserve
for peak: 40 GPUs on Friday and 2 on Sunday still costs 40. Serverless follows the
demand curve and scales to zero, which fits bursty, parallel, unpredictable work.
The rule offered: if the reserved-GPU premium is smaller than the gap between peak
and average demand, serverless wins. The caveat is sharp — an agent waiting hours
for human approval with a live GPU costs ~$45 for ten idle H200 hours.

The closing line is architectural rather than financial: the harness should not
know where inference comes from. It requests the next completion; everything else
sits behind a provider layer.

## Key claims

- Payment model is a distinct axis from model choice, and it changes cost by multiples, not percentages. [[raw/how-you-pay-for-llm-inference#1/ Pay per token vs. GPU time|cite]]
- ~$97 per-token versus ~$13 on GPU-time for the same 1,000-document workload. [[raw/how-you-pay-for-llm-inference#1/ Pay per token vs. GPU time|cite]]
- Reserved GPUs mean paying for peak demand continuously; serverless follows the curve to zero. [[raw/how-you-pay-for-llm-inference#2/ Serverless vs. reserved GPUs|cite]]
- Idle time is the hidden cost of agent workloads that wait on humans — ten idle H200 hours is ~$45. [[raw/how-you-pay-for-llm-inference#2/ Serverless vs. reserved GPUs|cite]]
- "Your harness shouldn't care where inference comes from. It should only know how to request the next completion." [[raw/how-you-pay-for-llm-inference|cite]]

## Connections

- **Entities**: [[wiki/entities/modal]]
- **Concepts**: [[wiki/concepts/inference-economics]], [[wiki/concepts/provider-abstraction]], [[wiki/concepts/agent-harness]]

> Synthesis: The only note in the wiki that puts a number on an architectural choice, and its last line quietly makes the case for the provider abstraction the embedding-hosting note argues separately.
