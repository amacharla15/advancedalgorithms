// CSCI 411 - Fall 2025
// Assignment 1 Skeleton
// Author: Carter Tillquist
// Feel free to use all, part, or none of this code for the coding problem on assignment 1.

#include <iostream>
#include <memory>
#include <vector>
using namespace std;

/**************************************************************************
 * A simple Node struct                                                   *
 * id - int - the id or name of the node                                  *
 * SCC - int - the strongly connected component that this node belongs to *
 * visited - bool - whether or not this node has been visited             *
 * ************************************************************************/
struct Node {
    int id;
    int SCC;
    bool visited;
};

/**************************************************************************************************
 * A simple struct of strongly connected component (SCC) graph nodes                              *
 * id - int - the id or name of the node (this corresponds to the SCC id)                         *
 * size - int - the number of nodes from the original graph that belong to this SCC               *
 * hasInEdges - bool - true if there are edges with end points in this SCC and false otherwise    *
 * hasOutEdges - bool - true if there are edges with start points in this SCC and false otherwise *
 * ************************************************************************************************/
struct SCCNode {
    int id;
    int size;
    bool hasInEdges;
    bool hasOutEdges;
};

/*********************************************************
 * A simple struct to hold the sizes of sets A, B, and C *
 * A - int - the size of set A                           *
 * B - int - the size of set B                           *
 * C - int - the size of set C                           *
 * *******************************************************/
struct Result {
    int A;
    int B;
    int C;
};

/******************************************************************************************************************
 * Given the adjacency list of a graph, generate a new adjacency list with the same nodes but with edges reversed *
 * A - vector<vector<shared_ptr<Node>>> - an adjacency list representation of a graph. Note that A[0] is a list   * 
 *     of all the Nodes in the graph with an additional dummy Node at A[0][0]. As a result, A[i] are the          * 
 *     neighbors of the Node with id i where these ids go from 1 to n, the size of the graph                      *
 * return - vector<vector<shared_ptr<Node>>> - an adjacency list of a new graph equivalent to the original but    *
 *          with edges reversed                                                                                   *
 * ****************************************************************************************************************/
vector<vector<shared_ptr<Node>>> reverseEdges(vector<vector<shared_ptr<Node>>> A){
  // YOUR CODE HERE
  int n = static_cast<int>(A[0].size()) - 1;   // Number of real nodes: A[0] holds pointers A[0][1 to n] (A[0][0] is a dummy)      
    vector<vector<shared_ptr<Node>>> R(n + 1); // Creating a reversed adjacency list with indices 0 to n
    R[0] = A[0];// Sharing the same Node objects between A and R (ids, visited, SCC stay in sync)                                      
    for (int u = 1; u <= n; ++u){// For each node u in the original graph
        for (const auto& to : A[u]){//for each outgoing edge u -> v in A
            int v = to->id;// target node id of edge u -> v                         
            R[v].push_back(A[0][u]); // Adding the reversed edge v -> u into R by pushing a pointer to node u                     
        }
    }
    // Returning the adjacency list with all edges reversed
    return R;

}

/********************************************************************************************************
 * A variation of DFS for the first pass over a graph looking for strongly connected components.        *
 * The goal is to fill the vector L with nodes in decreasing order with respect to finishing time       *
 * A - vector<vector<shared_ptr<Node>>> - an adjacency list                                             *
 * v - shared_ptr<Node> - the start node for the DFS                                                    *
 * &L - vector<shared_ptr<Node>> - a list of nodes to be filled in decreasing order with respect to     *
 *      finishing time                                                                                  *
 * ******************************************************************************************************/
