#Strongly Connected components
"""
A strongly connected component is a maximal set of vertices in a directed graph where:

Every vertex is reachable from every other vertex in that set.

"Maximal" means you can’t add more vertices to the set without breaking the property.


Why a cycle is necessary

For mutual reachability:

If vertex 𝑢u can reach vertex v and v can reach u, 
then there is a path  u→v and a path v→u.

Combining those two paths naturally forms a directed cycle 
(could be length 2 or longer).

If no cycles exist in that subgraph, it’s acyclic → you 
can’t have mutual reachability except for the trivial “reach yourself” case.
"""

