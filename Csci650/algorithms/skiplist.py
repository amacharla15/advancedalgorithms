"""
Skip Lists 
===============================

------------------------------------------------------------
1) What a Skip List is (in one line)
------------------------------------------------------------
A skip list is a probabilistic, layered linked-list that achieves balanced-tree–like performance
by promoting each node to higher "express lanes" with probability p, enabling fast search/insert/delete.

Core idea:
- Level 0 is a sorted linked list of all keys.
- Each higher level ℓ contains a subsequence of level ℓ−1 (each node is promoted independently with prob p).
- Search moves forward on high levels; when blocked, it drops down a level. Repeat until level 0.

------------------------------------------------------------
2) Parameters and typical choices
------------------------------------------------------------
Symbols:
- n = number of elements
- p = promotion probability (commonly 1/2 or 1/4)
- L = max level (can be ~ ⌈log_{1/p} n⌉ or a fixed cap, e.g., 32/64)
- With p = 1/2, expected height ≈ log2 n and expected #pointers per node ≈ 1/(1−p) = 2.

Rules of thumb:
- p = 1/2 → shallow (fast) with slightly more pointers.
- p = 1/4 → taller (more levels), fewer pointers per node, similar asymptotics.
- Cap L to a safe bound (e.g., 1 + ⌈log_{1/p}(n_max)⌉).

------------------------------------------------------------
3) Time & space complexity (expected)
------------------------------------------------------------
Operation        | Expected time         | Worst-case time | Space (expected)
-----------------|-----------------------|-----------------|-----------------
Search(key)      | O(log n)              | O(n)            | O(n / (1−p))
Insert(key)      | O(log n)              | O(n)            | O(1) extra per insert (amortized pointers)
Delete(key)      | O(log n)              | O(n)            | —
Range query [a,b]| O(log n + k)          | O(n)            | (k = #items in range)

Notes:
- Worst-case O(n) is astronomically unlikely with standard p and L caps.
- Expected constants are excellent and competitive with balanced BSTs.

------------------------------------------------------------
4) How search works (intuition)
------------------------------------------------------------
1) Start at top-left sentinel on highest non-empty level.
2) Move "forward" while next key ≤ target. If next key > target (or None), drop down one level.
3) Repeat until at bottom level (level 0). The current position is the predecessor of target.

This “forward-then-down” pattern mimics binary search via random sparsification.

------------------------------------------------------------
5) Insertion & deletion (high level)
------------------------------------------------------------
Insert(x):
- First, search to find predecessors at each level (maintain an update[] array).
- Flip coins to determine x’s tower height h (Pr[level ≥ ℓ] = p^ℓ).
- Splice x into the lists at levels 0..h by fixing forward pointers via update[].

Delete(x):
- Search to find predecessors at each level.
- If x exists, bypass x at each level it appears (fix forward pointers).
- Optionally shrink top levels if they become empty.

------------------------------------------------------------
6) Probabilistic analysis (key facts)
------------------------------------------------------------
- Level ℓ has ~ n · p^ℓ nodes in expectation.
- Expected height: E[height] ≈ log_{1/p} n.
- Expected search cost: O((1/p) · log_{1/p} n). For p=1/2, this is O(2 log2 n) → O(log n).
- Expected total pointers: n · (1/(1−p)) (since each node has Geometric(1−p) levels).

------------------------------------------------------------
7) Choosing p and L (practical)
------------------------------------------------------------
- p = 1/2: common; short towers, faster forward hops, slightly higher pointer overhead.
- p = 1/4: taller towers; fewer pointers per node; good cache behavior in some workloads.
- Set L = ⌈log_{1/p}(n_max)⌉ + 1 where n_max is a safe upper bound; or grow L lazily if needed.
- Use sentinels (−∞ at head; +∞ tail optional) for simpler edge handling.

------------------------------------------------------------
8) Where skip lists shine
------------------------------------------------------------
- Ordered maps/sets with simple implementation and competitive speed.
- Range queries and ordered iteration (unlike hash tables).
- Concurrent dictionaries: lock-free/lock-based variants are simpler than many tree counterparts.
- Memory allocators/indexes: predictable, pointer-based structure with O(log n) ops.

------------------------------------------------------------
9) Comparisons
------------------------------------------------------------
Against balanced BSTs (AVL/Red-Black):
- Similar expected O(log n) operations; skip lists are typically simpler to implement.
- BSTs give worst-case O(log n) deterministically; skip lists give it in expectation.
- Augmentations (order statistics) are straightforward in both, but differ in details.

Against hash tables:
- Hash: O(1) average search but no order; resizing can be costly; poor for range queries.
- Skip lists: O(log n) but maintain order and support range queries efficiently.

------------------------------------------------------------
10) Concurrency notes
------------------------------------------------------------
- Coarse-grained locks: lock predecessor nodes while splicing; simple but blocks readers/writers.
- Fine-grained locking per node/level: higher throughput; careful deadlock avoidance (lock order).
- Lock-free skip lists: widely-studied; use CAS on forward pointers, hazard pointers/epoch reclamation for memory safety.
- Validation step: after finding predecessors/successors, re-check links before commit (helpful under contention).

------------------------------------------------------------
11) Common pitfalls & implementation
------------------------------------------------------------
- Pointer fixes must be consistent across all involved levels (use an update[] path from search).
- Random level generation: geometric distribution; loop until coin tails or max L reached.
- Memory locality: array-of-struct pointers per node (forward[]) improves cache behavior.
- Sentinel levels: ensure head has L levels; avoid null checks by using tail sentinel or None carefully.
- Deletion must remove all tower levels of a node; consider GC/RC behavior in the language used.

------------------------------------------------------------
12) Useful formulas
------------------------------------------------------------
Expected nodes at level ℓ:         n_ℓ ≈ n · p^ℓ
Expected tallest level:            E[height] ≈ log_{1/p} n
Expected search steps:             O((1/p) · log_{1/p} n)
Expected pointers per node:        1/(1−p)
Pick L for capacity n_max:         L ≈ ⌈log_{1/p}(n_max)⌉ + 1

Small design table (rule of thumb):
- p = 1/2 → E[height] ≈ log2 n,    pointers/node ≈ 2
- p = 1/4 → E[height] ≈ log4 n,    pointers/node ≈ 1.33
- p = 1/e → E[height] ≈ ln n,      pointers/node ≈ 1.58


"""
