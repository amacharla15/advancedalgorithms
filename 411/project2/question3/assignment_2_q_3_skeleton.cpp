// CSCI 411 - Fall 2025
// Assignment 2 Question 3 - Count Shortest Paths Skeleton
// Author: Carter Tillquist
// Feel free to use all, part, or none of this code for the third coding question on assignment 2.

#include <iostream>
#include <queue>
#include <vector>
#include <map>

/*********************************************************************************
 * A simple node struct                                                          *
 * id - int - the id of the node                                                 *
 * dist - int - the distance from a source node to this node                     *
 * numPaths - int - the number of paths from a source node to this node          *
 * neighbors - vector<int> - a list of the integer ids if neighbors of this node *
 * visited - bool - true if this node has been visited and false otherwise       *
 *********************************************************************************/
struct Node {
  int id;
  int dist;
  int numPaths;
  std::vector<int> neighbors;
  bool visited;
};

/**************************************************************
 * Count the number of shortest paths from s to u             *
 * nodes - map<int, Node> - a map from node id to node struct *
 * s - int - the id of the start node                         *
 * u - int - the id of the end or target node                 *
 * return - int - the number of shortest paths from s to u    *
 **************************************************************/

int countShortestPaths(std::map<int, Node> nodes, int s, int u){
  // YOUR CODE HERE
    // If s or u were never inserted (isolated), add defaults so lookups work
    auto makeNode = [](int id){//defininmg a function such that it taks and int id and returns a Node
        Node a; //cretaing  a local Node variable a that we’ll fill in and return.
        a.id = id;//Setting the node’s identifier to the given id.
        a.dist = -1;//Initializing distance to -1 to mean “unknown / not discovered yet.”
        a.numPaths = 0;//Initially there are 0 known paths from the source to this node.
        a.neighbors = {};//Starting with an empty list of neighbors (no edges recorded here yet).
        a.visited = false;//Marking the node as not visited.
        return a;//with thsi we return the fully initialized Node.
    };
    //If the map nodes doesn’t contain the source s, 
    //we insert a default node for s using makeNode(s).
    // This guarantees lookups like nodes[s] are safe.
    if (nodes.find(s) == nodes.end()) nodes[s] = makeNode(s);
    if (nodes.find(u) == nodes.end()) nodes[u] = makeNode(u);

    // Trivial case: s == u -> exactly one shortest path of length 0
    //if the start and end are the same node there is exactly one shortest path (the trivial length-0 path), 
    //so we return 1 immediately
    if (s == u) return 1;

    // BFS from s, tracking:
    //  dist[v]    = shortest distance from s to v
    //  numPaths[v]= number of shortest paths from s to v
    std::queue<int> q; //Creating a FIFO queue to drive the BFS.
    nodes[s].dist = 0;//Initializing the source’s distance to 0 (distance from s to itself).
    nodes[s].numPaths = 1;//this means there’s one shortest path to s from s: the empty path.
    nodes[s].visited = true;//Marking s as discovered so we don’t re-enqueue it unnecessarily.
    q.push(s);//Starting the BFS by putting the source node s into the queue.

    while (!q.empty()){//we keep exploring while there are nodes waiting in the BFS queue
        int x = q.front(); q.pop();//we take the next node x from the front of the queue (FIFO)

        for (int v : nodes[x].neighbors){//Looking at every neighbor v of x.
            if (nodes.find(v) == nodes.end()) {
                nodes[v] = makeNode(v);//if v wasn’t inserted in the map yet, we create a default Node for it (distance −1, 0 paths, etc.). 
                // in case an endpoint only appears once
            }
            // First time discovered: we set distance and inherit path count
            if (nodes[v].dist == -1){//If v has no distance yet (undiscovered), this is the first time we see it.
                nodes[v].dist = nodes[x].dist + 1;//Setting v’s shortest distance to one more than x’s
                nodes[v].numPaths = nodes[x].numPaths; //All current shortest paths to v come through x, so we copy the number of shortest paths to x.
                q.push(v);//enqueue
            }
            // Another shortest path to v found via x
            //If v already has a distance, and going x -> v reaches exactly that same shortest distance, then we’ve found another shortest path to v
            else if (nodes[v].dist == nodes[x].dist + 1){
              //we add the number of shortest paths to x to v’s total, because each shortest path to x followed by edge (x, v) is a shortest path to v.
                nodes[v].numPaths += nodes[x].numPaths;
            }
        }
    }
    //After BFS, we return how many shortest paths reached the target u. If u was never discovered, numPaths stays 0.
    return nodes[u].numPaths; // 0 if unreachable
}

int main(){
  // Get the number of nodes and edges along with the start and end vertices
  int n = -1, m = -1, s = -1, u = -1;
  std::cin >> n >> m >> s >> u;

  // Here I have chosen to store the graph in a map
  // You can think of this as a hash table (though under the hood it is implemented as a red-black tree in C++)
  // The keys here are node ids and the values are the nodes themselves
  // You are, of course, welcome to use a different representation if you would prefer
  std::map<int, Node> nodes;
  int w = -1, v = -1;
  for (int i = 0; i < m; i++){
    std::cin >> w >> v;
    if (nodes.find(w) == nodes.end()){
      Node a;
      a.id = w;
      a.dist = -1;
      a.numPaths = 0;
      a.neighbors = {};
      a.visited = false;
      nodes[w] = a;
    }
    if (nodes.find(v) == nodes.end()){
      Node b;
      b.id = v;
      b.dist = -1;
      b.numPaths = 0;
      b.neighbors = {};
      b.visited = false;
      nodes[v] = b;
   }
   nodes[w].neighbors.push_back(v);
   nodes[v].neighbors.push_back(w);
  }

  std::cout << countShortestPaths(nodes, s, u) << std::endl;

  return 0;
}
