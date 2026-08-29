# How You Pay for LLM Inference

**Source:** [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:share:7488753301665255424/)
**Published:** 2026-08-05
**Engagement:** 7,948 impressions · 229 reactions · 56 comments · 19 reposts · 3.76% engagement rate

![[assets/paying-for-llm-inference.jpg]]

---

Most LLM cost discussions revolve around token pricing and monthly subscriptions...

But there's another dimension almost nobody talks about:

How you pay for inference.

This is one reason I use Modal as the default inference option for Decode, the coding agent I'm building throughout my Building a Coding Agent From Scratch series.

Together with Gemini and OpenRouter, it covers the three tiers of the build-vs.-buy decision:

- Gemini: proprietary models
- OpenRouter: open weights as a service
- Modal: open weights you serve yourself

But ultimately, there are two infrastructure decisions to make:

## 1/ Pay per token vs. GPU time

Most hosted APIs charge per input and output token.

That's great for interactive applications.

But agents are different.

They may process thousands of documents, read entire repositories, run long debugging loops, or generate outputs in parallel.

Imagine processing 1,000 documents with 30,000 input tokens each.

That's roughly:

- 30M input tokens
- 500K output tokens

Using Claude Sonnet pricing, that's about $97.

With Modal, I can instead serve an open-source model and pay for GPU time.

At roughly 3,000 tokens/sec on an H200, the same workload takes under 3 hours.

At $4.54/hour, that's roughly $13.

It's napkin math, but it shows the tradeoff.

At high throughput, paying for compute can be dramatically cheaper than paying per token.

## 2/ Serverless vs. reserved GPUs

Once you pay for GPU time, another decision appears.

Reserve GPUs or use serverless.

Reserved GPUs are cheaper per hour, but you reserve for peak demand.

If you need 40 GPUs on Friday and 2 on Sunday, you're still paying for 40.

Serverless follows the demand curve.
It scales up while the agent works, and back to zero when it doesn't.

This is ideal for workloads that are:

- Bursty
- Parallel
- Unpredictable
- Idle between tasks

A simple rule:

If the price premium for reserved GPUs is smaller than the gap between your peak and average demand, serverless often becomes the better choice.

But there's an important caveat...

If your agent waits hours for human approval while the GPU stays alive, idle time gets expensive fast.

Ten idle hours on an H200 is roughly $45.

So don't just ask, "Which model is cheapest?"

Also consider:

- How many tokens am I processing?
- How bursty is the workload?
- How predictable is demand?
- How much idle time will I have?
- How much latency can I trade for throughput?

To sum up:

Your harness shouldn't care where inference comes from.

It should only know how to request the next completion.

Everything else belongs behind the provider layer.

This is why Decode supports Gemini, OpenRouter, and Modal through the same interface.

I break down the full architecture in Lesson 2 of my Building a Coding Agent From Scratch series.

Check it out here: https://lnkd.in/d-3NGttv
