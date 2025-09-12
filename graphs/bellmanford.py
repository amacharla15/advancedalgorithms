"""
Bellman–Ford Algorithm 


──────────────────────────────────────────────────────────────────────────────
1) What is Bellman–Ford?
──────────────────────────────────────────────────────────────────────────────
Bellman–Ford is a single-source shortest path algorithm for weighted directed
graphs that may contain negative edge weights. It can also detect the presence
of a negative-weight cycle reachable from the source.

Key capabilities:
• Works with negative edge weights (unlike Dijkstra without reweighting).
• Detects negative cycles by a final “one more” relaxation pass.

When to use it:
• You have edges with negative weights.
• You must detect/report a negative cycle.
• Graph sizes where O(V·E) is acceptable (e.g., competitive programming,
  learning, or moderate-sized instances).


──────────────────────────────────────────────────────────────────────────────
2) Core Ideas (Intuition)
──────────────────────────────────────────────────────────────────────────────
“Relaxation” pushes improved distance estimates along edges. If the graph has V
vertices, the shortest simple path has at most (V-1) edges. Therefore, after
(V-1) full passes of edge relaxations, all shortest paths (without cycles) must
be found. If a (V-th) pass can still improve a distance, there exists a cycle
with negative total weight along some reachable path.

Relaxation rule for an edge u → v with weight w:
    if dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
        parent[v] = u    // optional: to reconstruct paths


──────────────────────────────────────────────────────────────────────────────
3) Pseudocode (Single-Source + Negative-Cycle Detection)
──────────────────────────────────────────────────────────────────────────────
Input:
    V = number of vertices, vertices indexed 0..V-1
    E = list of directed edges (u, v, w)
    s = source vertex

Output:
    dist[v] = shortest distance from s to v (if no neg. cycle reachable)
    parent[v] = predecessor of v on a shortest path (optional)
    or a report that a negative cycle is reachable

Initialize:
    for each v in 0..V-1:
        dist[v] = +∞
        parent[v] = NIL
    dist[s] = 0

Main (V-1) passes:
    for i in 1..V-1:
        updated = false
        for each edge (u, v, w) in E:
            if dist[u] != +∞ and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = true
        if not updated:
            break  // early stop optimization

Negative-cycle check (V-th pass):
    hasNegCycle = false
    for each edge (u, v, w) in E:
        if dist[u] != +∞ and dist[u] + w < dist[v]:
            hasNegCycle = true
            // Optionally: mark v (and nodes reachable from v) as -∞ distance
            // or reconstruct a specific negative cycle via parent links
            break

If hasNegCycle:
    report "Negative cycle reachable from source"
Else:
    report dist[0..V-1] and optionally reconstruct paths from parent[]


──────────────────────────────────────────────────────────────────────────────
4) Complexity
──────────────────────────────────────────────────────────────────────────────
Time:  O(V · E)
Space: O(V)

Notes:
• For sparse graphs (E ≈ V), O(V·E) ≈ O(V²).
• For dense graphs (E ≈ V²), O(V·E) ≈ O(V³).


──────────────────────────────────────────────────────────────────────────────
5) Correctness Sketch
──────────────────────────────────────────────────────────────────────────────
• After k full passes, Bellman–Ford has correctly computed the shortest paths
  that use at most k edges.
• Any shortest simple path uses ≤ (V-1) edges (no vertex repeats).
• Hence after (V-1) passes, all shortest paths are found.
• If one more pass still improves a distance, the “improvement” must rely on a
  cycle; its total weight must be negative, otherwise no strict improvement
  would be possible → negative cycle detected.


──────────────────────────────────────────────────────────────────────────────
6) Pros & Cons
──────────────────────────────────────────────────────────────────────────────
Pros:
• Handles negative edges.
• Detects negative cycles.
• Simple to implement; easy to reason about.

Cons:
• Slower than Dijkstra for non-negative graphs (O(V·E) vs O(E log V)).
• Can be costly on large dense graphs.

Common alternatives:
• Dijkstra (non-negative weights).
• Johnson’s algorithm (all-pairs on sparse graphs with possible negatives).
• Floyd–Warshall (all-pairs, dense/smaller graphs).


──────────────────────────────────────────────────────────────────────────────
7) Worked Example (Step-by-Step)
──────────────────────────────────────────────────────────────────────────────
Graph (directed edges):
    A(0) → B(1) (4)
    A(0) → C(2) (2)
    C(2) → B(1) (-3)
    B(1) → D(3) (2)
    C(2) → D(3) (3)

Map: A=0, B=1, C=2, D=3. Source s = A (0).

Initialization:
    dist = [0, +∞, +∞, +∞]
    parent = [NIL, NIL, NIL, NIL]

Pass 1: relax all edges
    (A→B, 4): 0+4 < ∞ → dist[B]=4,  parent[B]=A
    (A→C, 2): 0+2 < ∞ → dist[C]=2,  parent[C]=A
    (C→B,-3): 2-3= -1 < 4 → dist[B]=-1, parent[B]=C
    (B→D, 2): -1+2=1 < ∞ → dist[D]=1,  parent[D]=B
    (C→D, 3): 2+3=5  < 1 ? no
    After pass 1: dist = [0, -1, 2, 1], parents = [NIL, C, A, B]

Pass 2:
    (A→B): 0+4 < -1 ? no
    (A→C): 0+2 < 2 ?  no
    (C→B): 2-3= -1 < -1 ? no (equal)
    (B→D): -1+2=1 < 1 ?  no (equal)
    (C→D): 2+3=5 < 1 ?  no
    No updates → early stop

Negative-cycle check:
    Try each edge again; no further improvements → no negative cycle.

Final shortest distances from A:
    dist[A]=0, dist[B]=-1, dist[C]=2, dist[D]=1
Example shortest paths:
    A→C (2)
    A→C→B (-1)
    A→C→B→D (1)


──────────────────────────────────────────────────────────────────────────────
8) Path Reconstruction (Optional)
──────────────────────────────────────────────────────────────────────────────
Use parent[]:
    Reconstruct v’s path by following parent[v] → parent[parent[v]] → … → s,
    then reverse the sequence. Detect a loop during reconstruction if you’re
    reporting a negative cycle.


──────────────────────────────────────────────────────────────────────────────
9) Variants & Practical Notes
──────────────────────────────────────────────────────────────────────────────
• Early exit: If a full pass makes no updates, stop; distances are final.
• Reachability: Only edges from nodes with finite dist[u] can relax.
• SPFA (“Shortest Path Faster Algorithm”): A queue-based heuristic variant that
  often runs faster in practice but still has worst-case O(V·E). Good for many
  sparse, real-world graphs but not a guaranteed improvement.
• Negative cycle reporting: To print the actual cycle, track predecessors during
  detections and walk back V steps from an updated node, then loop until repeat.

──────────────────────────────────────────────────────────────────────────────
12) Quick Decision Guide (Which Algorithm When?)
──────────────────────────────────────────────────────────────────────────────
• Non-negative weights, single-source: Dijkstra (binary heap / Fibonacci heap).
• Negative edges, single-source: Bellman–Ford (and detect negative cycles).
• All-pairs on sparse graphs with possible negatives: Johnson’s (BF + Dijkstra).
• All-pairs on small/medium dense graphs: Floyd–Warshall.
• Real road networks / maps: A* / ALT / Contraction Hierarchies (with heuristics).

"""
