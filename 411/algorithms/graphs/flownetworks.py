"""
a graph G = (V, E) is a flow network if each edge (u, v) ∈ E has a non-negative capacity c(u, v) ≥ 0. 
and there is a source vertex s ∈ V and a sink vertex t ∈ V, s ≠ t.

s is called the source, and t is called the sink.
capacity is the maximum amount of flow that can pass through an edge.
flow is a term that shows what actually the edge carry

The flow must satisfy the following conditions:
1. Capacity Constraint: For every edge (u, v) ∈ E, the flow f(u, v) must not exceed the capacity c(u, v).
2. Skew Symmetry: For every pair of vertices u and v, the flow from u to v is the negative of the flow from v to u, i.e., f(u, v) = -f(v, u).
3. Flow Conservation: For every vertex u ∈ V \ {s, t}, the total flow into u must equal the total flow out of u. Mathematically, this is expressed as:
   ∑(v ∈ V) f(v, u) = ∑(v ∈ V) f(u, v)
   ==>This means if there are two edges coming into a vertex and their sum is 2 then the out flow is 2 as well, and if there is one vertex coming
   and two vertex flowing where one vertex has 2 as flow then the outflow edges will have flow as 1 and 1 


   Max flow problem:
   we need to find the maximum flow from source to sink in a flow network without
   violating the capacity constraints and flow conservation conditions.
    if there are too many nodes? 
    sol: residual graph
    a residual graph is a modified version of the original flow network that represents 
    the remaining capacity for additional flow.

"""