void DFSSCC(vector<vector<shared_ptr<Node>>> A, shared_ptr<Node> v, vector<shared_ptr<Node>> &L){
  // YOUR CODE HERE
    // If this node was already visited in this pass, we stop.
    if (v->visited) return;
    // Markin current node as visited.
    v->visited = true;
    // For every neighbor w with an edge v -> w 
    // (Adjacency is stored so that A[v->id] lists v's outgoing neighbors.)
    for (const auto& w : A[v->id]){
        // Exploring w only if it hasn't been visited yet.
        if (!w->visited){
            DFSSCC(A, w, L);
        }
    }
    // After exploring all descendants of v, we record v's finishing time.
    // ensuring L ends up sorted by decreasing finishing time.
    L.push_back(v);
}

/******************************************************************************************************************
 * A variation of DFS for the second pass over a graph looking for strongly connected components.                 *
 * There are three goals (1) to label nodes with a SCC id (2) to generate nodes of a SCC metagraph (3) and to     *
 * determine which nodes in this metagraph have incoming and outgoing edges.                                      *
 * A - vector<vector<shared_ptr<Node>>> - an adjacency list representing the transpose or edge reverse of the     *
 *     original graph                                                                                             *
 * v - shared_ptr<Node>- the start node for the DFS                                                               *
 * scc - int - the current strongly connected component id                                                        *
 * &SCCs - vector<SCCNode> - the nodes of a SCC metagraph                                                         *
 ******************************************************************************************************************/
void DFSAssign(vector<vector<shared_ptr<Node>>> A, shared_ptr<Node> v, int scc, vector<SCCNode> &SCCs){
  // YOUR CODE HERE
  // If already visited in this pass, we do nothing
    if (v->visited) return;
    // Markig and labelling this node with the current SCC id
    v->visited = true;
    v->SCC = scc;
    // Counting this node toward the size of its SCC.
    ++SCCs[scc].size;
    // Exploring all neighbors in the TRANSPOSE graph (edges reversed).
    // In the transpose, an original edge u->w becomes w->u,
    // so traversing T groups together nodes that are mutually reachable.
    for (const auto& w : A[v->id]) {
        if (!w->visited) {
            DFSAssign(A, w, scc, SCCs);
        }
    }
}

/******************************************************************************************************
 * Find the strongly connected components (SCCs) of a graph. The SCC of each Node is added to the SCC *
 * member of the Node struct. In addition, a vector of SCCNode is returned.                           *
 * A - vector<vector<shared_ptr<Node>>> - an adjacency list                                           *
 * return - vector<SCCNode> - a vector of nodes in the SCC metagraph of A                             *
 * ****************************************************************************************************/
vector<SCCNode> SCC(vector<vector<shared_ptr<Node>>> A){
  // YOUR CODE HERE
  // Number of real nodes (A[0][1 to n] holds the actual Node pointers; A[0][0] is a dummy)
    int n = static_cast<int>(A[0].size()) - 1;
    //First pass (on original G): build finishing-time order L
    
    // Resetting all visit marks before the first DFS pass.
    for (int i = 1; i <= n; ++i) A[0][i]->visited = false;   // clear visited
    //Creating the list that will store nodes by finishing time.
    // Reserving n avoids reallocations during pushes.

    //Run DFS from every unvisited node.
    vector<shared_ptr<Node>> L; L.reserve(n);                
    for (int i = 1; i <= n; ++i) {// iterate over all node ids 1 to n
      if (!A[0][i]->visited) {// if node i has not been visited in this first pass
        // run DFS starting at node i.
        // DFSSCC explores reachable nodes and, when each node finishes,
        // it pushes that node into L (postorder). This builds L in increasing
        // finishing time; reading L from back to front gives decreasing order
        DFSSCC(A, A[0][i], L);
      }
    }


    auto T = reverseEdges(A);// Building the TRANSPOSE graph T: every edge u->v becomes v->u.                           
    for (int i = 1; i <= n; ++i) A[0][i]->visited = false; // clear all visited flags  

    vector<SCCNode> sccNodes; sccNodes.reserve(n); // This will store one record per SCC: {id, size, hasIn, hasOut}, Max SCCs is n (each node alone), so reserve n to avoid reallocations     
    int sccCount = 0;// Next SCC id to assign (0, 1, 2, ...)
    for (int i = static_cast<int>(L.size()) - 1; i >= 0; --i){ // Processing nodes in DECREASING finishing time
        auto v = L[i];// Taking the next node by that order
        if (!v->visited){// this deals if this node hasn't been assigned to an SCC yet
            // Creating a new SCC record; size will be incremented inside DFSAssign
            sccNodes.push_back(SCCNode{ sccCount, 0, false, false });// Starting a NEW SCC record with current id sccCount
            DFSAssign(T, v, sccCount, sccNodes);//mark ing all reachable nodes with SCC = sccCount, increasing sccNodes[sccCount].size for each             
            ++sccCount;// Advancing to the next SCC id for future components
        }
    }

    for (int u = 1; u <= n; ++u) {// visiting each original node id u = 1..n
    int cu = A[0][u]->SCC;// cu = SCC id (component) that node u belongs to
    for (const auto& to : A[u]) {// for every edge u -> (to->id) in the ORIGINAL graph
        int cv = to->SCC;// cv = SCC id of the head endpoint (neighbor)
        if (cu != cv) {// if the edge goes between two DIFFERENT SCCs
            sccNodes[cu].hasOutEdges = true;// then cu’s component has at least one outgoing edge
            sccNodes[cv].hasInEdges  = true;// and cv’s component has at least one incoming edge
          }
        }
    }
    return sccNodes;// return all SCC records with size & in/out flags filled
}

