# Executive Summary: 2D Knowledge Graph Libraries

Comparison across **scale**, **how it runs**, and **beauty**.

## At-a-glance

| Library                   | Scale (max practical)              | How it runs                                     | Beauty                                  |
| ------------------------- | ---------------------------------- | ----------------------------------------------- | --------------------------------------- |
| **Sigma.js + graphology** | ★★★★☆ ~tens of thousands of nodes  | WebGL renderer + separate graph/algorithm layer | ★★★★★ Best beauty-for-effort            |
| **D3.js**                 | ★★☆☆☆ ~1–5k (SVG) / ~10k+ (Canvas) | You build rendering + force sim yourself        | ★★★★★ Highest ceiling, all manual       |
| **Cosmograph**            | ★★★★★ 100k–1M+ nodes               | GPU compute (force sim + render on GPU)         | ★★★★☆ Stunning at scale, less for small |
| **Cytoscape.js**          | ★★★★☆ ~tens of thousands           | Canvas renderer + rich graph-theory engine      | ★★★☆☆ Functional defaults, stylable     |
| **vis-network**           | ★★☆☆☆ ~1–3k comfortably            | Canvas + built-in physics                       | ★★★☆☆ Clean but generic                 |

## On scale

- **Cosmograph** wins decisively — GPU-accelerated, purpose-built for massive graphs (hundreds of thousands to millions). If your knowledge graph is huge, this is the only one that won't choke.
- **Sigma.js** and **Cytoscape.js** both comfortably handle tens of thousands. Sigma (WebGL) edges ahead on raw render performance; Cytoscape (Canvas) trades some speed for analysis depth.
- **D3.js** scales as well as _you_ engineer it — Canvas can push 10k+, SVG falls over by a few thousand.
- **vis-network** is the most limited; great for small/medium graphs, struggles past a few thousand.

## On how it runs

- **Sigma.js + graphology** — Clean separation of concerns: graphology holds the data and runs algorithms (Louvain, centrality, ForceAtlas2 layout); Sigma renders via WebGL. Layout is computed up front, then drawn. Modular, modern, well-architected.
- **D3.js** — Lowest level. `d3-force` runs an iterative tick-based simulation; you wire up rendering (SVG/Canvas) and every interaction by hand. Maximum control, maximum work.
- **Cosmograph** — Both the force simulation _and_ rendering happen on the GPU. Near-zero main-thread cost, which is why it scales. Less granular control over individual elements.
- **Cytoscape.js** — Batteries-included engine: data model, layouts, and a deep graph-theory algorithm library in one package. Canvas-rendered. The most "complete framework" feel.
- **vis-network** — Highest-level and easiest: feed it nodes/edges, physics and rendering just work. Least control, fastest to a result.

## On beauty

- **Sigma.js** — Best looking _with little effort_. Crisp WebGL nodes, zoom-aware labels, gorgeous organic clusters with ForceAtlas2 + community coloring. The pragmatic beauty winner.
- **D3.js** — Highest possible ceiling — curved gradient edges, custom glyphs, animated transitions — but every bit of that beauty is your labor. Plain by default.
- **Cosmograph** — Breathtaking "map of the universe" aesthetic _at scale_; underwhelming for small graphs.
- **Cytoscape.js** — Academic/functional defaults; can be styled well via its CSS-like stylesheets, but beauty isn't free.
- **vis-network** — Tidy and presentable, but generic — no one calls it striking.

## Bottom line

- **Best overall for a beautiful, interactive knowledge graph:** **Sigma.js + graphology + ForceAtlas2** — the sweet spot of scale, performance, and beauty.
- **Massive graphs (100k+):** **Cosmograph**.
- **Analysis-heavy applications:** **Cytoscape.js**.
- **Bespoke, art-grade visuals with time to invest:** **D3.js**.
- **Quick small graph, minimal effort:** **vis-network**.

Want this as a one-page document (Markdown, PDF, or slide) you can share?
