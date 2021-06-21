#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size

maxWeights = []

class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def ReadTree():
    global maxWeights
    size = int(input())
    maxWeights = [-1 for i in range(size)]
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree


def dfs(tree, vertex, parent):
    
    global maxWeights

    if maxWeights[vertex] == -1: # the max weight for this vertex has not been found

        if not tree[vertex].children: # the vertex has no children
            # only option is to select this vertex
            # max weight will simply be its weight
            maxWeights[vertex] = tree[vertex].weight

        else:

            # the vertex has some children
            m1 = tree[vertex].weight
            for child in tree[vertex].children:
                if child != parent:
                    for grandchild in tree[child].children:
                        if grandchild != vertex:
                            # option 1: select this vertex and its grandchildren solutions
                            m1 = m1 + dfs(tree, grandchild, child)

            # option 2: do not select this vertex, instead select its direct children and their solutions
            m0 = 0
            for child in tree[vertex].children:
                if child != parent:
                    m0 += dfs(tree, child, vertex)

            # get the max of both options
            maxWeights[vertex] = max(m1, m0)
    
    return maxWeights[vertex]

def MaxWeightIndependentTreeSubset(tree):
    global maxWeights
    size = len(tree)

    if size == 0: # tree is empty
        return 0

    maxWeight = dfs(tree, 0, -1)

    return maxWeight


def main():
    tree = ReadTree();
    maxWeight = MaxWeightIndependentTreeSubset(tree);
    print(maxWeight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()

# 5
# 1 5 3 7 5
# 5 4
# 2 3
# 4 2
# 1 2