"""
a graph G = (V, E) is a flow network if each edge (u, v) ∈ E has a non-negative capacity c(u, v) ≥ 0.
and there is a source vertex s ∈ V and a sink vertex t ∈ V, s ≠ t.

s is called the source, and t is called the sink.
capacity is the maximum amount of flow that can pass through an edge.
flow is a term that shows what actually the edge carry

The flow must satisfy the following conditions:

Capacity Constraint: For every edge (u, v) ∈ E, the flow f(u, v) must not exceed the capacity c(u, v).

Skew Symmetry: For every pair of vertices u and v, the flow from u to v is the negative of the flow from v to u, i.e., f(u, v) = -f(v, u).

Flow Conservation: For every vertex u ∈ V \ {s, t}, the total flow into u must equal the total flow out of u. Mathematically, this is expressed as:
∑(v ∈ V) f(v, u) = ∑(v ∈ V) f(u, v)
==> This means if there are two edges coming into a vertex and their sum is 2 then the outflow is 2 as well; if one incoming edge has flow 2
and there are two outgoing edges, they could each carry 1, keeping in = out.

Max flow problem:

find the maximum s→t flow without violating capacity and conservation.

If there are too many nodes?

Solution idea: use a residual graph, which shows where more flow can still be pushed (or undone).

Residual Graph (core idea)

Given a current flow f, the residual capacity c_f(u, v) tells how much more we can send from u to v:

For a forward edge (u→v): c_f(u, v) = c(u, v) − f(u, v).

For a reverse edge (v→u): c_f(v, u) = f(u, v). (we can “undo” previously sent flow)

The residual graph G_f = (V, E_f) contains a directed edge (u, v) whenever c_f(u, v) > 0, with capacity c_f(u, v).

Intuition:

Forward residual edges let you push more flow up to remaining capacity.

Reverse residual edges let you pull back (cancel) some of the flow to reroute it more profitably elsewhere.

Augmenting Path & Ford–Fulkerson Method

Augmenting path: a simple path from s to t in the residual graph G_f where every edge has positive residual capacity.

Bottleneck on a path P: b = min{ c_f(e) : e ∈ P } — the max additional flow you can send along P.

Ford–Fulkerson (FF):

Start with zero flow: f(e)=0 for all e.

Build residual graph G_f.

If there exists an s→t augmenting path P in G_f:

Let b be its bottleneck.

Augment: for each edge (u, v) on P, increase f(u, v) by b; and for each reverse edge (v, u) on P, decrease f(v, u) by b.

Update residual capacities; repeat.

If no augmenting path exists, stop. Current f is a maximum flow.

Termination & Complexity:

If all capacities are integers, FF terminates and the number of augmentations ≤ total max flow value F. Time is O(E * F) (can be large).

Edmonds–Karp (EK) is FF with BFS to choose the shortest (in edges) augmenting path each time:

Time: O(V * E^2).

Easy to implement; reliable in practice.

Max-Flow Min-Cut Theorem (why Ford–Fulkerson is correct)

A cut (S, T) partitions V into S and T = V \ S with s ∈ S and t ∈ T.

Capacity of a cut: C(S, T) = ∑[u∈S, v∈T] c(u, v).

Theorem: The value of any s→t flow ≤ capacity of any s–t cut. Moreover:

When FF/EK halts (no augmenting path), there exists a cut whose capacity equals the current flow value.

Therefore, the final flow is maximum, and that cut is minimum.

Intuition sketch:

If no augmenting path exists, from s you cannot reach t in G_f.

Let S be the set of nodes reachable from s in G_f; then every edge crossing (S→T) in the original graph is saturated (f = c) and every edge T→S has zero flow.

Flow value equals sum of capacities on (S→T), i.e., equals the cut capacity ⇒ optimal.

Tiny Worked Example (by hand)

Edges (directed, capacity in parentheses):
s→a(3), s→b(2), a→b(1), a→t(2), b→t(3)

Start f=0. Residual capacities = original capacities.

Find path s→a→t. Bottleneck = min(3,2) = 2. Augment by 2.

Now f(s,a)=2, f(a,t)=2 (a→t saturated). Reverse edges a→s(2), t→a(2) appear in residual.

New path s→b→t. Bottleneck = min(2,3)=2. Augment by 2.

f(s,b)=2 (s→b saturated), f(b,t)=2 (still 1 capacity left on b→t).

Can we send more?

Try s→a (has 1 residual) → b via a→b(1) → t via b→t(1). Bottleneck = 1. Augment by 1:

f(s,a)=3 (now saturated), f(a,b)=1, f(b,t)=3 (now saturated).

No more s→t path exists in residual. Total max flow = f out of s = 3 + 2 = 5.

Check cut {s, a, b} / {t}: capacity = c(a,t)+c(b,t) = 2 + 3 = 5 ⇒ matches max flow."""