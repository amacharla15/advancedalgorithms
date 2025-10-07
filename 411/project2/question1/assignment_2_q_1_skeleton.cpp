// CSCI 411 - Fall 2025
// Assignment 2 Skeleton
// Author: Carter Tillquist
// Feel free to use all, part, or none of this code for the first coding problem on assignment 2.

#include <iostream>
#include <memory>
#include <vector>
#include <deque>
#include <climits>
#include <algorithm>
using namespace std;

/******************************************************************************
 * A simple Node struct                                                       *
 * id - int - the id or name of the node                                      *
 * dist - int - the distance from some given node to this node                *
 * inI - bool - true if the node is a member of the set I and false otherwise *
 * visited - bool - whether or not this node has been visited                 *
 * ****************************************************************************/
struct Node {
    int id;
    int dist;
    bool inI;
    bool visited;
};

/**************************************************************************
 * A simple Edge struct                                                   *
 * from - shared_ptr<Node> - the node where this edge starts              *
 * to - shared_ptr<Node> - the node where this edge ends                  *
 * weight - int - the weight of this edge                                 *
 * ************************************************************************/
struct Edge {
    shared_ptr<Node> from;
    shared_ptr<Node> to;
    int weight;
};

/****************************************************************************************************************************
 * Given a graph, find the set of nodes that belong to the set I, that is, the set of vertices v such that there            *
 * is at least one path of length negative infinity ending at v.                                                            *
 * A - vector<vector<shared_ptr<Edge>>> - an adjacency list representation of a graph where each element is a weighted edge *
 * return - vector<int> - the integer ids of nodes in the set I                                                             *
 * **************************************************************************************************************************/
vector<int> findSetI(vector<vector<shared_ptr<Edge>>> A){
    // YOUR CODE HERE
    
    int n = (int)A.size() - 1; //In this , A has n+1 buckets: bucket 0 is differet (used only to stash per-node pointers). 
    //So the actual number of graph vertices is n = A.size() - 1.

    // Building  nodes array so we can quickly get the shared_ptr<Node> for each id.
    // For each stored real node’s pointer in A[0][i]->from. We copy those pointers into nodes[i] for easy access later.
    vector<shared_ptr<Node>> nodes(n + 1);
    for (int i = 1; i <= n; ++i) nodes[i] = A[0][i]->from;

    //I'm going to run Bellman–Ford from a super-source s.
    //s is an artificial node with id 0 and I Will add a zero-weight edge s -> v for every real vertex v.
    //this lets us treat every vertex as potentially reachable, which is what we need when we’re searching for any negative cycle anywhere in the graph (not just from one chosen start).
    shared_ptr<Node> s(new Node());
    s->id = 0; s->dist = 0; s->inI = false; s->visited = false;
    //Eprime will be a flat list of edges for the augmented graph G`= (V U {s}, E U {(s-->v)})
    //and the keyword reserve avoids repeated allocations
    vector<shared_ptr<Edge>> Eprime;
    Eprime.reserve( (size_t) (n + 1) * 4 );

    // copying all original nodes from the adjacency list into Eprime
    //and after this loop Eprime containes exactly the edges of the original graph E
    for (int u = 1; u <= n; ++u){
        for (auto &e : A[u]) Eprime.push_back(e);
    }
    // Adding the zero weight edges (s --> v) for every real vertex v 
    //with the prevous loop Eprime now represents E` = E U {(s --> v, 0) v}
    // so iwth the augumentation running bellman ford from s detects any 
    //negative cycle that is reachable from some vertex , 
    //because from s we can reach every vertex via these 0-cost edges. 






    //For every real vertex v, creating an edge (s → v) of weight 0 and append it to Eprime
    // so that making a super-source s that can “reach” every vertex at zero cost so Bellman–Ford can 
    //see negative cycles anywhere in the graph
    for (int v = 1; v <= n; ++v){
        shared_ptr<Edge> e(new Edge());
        e->from = s;
        e->to   = nodes[v];
        e->weight = 0;
        Eprime.push_back(e);
    }

    // Bellman–Ford from s for |V'|-1 = n rounds
    const long long INF = (long long)4e18;
    // dist array holds the current best distance estimate from s to each vertex id.
    vector<long long> dist(n + 1, INF);
    dist[0] = 0;//Index 0 corresponds to s. Initializing all to INF, except s which starts at 0.
    //for a node pointer, we return its integer id. If it’s the super-source pointer s, return 0; 
    //otherwise return its stored id
    auto getId = [&](const shared_ptr<Node>& p)->int {
        return (p == s ? 0 : p->id);
    };
    //main bellman-ford loop:

    //doing up to n iterations bcause |V`| = n+1 and we run |V`| -1 = n rounds
    //for every edge u → v in the augmented edge list Eprime, we  try to improve
    // (relax) dist[v] using dist[u] + weight(u,v) 
    //we skip edges whiose tail u is still at INF which is unreachable
    //if any distance improved in an iteration we set changed = True
    // and if an iteration makes no changes we break early
    // it is because after n rounds if any edges can still relax it means a negative cycle is reachable
    //from s and we will detect that in the next block of code
    for (int it = 1; it <= n; ++it){
        bool changed = false;
        for (auto &e : Eprime){
            int u = getId(e->from);
            int v = getId(e->to);   // never 0 in practice, but safe
            if (dist[u] == INF) continue;
            long long cand = dist[u] + (long long)e->weight;
            if (cand < dist[v]){
                dist[v] = cand;
                changed = true;
            }
        }
        if (!changed) break;
    }

    // creating a  array inS initialized to zero
    //inS[v] = 1 will mean “vertex v is affected by a negative cycle (on or reachable from one).”
    vector<char> inS(n + 1, 0);

    //Scanning every edge in the augmented edge list Eprime one more time
    //after Bellman–Ford finished.
    for (auto &e : Eprime){
        //for ecah edge convert pointers to integre ids getId
        //if u was unreachable (dist[u] == INF), weskip it.
        int u = getId(e->from);
        int v = getId(e->to);
        if (dist[u] == INF) continue;
        //Computing the relaxed distance candidate cand = dist[u] + weight(u,v).
        long long cand = dist[u] + (long long)e->weight;
        //If cand < dist[v] even after the full BF rounds, this means distances could 
        //still be improved ⇒ a negative cycle is reachable that can influence v.
        if (cand < dist[v]){
            if (v != 0) inS[v] = 1; 
        }
    }

    // If S empty, we return empty I
    //Checking whether we found any vertex influenced by a negative cycle.
    bool anyS = false;
    for (int v = 1; v <= n; ++v) if (inS[v]) { anyS = true; break; }
    //If none, the set I (vertices that can end a path of length −∞) is empty, so we return {}.
    if (!anyS) return {};

    // Preparing a BFS/DFS forward flood on the original graph (not Eprime).

    //visited marks vertices we’ve already enqueued/processed.

    //Q is a queue for BFS 
    //I will accumulate all vertices reachable from the poisoned set
    vector<char> visited(n + 1, 0);
    deque<int> Q;
    vector<int> I;

    //Iterating over all real vertices 1..n
    for (int v = 1; v <= n; ++v){
        if (inS[v] && !visited[v]){
            visited[v] = 1;//Marking it visited.
            Q.push_back(v);//enquing it as a bfs start node
            I.push_back(v); // adding to the answer set I 
        }
    }
    //BFS traversal
    while (!Q.empty()){
        int x = Q.front(); Q.pop_front();
        for (auto &e : A[x]){            
            int y = e->to->id;
            if (!visited[y]){
                visited[y] = 1;
                Q.push_back(y);
                I.push_back(y);
            }
        }
    }

    return I;
}


