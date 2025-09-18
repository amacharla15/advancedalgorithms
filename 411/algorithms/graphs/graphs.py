"""
Topological Sort:

Ordering of the vertices of a Directed Acyclic Graph (DAG) 
such that for every directed edge (u, v),
vertex u comes before vertex v in the ordering.

**** Only defined for DAGs
***If there is a cycle, topological sort is not possible
*** A topological ordering is not necessarily unique—different
 valid orders may exist depending on which nodes are chosen first.

"""

"""

**This algorithm can help checking for cycles in a directed graph.
1) Kahn's Algorithm (BFS-based):
--> Find a node with no incoming edges (in-degree 0)
add it to end of the topological order
--> Remove that node and its outgoing edges from the graph
repeat until the graph is empty or no nodes with in-degree 0 are found
if there are still nodes in the graph, it contains a cycle


step by step:

Compute in-degree of every vertex
Count incoming edges for each node.
Why: nodes with in-degree 0 have no prerequisites and can go first.

Initialize a queue with all in-degree-0 nodes
Any of these can start the ordering. If there are multiple, any order among them is fine.

Pop from the queue, append to the result
This “emits” a node in the topological order.

For each outgoing edge from that node (u → v)
Decrease inDegree[v] by 1 (we’re “removing” the edge because u is now placed).

If any neighbor’s in-degree becomes 0, push it into the queue
It has no remaining unmet prerequisites.

Repeat steps 3–5 until the queue is empty.

Cycle check

If the result contains all V nodes, success: you have a topological order.

If not, there’s a cycle (some nodes never reached in-degree 0).

===========================================================================================

Time Complexity: O(V + E)::
Building in-degree array
→ Go through all edges once → O(E)

Processing queue
→ Remove each node once → O(V)

For each node’s adjacency list
→ Iterate over each outgoing edge exactly once → O(E)

O(V) for nodes+O(E) for edges=O(V+E)
"""

"""


"""