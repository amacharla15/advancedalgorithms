"""
Greedy Algorithms: 



Greedy = make the locally best choice at each step and never backtrack. It works when the
“greedy-choice property” holds, usually proven by an exchange or stay-ahead argument
(or by invoking a matroid/structure property). If you can’t justify it, prefer DP or search.

What is a Greedy Algorithm?

Definition:

An algorithm that builds a solution step-by-step by always picking the locally optimal choice
according to a simple key (e.g., smallest edge, earliest finish time, highest value/weight).

Key ingredients:

Greedy-choice property: There exists an optimal solution that begins with the greedy choice.

Optimal substructure: After making a choice, the remaining subproblem has the same form.

Proof templates:

Exchange argument: Take any optimal solution; swap its first decision with the greedy decision, show
the solution’s value doesn’t worsen; iterate swaps to transform into the greedy solution.

Stay-ahead argument: After each step i, the greedy partial solution is at least as “good”
(earlier finish / smaller cost / larger coverage) as any other partial solution’s first i steps.

Where greedy shines (classic “wins”):

Interval scheduling by earliest finish time (maximize number of compatible intervals).

Minimum Spanning Tree: Kruskal and Prim (cut property).

Shortest paths with nonnegative weights: Dijkstra.

Huffman coding (merge two lightest trees).

Fractional knapsack (pick by value/weight ratio).

Canonical coin systems (e.g., US coins) for coin change.

Where greedy tends to fail:

0/1 knapsack (ratio-greedy is not optimal).

Set cover (greedy is a log-approximation, not optimal).

Arbitrary coin systems (e.g., {1,3,4} breaks greedy for amount 6).

Problems with strong global coupling or backward constraints.

Quick Diagnosis Checklist: “Is this problem greedy?”

Can I state a simple key for “best next choice” (earliest finish, smallest weight, highest ratio)?

Can I break that rule on a tiny adversarial example? (If yes → not greedy.)

Can I prove an exchange or stay-ahead argument?

Is there a known structure (matroid, cut property) that makes the key safe?
If 2) fails and 3)/4) succeed → greedy is likely correct. Otherwise prefer DP/search.

Minimum Spanning Trees (MSTs)

Problem:

Given a connected, undirected, weighted graph G=(V,E,w), find a spanning tree T with |V|−1 edges
minimizing total weight sum(w(e) for e in T). MST may not be unique if there are equal weights,
but all MSTs share the same total weight.

Foundational properties:

Cut property (safe-edge rule): For any cut (S, V−S), the lightest edge crossing the cut is “safe” —
it belongs to some MST.

Cycle property: In any cycle, the heaviest edge does not belong to some MST.

These two justify greedy choices in Kruskal/Prim.

Kruskal’s Algorithm (Edge-centric Greedy for MST)

Idea:

Sort all edges by nondecreasing weight. Scan in order; add an edge if it connects two different components
(no cycle). Use Disjoint Set Union (DSU/Union–Find) with path compression + union by rank/size.

Steps:

Sort edges by weight ascending.

Initialize forest T = ∅ (each vertex in its own component).

For each edge (u,v) in sorted order:

If find(u) != find(v), add edge to T and union(u,v).

Stop when T has |V|−1 edges (or when edges exhausted, producing a spanning forest).

Correctness:

Each accepted edge is the lightest across some cut (the components define the cut).

By the cut property, it’s safe.

Complexity:

Sorting: O(E log E) = O(E log V).

DSU ops: ~O(E α(V)) ≈ linear in practice.

When to use:

Sparse graphs or when edges are easy to sort once.

You naturally think in “merge components” mode.

Prim’s Algorithm (Vertex-centric Greedy for MST)

Idea:

Grow a single tree. Start from any vertex s; repeatedly add the minimum-weight edge leaving the tree
to a new vertex.

Steps:

S = {s}; for all v, track best edge weight to connect v to S (a key).

Repeatedly pick vertex v ∉ S with minimum key; add its connecting edge; update keys of its neighbors.

Data structures and complexity:

Binary heap + adjacency lists: O(E log V).

Fibonacci heap (theoretical): O(E + V log V).

Dense graphs with array (no heap): O(V^2).

Correctness:

At each step, choose the lightest edge crossing the cut (S, V−S). By the cut property, it’s safe.

When to use:

Dense graphs or adjacency-matrix style; you want a “frontier expansion” perspective.

Kruskal vs Prim — Quick Contrast

Strategy: Kruskal = pick cheapest edge anywhere that doesn’t form a cycle (component merging).
Prim = expand the current tree by the cheapest outgoing edge (frontier).

DS: Kruskal = DSU + edge sort; Prim = priority queue of cut edges.

Best for: Kruskal = sparse graphs; Prim = dense graphs or when growing from a seed is natural.

Both: O(E log V) with standard heaps/sorts; both rely on the cut property.

Jump Game Family (Greedy and Non-Greedy)

Jump Game I — “Can I reach the end?”:

Input: array a[0..n−1] with nonnegative ints. Start at index 0. From i, you can jump to any j in [i+1, i+a[i]],
staying in bounds. Question: can you reach index n−1?

Greedy invariant (furthest reach):

Track reach = furthest index reachable so far.

Scan i from 0..n−1:

If i > reach → unreachable → return False.

reach = max(reach, i + a[i]).

If reach ≥ n−1 → return True.

Why correct (stay-ahead):

Among all strategies that reach i, the one with largest “furthest reach” after i is never worse.

If greedy cannot reach i, no strategy can (otherwise reach would have been ≥ i).

Complexity: O(n) time, O(1) space.

Examples:

[2,3,1,1,4] → True (reach hits 4 at i=1).

[3,2,1,0,4] → False (reach stalls at 3, can’t step on 4).

Jump Game II — “Minimum number of jumps” (assume reachable):

Greedy by levels/windows (BFS over ranges):

Maintain current window [curL, curR] of indices reachable with k jumps.

Compute nextR = max(i + a[i]) for i in [curL..curR], then increment jumps and set window to [curR+1, nextR].

Stop when curR ≥ n−1. Complexity: O(n), O(1).

Jump Game III — “Reach a zero” (can move ±a[i]):

Use BFS/DFS with a visited set; not a greedy frontier problem. Complexity: O(n).

Canonical Coin Change vs Greedy (Caution)

Greedy “take the largest coin ≤ remaining” is not always optimal for arbitrary denominations.

Works for canonical systems (e.g., US coins {1,5,10,25,100}, powers of a base {1,b,b^2,...}).

Counterexample: coins {1,3,4}, amount 6.

Greedy: 4 + 1 + 1 = 3 coins; optimal: 3 + 3 = 2 coins.

If optimality is required for arbitrary sets, use DP (O(n·amount)).

Proof Patterns to Quote

Cut property (MSTs): Lightest edge across any cut is safe → justifies both Kruskal and Prim.

Cycle property (MSTs): Heaviest edge in a cycle can be removed without losing feasibility.

Exchange argument (interval scheduling / MST): Swap non-greedy choices for greedy ones to show no loss.

Stay-ahead (Jump Game I / Fractional knapsack): After each step i, greedy’s state dominates any other’s.

Common Pitfalls & Edge Cases

MST vs Shortest-Path Tree: different objectives; MST can distort shortest paths.

Dijkstra requires nonnegative weights; Bellman-Ford handles negatives.

Jump Game I: zeros only block if you must land on them and your reach doesn’t already exceed them.

Kruskal on disconnected graphs yields a minimum spanning forest (one MST per component).

Ties in MST edges → multiple correct MSTs (same total weight).

Mini Worked Examples (Concise)

MST example:

Graph edges: A–B:1, B–C:2, C–D:3, A–C:4, B–D:5.

Kruskal: pick 1 (A–B), 2 (B–C), 3 (C–D) → 3 edges for 4 nodes → total 6.

Prim from A: add A–B(1), then B–C(2), then C–D(3) → total 6.

Jump Game I:

[2,3,1,1,4]: reach evolves 0→2→4→4→4 → True.

[3,2,1,0,4]: reach evolves 0→3→3→3→3, but index 4 > reach → False.
"""