int main(){  
    //get the number of nodes and number of edges from cin separated by a space
    int n = -1, m = -1;
    cin >> n >> m;

    //add the nodes to an adjacency list
    //in this case, A[i] is a vector of all edges leaving A[i]
    //note that A[0] is a list of self loops representing all nodes in the graph
    //these are not actual edges in the graph, just a way to keep track of all nodes
    //Furthermore, A[0][0] is a dummy edge with a dummy node
    //this means that A[0][i] represents the node with id i where ids start at 1
    vector<vector<shared_ptr<Edge>>> A(n+1);
    A[0].push_back(shared_ptr<Edge>(new Edge()));
    for (int i=1; i<n+1; i++){
        shared_ptr<Node> v = shared_ptr<Node>(new Node());
        v->id = i;
        v->dist = INT_MAX;
        v->inI = false;
        v->visited = false;
        shared_ptr<Edge> e = shared_ptr<Edge>(new Edge());
        e->from = v;
        e->to = v;
        e->weight = 0;
        A[0].push_back(e);
    }

    //get edges from cin and add them to the adjacency list
    //the start, end, and weight of a single edge are on the same line separated by spaces
    int u = -1, v = -1, w = -1;
    for (int i=0; i<m; i++){
        cin >> u >> v >> w;
        shared_ptr<Edge> e = shared_ptr<Edge>(new Edge());
        e->from = A[0][u]->from;
        e->to = A[0][v]->to;
        e->weight = w;
        A[u].push_back(e);
    }

    //find nodes belonging to the set I and print them out in ascending order
    vector<int> I = findSetI(A);
    sort(I.begin(), I.end());
    for (int i=0; i<(int)I.size()-1; i++){
        cout << I[i] << " ";
    }
    if (I.size() > 1){ cout << I[I.size()-1] << endl; }

    return 0;
}
