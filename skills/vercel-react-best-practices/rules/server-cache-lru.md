---
title: Cross-Request LRU Caching
impact: HIGH
impactDescription: reuses costly reads when freshness and isolation permit
tags: server, cache, lru, cross-request
---

## Cross-Request LRU Caching

Consider a bounded cross-request cache only when repeated reads have meaningful cost and the data may be reused under an explicit freshness and isolation policy. Reuse an existing cache first. Define key identity, lifetime, size bounds, and invalidation ownership before adding an LRU dependency; ordinary sequential requests alone do not justify it.

An LRU cache can help when a bounded working set recurs and evicting entries is acceptable. Choose limits from the workload and memory budget. TTL and invalidation must match the data contract; do not copy example limits as application requirements.

Cache public data only when it has the same meaning for every caller. Include tenant, locale, version, or other relevant identity when results differ. Do not share authorization-dependent data or accept stale results when the contract requires fresh state. Choose a narrower scope or no cache when those guarantees cannot be preserved.

Use precise cache value types and distinguish a cache miss from valid falsy values. Account for failed loads and concurrent fills when they affect correctness. The write path or another identified owner must invalidate entries when the freshness contract requires it.

A process-local cache is an optimization, not durable storage or a guarantee of reuse across replicas and restarts. Verify the deployment's process lifetime and measure hit rate, latency, and memory cost. A shared cache service needs its own demonstrated requirement; do not add one automatically when local reuse is limited.

Reference: [lru-cache documentation](https://isaacs.github.io/node-lru-cache/)
