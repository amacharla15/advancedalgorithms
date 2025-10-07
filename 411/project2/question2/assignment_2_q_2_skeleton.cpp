// CSCI 411 - Fall 2025
// Assignment 2 Question 2 - Outpost
// Author: Carter Tillquist
// Feel free to use all, part, or none of this code for the outpost problem on assignment 2.

#include <iostream>
#include <memory>
#include <vector>
#include <set>
#include <math.h>

/****************************************************************
 * A simple struct to help track outpost information            *
 * id - int - the outpost id                                    *
 * x - float - the outpost's x coordinate                       *
 * y - float - the outpost's y coordinate                       *
 * s - float - the signal strength of the outpost's transmitter *
 ****************************************************************/
struct Outpost {
  int id;
  float x;
  float y;
  float s;
};

/****************************************************************************************************************************
 * A function to determine the maximum number of outposts that can be contacted with a single visit to the planet's surface *
 * outposts - vector<Outpost> - a vector of all outposts, index corresponds to outpost id                                   *
 * distances - vector<vector<float>> - a distance matrix, distances[i][j] is the distance from outpost i to outpost j       *
 * return - numContacted - the maximum number of outposts that can be contacted                                             *
 ****************************************************************************************************************************/
int maxContacts(std::vector<Outpost>& outposts, std::vector<std::vector<float>>& distances){
    const int n = (int)outposts.size();

    // 1) Building directed graph: i -> j if dist(i,j) <= s_i
    //G[i] will store all outposts j that i can reach (edges i→j).
    //GT is the transpose graph: GT[j] will store all i that can reach j (edges j←i).
    std::vector<std::vector<int>> G(n), GT(n);
    //Double loopING over all ordered pairs (i, j) of outposts.
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < n; ++j){
            //CheckING if outpost j is within the signal range of outpost i.
            //distances[i][j] is the Euclidean distance between i and j.
            //outposts[i].s is i’s transmit strength (max distance it can send).
            //+ 1e-9f is a tiny tolerance to avoid floating-point edge-case errors when the distance equals the range
            if (distances[i][j] <= outposts[i].s + 1e-9f){
                G[i].push_back(j);//If i can reach j, WEe add a directed edge i→j to G.
                GT[j].push_back(i); // transposing simultaneously
            }
        }
    }

    // 2) Kosaraju (iterative) - order via DFS on G
    //We’ll run the first DFS of Kosaraju.
    //state[i] tracks DFS status for node i: 
    //not visited (0), on the stack/being explored (1), or fully done (2).
    std::vector<char> state(n, 0); // 0=unseen,1=discovering,2=finished
    //order will store vertices in finishing order (postorder)
    std::vector<int> order; order.reserve(n);
    //to start a DFS from every node (to cover disconnected parts).
    for (int start = 0; start < n; ++start){
        //Skiping nodes already visited by a previous DFS.
        if (state[start] != 0) continue;
        //Using the stack st to simulate recursion (iterative DFS).
        //Pushing the start node.
        std::vector<int> st; st.push_back(start);
        //Dfs loop
        while (!st.empty()){
            int u = st.back();
            if (state[u] == 0){
                state[u] = 1; // discover
                for (int v : G[u]){
                    if (state[v] == 0) st.push_back(v);
                }
            } else {
                st.pop_back();
                if (state[u] != 2){
                    state[u] = 2;      // finish
                    order.push_back(u); // postorder
                }
            }
        }
    }

    // 3) Assign components via DFS on GT (iterative)
    //comp_id[i] will store which strongly connected component (SCC) 
    //node i belongs to.
    std::vector<int> comp_id(n, -1);
    //Counter for how many SCCs we’ve found so far (also used as the current SCC id).
    int comp_cnt = 0;
    //Process nodes in reverse finishing order from the first DFS (Kosaraju rule).
    for (int idx = n - 1; idx >= 0; --idx){
        //root is the next node to seed a DFS on the transpose graph GT.
        int root = order[idx];
        //If this node already belongs to some SCC, we skip it.
        if (comp_id[root] != -1) continue;
        //Starting an iterative DFS on GT from root.
        //Assigning root to the current component comp_cnt.
        std::vector<int> st; st.push_back(root);
        comp_id[root] = comp_cnt;
        //Standard DFS loop using a stack.
        while (!st.empty()){
            int u = st.back(); st.pop_back();
            for (int v : GT[u]){//Exploing incoming edges of u in the original graph, i.e., outgoing edges in GT.
                //Any unassigned neighbor v reachable in GT is in the same SCC.
                //Assigning it the same comp_cnt and continue DFS from it
                if (comp_id[v] == -1){
                    comp_id[v] = comp_cnt;
                    st.push_back(v);
                }
            }
        }
        //When the stack empties, we’ve collected one full SCC.
        //Incrementing comp_cnt to label the next SCC discovered by later iterations.
        ++comp_cnt;
    }

    // 4) Component sizes
    //Making an array sizeC of length = number of SCCs.
    //sizeC[c] will store how many original nodes are in component
    std::vector<int> sizeC(comp_cnt, 0);
    //For every node v, we look up its component id comp_id[v] and increment that component’s size.
    for (int v = 0; v < n; ++v) ++sizeC[comp_id[v]];

    // 5) Condensed DAG H (dedup parallel edges)
    //Creating adjacency lists for the condensed graph H.
    
    // Each vertex of H is one SCC. We’ll add edges between components.
    std::vector<std::vector<int>> H(comp_cnt);
    //For each component, we keep a set to remember which outgoing 
    //component edges we’ve already added (to avoid duplicates like C→D added many times).
    std::vector<std::set<int>> seenEdge(comp_cnt);
    for (int u = 0; u < n; ++u){//looping over eacg origina node u 
        int cu = comp_id[u];//cu = component that u belongs to.
        for (int v : G[u]){//For every edge u → v in the original graph, we find cv = component of v.
            int cv = comp_id[v];
            //If this edge goes between different components (cu != cv) and we haven’t already recorded an edge from cu to cv
            if (cu != cv && !seenEdge[cu].count(cv)){
                seenEdge[cu].insert(cv);
                H[cu].push_back(cv);
            }
        }
    }

    // 6) BFS from each component on H to count reachable total
    int ans = 0;//This will hold the best (maximum) number of outposts we can reach from a single landing.
    for (int c0 = 0; c0 < comp_cnt; ++c0){//Trying starting from each SCC (component) c0 as the landing place.
        std::vector<char> mark(comp_cnt, 0);//mark[c] tells us if component c has been visited in this run.
        std::vector<int> Q; Q.reserve(comp_cnt);//An array used as a queue for BFS over the condensed DAG H.
        int head = 0;//head is the index of the current front element.
        //Start BFS from c0. Mark it visited, enqueue it.
        mark[c0] = 1;
        Q.push_back(c0);
        int total = 0;//total will count how many original outposts are reachable from c0.
        //Standard BFS loop while queue not empty.
        while (head < (int)Q.size()){
            int c = Q[head++];
            total += sizeC[c];
            for (int d : H[c]){
                if (!mark[d]){
                    mark[d] = 1;
                    Q.push_back(d);
                }
            }
        }
        if (total > ans) ans = total;
    }

    return ans;
}



/************************************************************
 * Determines the distance between two outposts             *
 * a - Outpost - an outpost with x, y coordinates           *
 * b - Outpost - a second outpost                           *
 * return - the Euclidean distance between the two outposts *
 ************************************************************/
float distance(Outpost a, Outpost b){
  return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
}

int main(){
  // Get the total number of outposts
  int n = -1;
  std::cin >> n;

  // Get outpost information
  std::vector<Outpost> outposts;
  float x = 0, y = 0, s = 0;
  for (int i = 0; i < n; i++){
    std::cin >> x >> y >> s;
    Outpost o;
    o.id = i;
    o.x = x;
    o.y = y;
    o.s = s;
    outposts.push_back(o);
  }

  // Determine pairwise outpost distances
  std::vector<std::vector<float>> distances(outposts.size(), std::vector<float>(outposts.size(), 0));
  for (int i = 0; i < outposts.size(); i++){
    for (int j = i+1; j < outposts.size(); j++){
      float dist = distance(outposts[i], outposts[j]);
      distances[i][j] = dist;
      distances[j][i] = dist;
    }
  }

  std::cout << maxContacts(outposts, distances) << std::endl;  

  return 0;
}
