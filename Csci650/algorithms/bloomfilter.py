"""
Bloom Filters 
==================================

------------------------------------------------------------
1) What a Bloom filter is 
------------------------------------------------------------
A Bloom filter is a compact probabilistic set representation that supports fast membership queries with one-sided error:
- No false negatives (if item was added, query returns “maybe present”).
- Allows false positives (may say “maybe present” for items never added), tunable by design.

Core idea:
- Keep a bit array of length m (all zeros initially).
- Choose k independent hash functions h_1..h_k mapping items → {0..m-1}.
- To add x: set bits at positions h_1(x),...,h_k(x) to 1.
- To query x: if all those k bits are 1 ⇒ “maybe present,” else “definitely not present.”

Time/space:
- Add/query: O(k) time (typically small constant, like k∈[4,10]).
- Space: O(m) bits; extremely compact for large sets.

------------------------------------------------------------
2) Parameters and the classic false-positive formula
------------------------------------------------------------
Symbols:
- n = planned maximum number of inserted items.
- m = number of bits in the bit array.
- k = number of hash functions.
- p = false-positive probability (FPP).

Derivation sketch:
- After inserting n items, each of the m bits is set to 1 independently with probability:
    b ≈ 1 − exp(−k n / m).
- A query for an item not in the set checks k bits; all must be 1 to yield a false positive:
    p ≈ b^k = (1 − exp(−k n / m))^k.

Optimal k (for fixed m and n):
- k* = (m / n) · ln 2   (round to nearest integer in practice).

Sizing for target p:
- m ≈ −(n · ln p) / (ln 2)^2  ≈ 1.44 · n · log2(1/p).
- With k = (m/n) ln 2, one gets near-minimal p for given m and n.

Rules of thumb:
- To reach p ≈ 1%, m/n ≈ 9.6 bits per element, k ≈ 7.
- To reach p ≈ 0.1%, m/n ≈ 14.4 bits per element, k ≈ 10.

------------------------------------------------------------
3) Guarantees and limitations
------------------------------------------------------------
Guarantees:
- One-sided error: never returns “absent” for an inserted item.
- Fast operations: O(k) adds and queries; k is small constant.

Limitations:
- No deletions in the classic structure (removing would introduce false negatives).
- False positives possible; rate grows as you insert beyond the planned capacity n.
- Requires good (pairwise-independent or better) hash functions; poor hashing inflates p.

------------------------------------------------------------
4) Practical hashing & implementation notes
------------------------------------------------------------
- Double hashing (Kirsch–Mitzenmacher): simulate k hashes via
    h_i(x) = (h1(x) + i · h2(x)) mod m
  → reduces cost to two base hashes per item with negligible accuracy loss.
- Use well-distributed 64-bit digests; avoid correlated hash outputs.
- Bit array often implemented with bytearray/bitset; memory-mapped files can scale IO.

------------------------------------------------------------
5) Variants and when to use them
------------------------------------------------------------
Counting Bloom Filter (supports deletes):
- Replace each bit with a small counter (e.g., 4 bits). Insert increments; delete decrements.
- More space; beware counter overflow if heavily used.

Scalable Bloom Filter (grows as data grows):
- Chain multiple filters with increasing sizes and adjusted p’s (e.g., geometric sequence of p’s).
- Maintains overall target false-positive rate while allowing unbounded inserts.

Partitioned Bloom Filter:
- Split m into k equal slices; hash i sets 1 bit in slice i.
- Often improves cache behavior and tightens analysis of p.

Stable Bloom Filter (for streams):
- “Aging” mechanism to forget old items and bound p in sliding windows.
- Useful for long-running dedup/stream analytics where memory must remain fixed.

Cuckoo Filter (related, but different tradeoffs):
- Returns approximate membership and supports deletes without counters.
- Uses cuckoo hashing of short fingerprints; sometimes better practical performance.

------------------------------------------------------------
6) Operations beyond membership
------------------------------------------------------------
Union:
- Bitwise OR of two filters (same m and k) approximates union of sets; p increases with density.

Intersection (approximate):
- Bitwise AND can be used, but semantics are looser than union (AND may under-approximate).

Cardinality estimation:
- From fraction of zero bits z ≈ exp(−k n / m) ⇒ n̂ ≈ −(m/k) · ln z (rough heuristic; use with care).

------------------------------------------------------------
7) Choosing parameters in practice
------------------------------------------------------------
Workflow:
1) Decide acceptable false-positive rate p (e.g., 1% for cache prefilters, 0.1% for security-adjacent checks).
2) Estimate maximum n (planned capacity). Oversize slightly (headroom 10–30%).
3) Compute m ≈ −(n ln p)/(ln 2)^2 and k ≈ (m/n) ln 2; round k to integer and m to bytes/pages.
4) Verify runtime budget (k hashes per operation) and memory footprint (m bits).

Practical picks (rules of thumb):
- n = 1e6, p = 1%  ⇒ m ≈ 9.6e6 bits ≈ 1.2 MB, k ≈ 7.
- n = 1e6, p = 0.1% ⇒ m ≈ 14.4e6 bits ≈ 1.8 MB, k ≈ 10.

------------------------------------------------------------
8) Where Bloom filters shine
------------------------------------------------------------
- Web/CDN caches: prefilter membership before expensive lookups.
- Databases/storage engines: avoid probing on-disk structures when key is surely absent.
- Distributed systems: duplicate suppression, set reconciliation prefilters.
- Security/forensics pipelines: quick “seen before?” checks with low false-positive budgets.
- Stream processing: scalable dedup with stable/scalable variants.

------------------------------------------------------------
9) Common pitfalls & sanity checks
------------------------------------------------------------
- Overfilling: pushing much beyond planned n sharply increases p (bits saturate).
- Poor hashing: correlated or biased hashes inflate p; validate with empirical tests.
- Deletes in classic Bloom: not supported (use counting or cuckoo filters).
- Heterogeneous parameters: only OR/AND filters with identical (m, k, hash family) unless you know the math.

------------------------------------------------------------
10) Quick comparison table
------------------------------------------------------------
Aspect                  | Classic Bloom           | Counting Bloom         | Cuckoo Filter
------------------------|-------------------------|------------------------|---------------------------
False negatives         | Never                   | Never (if counters ok) | Never (for stored keys)
False positives         | Yes (p tunable)         | Yes (p tunable)        | Yes (tunable via FP len)
Deletes                 | No                      | Yes                    | Yes
Space per key (typical) | Very low                | Higher (counters)      | Low–moderate
Ops cost                | k probes/hashes         | k probes + counters    | 1–2 table lookups

"""