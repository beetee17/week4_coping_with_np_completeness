# python3
import sys
sys.setrecursionlimit(10**6)
import threading

from collections import defaultdict
from queue import LifoQueue

threading.stack_size(2**26)

class Vertex():
    def __init__(self, index):
        self.index = index

        self.visited = 0
        self.scc = None

        self.pre = None
        self.post = None


class Graph():
    def __init__(self, edges, vertices):

        # create a dict with vertex as key and list of its neighbours as values
        self.adj = defaultdict(list)
    
        self.edges = edges

        # for a directed graph, b is adjacent to a but not vice versa
        for (a, b) in edges:
            self.adj[vertices[a]].append(vertices[b])
                    
        self.vertices = vertices
        self.num_scc = 1
        self.acyclic = True

        self.clock = 1
        self.postOrder = LifoQueue(maxsize=len(vertices))
        self.postOrderList = []
    
    def previst(self, v):
        v.scc = self.num_scc
        v.pre = self.clock
        self.clock += 1
        
    def postvist(self, v):
        v.post = self.clock
        self.clock += 1

        v.visited = 1
        self.postOrder.put_nowait(v)
        self.postOrderList.append(v)

    def explore(self, v):

        v.visited = -1
        # pre-vist block
        self.previst(v)

        # explore each neighbour of the vertex 
        for neighbour in self.adj[v]:
            if neighbour.visited == -1:
                self.acyclic = False

            if neighbour.visited == 0:
                self.explore(neighbour)

        # post-visit block
        self.postvist(v)
        
            
    def DFS(self):
        
        for v in self.vertices:
            # explore each vertex (and its neighbours)
            if v.visited == 0:
                self.explore(v)

        return self.postOrder
     

    def find_strongly_connected_components(self, reverse_postOrder):

        for v in self.vertices:
            v.visited = 0

        while not reverse_postOrder.empty():
            v = reverse_postOrder.get_nowait()
            # print(v.post)
            if v.visited == 0:
                self.explore(v)
                # once all neighbours of the vertex have been explored, they form a single strongly connected component
                self.num_scc += 1

        self.num_scc -= 1

        return self.postOrderList


def number_of_strongly_connected_components(edges, reverse_edges, vertices):
    # The vertex with the single largest post order number in the entire graph has to come from a component with no other components pointing to it. That vertex needs to be the source component
    # the reverse graph and the orig graph have the same strongly connected componenets (scc)
    # however, source component of reverse graph are sink componente of orig graph
    # therefore, by performing DFS on the reverse graph, we find its source components which give us the sink components of the original graph, which is what we want

    graph = Graph(edges, vertices)

    # let the reverse_graph be the graph obtained by flipping the direction of all its edges
    reverse_graph = Graph(reverse_edges, vertices)


    # perfrom DFS on reverse graph to populate post visit indices for each vertex
    # the postvisit block pushes each vertex into a stack such that getting each item ensures descending post order
    reverse_postOrder = reverse_graph.DFS()

    # a sink scc has no outgoing edges from the component
    # if v is in a sink component, explore(v) will find all the vertices reachable from v, which is the definition of a scc
    postOrderList = graph.find_strongly_connected_components(reverse_postOrder)


    return graph, postOrderList

def get_implicaton_graph(num_variables, clauses):
    # e.g there are 3 variables - x, y, z
    # the implication graph should have 3*2=6 nodes, 
    # deonting each variable and its negation e.g. x and NOT x
    # A variable with an index, i, will have its negation's index to be (i + num_variables)
    # For each clause, two edges can be added: one by taking the first variable and the
    # negation of the second variable, and vice versa
    # e.g. the clause (x OR NOT y) will result in the edges x -> y and NOT y -> NOT x
    # think of the -> as saying 'implies'. i.e. x implies y

    vertices = [Vertex(i) for i in range(num_variables*2)]
    edges = []
    reverse_edges = []

    for clause in clauses:
        
        # convert the literals to the correct indices in the vertices array
        if clause[0] < 0:
            literal1 = abs(clause[0]) + num_variables - 1
            neg_literal1 = abs(clause[0]) - 1
        else:
            neg_literal1 = abs(clause[0]) + num_variables - 1
            literal1 = abs(clause[0]) - 1

        if clause[1] < 0:
            literal2 = abs(clause[1]) + num_variables - 1
            neg_literal2 = abs(clause[1]) - 1
        else:
            neg_literal2 = abs(clause[1]) + num_variables - 1
            literal2 = abs(clause[1]) - 1
        
        edges.append([neg_literal1, literal2])
        edges.append([neg_literal2, literal1])

        reverse_edges.append([literal2, neg_literal1])
        reverse_edges.append([literal1, neg_literal2])

    return edges, reverse_edges, vertices

def solve_2SAT(edges, reverse_edges, vertices, num_variables):
    graph, postOrderList = number_of_strongly_connected_components(edges, reverse_edges, vertices)

    for var in range(num_variables):
        neg_var = var + num_variables
        if graph.vertices[var].scc == graph.vertices[neg_var].scc:
            return -1
    

    assignment = [None for i in range(num_variables)]
    postOrderList = [v.index+1 if v.index < num_variables else -(v.index-num_variables+1) for v in reverse_postOrderList]

    for i in postOrderList:
        if not assignment[abs(i)-1]:
            assignment[abs(i)-1] = i

    return assignment
    




def main():
    num_variables, num_clauses = map(int, input().split())
    clauses = [ list(map(int, input().split())) for i in range(num_clauses) ]

    edges, reverse_edges, vertices = get_implicaton_graph(num_variables, clauses)
    assignment = solve_2SAT(edges, reverse_edges, vertices, num_variables)

    if assignment == -1:
        print('UNSATISFIABLE')

    else:
        print('SATISFIABLE')
        print(' '.join(map(str, assignment)))

# to avoid stack overflow errors
threading.Thread(target=main).start()
   