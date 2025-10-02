"""
Dijkstra’s Algorithm (Single-Source Shortest Paths, Nonnegative Weights)
=======================================================================

WHAT THIS FILE CONTAINS
-----------------------
1) implementation of Dijkstra using:
   - dist[]  : best-known distance from source to each node
   - visited[] (settled): node is finalized when popped from PQ
   - parent[]: to reconstruct actual shortest paths
   - a binary heap (heapq) priority queue

2) Tiny driver example and path reconstruction helper.

3) “Greedy property” explanation (why the algorithm is correct):
   Dijkstra makes a greedy choice at each step: it permanently selects the
   unsettled node u with the smallest tentative distance dist[u]. This is safe
   (i.e., can’t hurt the optimality of the final answer) when all edges are
   NONNEGATIVE. The cut between {settled nodes} and {unsettled nodes} is a valid
   cut; among all edges crossing this cut, any path reaching an unsettled node
   through a settled node is at least dist[u] + w(u,v). Because dist[u] is the
   smallest among unsettled nodes, no alternative path coming from unsettled
   territory can improve it later without using a negative-weight edge. Hence,
   once u is popped from the PQ, dist[u] is FINAL.

WHEN TO USE
-----------
- All edge weights ≥ 0  -> Use Dijkstra (this file).
- Some edge < 0         -> Use Bellman–Ford (or Johnson’s for all-pairs).
- All edges = 1         -> BFS is simpler and optimal.

GRAPH FORMAT
------------
- n: number of vertices (0..n-1)
- adj: adjacency list where adj[u] is a list of (v, w) pairs
       meaning an edge u -> v with nonnegative weight w
- Undirected graph: push both directions.
- Directed graph: push only the given direction.

COMPLEXITY
----------
- Using a binary heap and adjacency lists: O(E log V).

"""

import heapq
from typing import List, Tuple, Optional

def build_adjacency_list(n: int, edges: List[Tuple[int, int, float]], undirected: bool = True) -> List[List[Tuple[int, float]]]:
    """
    Build adjacency list from an edge list.
    edges: list of (u, v, w)
    undirected=True -> add both (u->v, v->u)
    """
    adj: List[List[Tuple[int, float]]] = []
    # initialize empty lists
    i = 0
    while i < n:
        adj.append([])
        i += 1

    i = 0
    m = len(edges)
    while i < m:
        u, v, w = edges[i]
        # push u -> v
        adj[u].append((v, w))
        if undirected:
            # push v -> u
            adj[v].append((u, w))
        i += 1

    return adj


def dijkstra(n: int, adj: List[List[Tuple[int, float]]], src: int) -> Tuple[List[float], List[Optional[int]]]:
    """
    Dijkstra single-source shortest paths.
    - n: number of nodes (0..n-1)
    - adj[u]: list of (v, w) neighbors
    - src: starting node

    Returns:
      dist[]  : shortest distances from src
      parent[]: predecessor for each node in a shortest path tree
    """
    # Initialize arrays
    INF = float('inf')
    dist: List[float] = [0.0] * n
    parent: List[Optional[int]] = [None] * n
    visited: List[int] = [0] * n  # 0 = not settled, 1 = settled

    i = 0
    while i < n:
        dist[i] = INF
        parent[i] = None
        visited[i] = 0
        i += 1

    dist[src] = 0.0

    # Min-heap of (distance, node)
    pq: List[Tuple[float, int]] = []
    heapq.heappush(pq, (0.0, src))

    # Main loop
    while len(pq) > 0:
        cur_dist, u = heapq.heappop(pq)

        # Skip stale entries
        if visited[u] == 1:
            continue
        visited[u] = 1  # settle u; dist[u] is now final

        # Relax all edges (u -> v, w)
        j = 0
        deg = len(adj[u])
        while j < deg:
            v, w = adj[u][j]

            # Dijkstra requires nonnegative w
            # If w < 0, this algorithm is not valid.
            alt = cur_dist + w
            if alt < dist[v]:
                dist[v] = alt
                parent[v] = u
                heapq.heappush(pq, (alt, v))
            j += 1

    return dist, parent


def reconstruct_path(parent: List[Optional[int]], src: int, target: int) -> List[int]:
    """
    Reconstruct shortest path from src to target using parent[].
    Returns a list of nodes from src to target.
    If target is unreachable, returns [].
    """
    path: List[int] = []
    cur = target

    # If unreachable, parent chain never reaches src and dist[target] would be inf.
    # Here we just reconstruct blindly; caller should check dist first if needed.
    while cur is not None:
        path.append(cur)
        if cur == src:
            break
        cur = parent[cur]

    # If we didn’t end on src, there is no valid path
    if len(path) == 0 or path[-1] != src:
        return []

    # reverse path
    i = 0
    j = len(path) - 1
    while i < j:
        tmp = path[i]
        path[i] = path[j]
        path[j] = tmp
        i += 1
        j -= 1

    return path


def _tiny_demo():
    """
    Tiny demo:
      0 --1-- 1 --2-- 2
       \      |
        \3    |1
          \   |
            3
    Edges (undirected):
      (0,1,1), (1,2,2), (0,3,3), (1,3,1)
    Shortest from 0:
      dist[0]=0, dist[1]=1, dist[3]=2 (0->1->3), dist[2]=3 (0->1->2)
    """
    n = 4
    edges = [(0,1,1.0), (1,2,2.0), (0,3,3.0), (1,3,1.0)]
    adj = build_adjacency_list(n, edges, undirected=True)
    src = 0
    dist, parent = dijkstra(n, adj, src)

    print("dist:", dist)
    t = 2
    path_0_to_2 = reconstruct_path(parent, src, t)
    print("path 0->2:", path_0_to_2)


if __name__ == "__main__":
    # Run the tiny demo if you execute this file directly
    _tiny_demo()


"""
GREEDY PROPERTY (Why Dijkstra’s Choice Is “Safe”)
-------------------------------------------------
At each step, Dijkstra removes from the priority queue the unsettled node u with
the smallest tentative distance dist[u] and permanently settles it. Consider the
cut (S, V \ S) where S is the set of already settled nodes (including u). Because
all edge weights are nonnegative, any path reaching an unsettled node v through
an unsettled intermediate cannot reduce the cost to u afterward. Thus, dist[u]
is already the minimum possible distance from the source to u; marking it
“visited/settled” is safe and never needs revision.

COMMON PITFALLS
---------------
- Mark visited when you POP a node from the PQ, not when you PUSH it.
- Do not use Dijkstra if any edge weight is negative.
- For unweighted graphs (all w=1), use BFS instead.
"""