/************************************************************************************************
 * Given the adjacency list representation of a graph, fill and return a Result struct with the *
 * number of nodes that belong to the three sets A, B, and C as described in assignment 1       *
 * A - vector<vector<shared_ptr<Node>>> - an adjacency list                                     *
 * return - Result - a Result struct holding the sizes of sets A, B, and C                      *
 * **********************************************************************************************/
Result getSetSizes(vector<vector<shared_ptr<Node>>> A){
  // YOUR CODE HERE
    vector<SCCNode> sccs = SCC(A);// computing SCCs and per-SCC metadata (size, hasInEdges, hasOutEdges)
    Result R{0, 0, 0};// counters for |A|, |B|, |C|
    for (const auto& s : sccs) {// examining each SCC (tie-group)
        if (!s.hasInEdges && s.hasOutEdges) {
            R.A += s.size;// TOP group: no incoming, some outgoing -> contributes to |A|
        } else if (s.hasInEdges && !s.hasOutEdges) {
            R.B += s.size;// BOTTOM group: some incoming, no outgoing -> contributes to |B|
        } else {
            R.C += s.size;// MIDDLE/ISOLATED: everything else -> contributes to |C|
        }
    }
    return R;// return the triple (|A|, |B|, |C|)
}

int main(){
    //get the number of nodes and number of edges from cin separated by a space
    int n = -1, m = -1;
    cin >> n >> m;


    //add the nodes to an adjacency list
    //note that A[0] is a list of nodes with a dummy node in A[0][0]
    //this means that A[i] is the node with id i where ids start at 1
    vector<vector<shared_ptr<Node>>> A(n+1);
    A[0].push_back(shared_ptr<Node>(new Node()));
    for (int i=1; i<n+1; i++){
        shared_ptr<Node> v = shared_ptr<Node>(new Node());
        v->id = i;
        v->SCC = -1;
        v->visited = false;
        A[0].push_back(v);
    }

    //get edges from cin and add them to the adjacency list
    //the start and end of a single edge are on the same line separated by a space
    int u = -1, v = -1;
    for (int i=0; i<m; i++){
        cin >> u >> v;
        A[u].push_back(A[0][v]);
    }

    //call getSetSizes to determine the size of the sets A, B, and C and print the results
    Result R = getSetSizes(A);
    cout << "|A| = " << R.A << ", |B| = " << R.B << ", |C| = " << R.C;
    return 0;
}

