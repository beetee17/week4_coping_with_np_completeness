# python3
from itertools import permutations
INF = 10 ** 9

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph

def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))

def optimal_path(graph):
    # This solution tries all the possible sequences of stops.
    # It is too slow to pass the problem.
    # Implement a more efficient algorithm here.
    n = len(graph)
    best_ans = INF
    best_path = []

    for p in permutations(range(n)):
        cur_sum = 0
        for i in range(1, n):
            if graph[p[i - 1]][p[i]] == INF:
                break
            cur_sum += graph[p[i - 1]][p[i]]
        else:
            if graph[p[-1]][p[0]] == INF:
                continue
            cur_sum += graph[p[-1]][p[0]]
            if cur_sum < best_ans:
                best_ans = cur_sum
                best_path = list(p)

    if best_ans == INF:
        return (-1, [])
    return (best_ans, [x + 1 for x in best_path])

def optimal_path_dp(graph):
    from itertools import combinations
    import math
    n = len(graph)
    subsets = []

    minCostDP = {}
    parent = {}
    index = {}

    for i in range(n):  # to get all lengths: 0 to 3
        for subset in combinations(range(1, n), i):
            subsets.append(subset)
            index.update({len(index) : subset})
            
    print(graph)

    for subset in subsets:
        for v in range(1, n): 
            if v in subset: continue

            minCost = math.inf
            minPrev = 0
            

            for prev in subset:
                cost = graph[prev][v]
                prev_subset = [u if u != prev for u in subset]
                cost += minCostDP[prev][prev_subset]

                if cost < minCost:
                    minCost = cost
                    minPrev = prev

            if not subset:
                minCost = graph[v][0]

            parent.update({subset : minPrev})
            minCostDP.update({subset : minCost})
            print(minCostDP)


        



if __name__ == '__main__':
    # print_answer(*optimal_path(read_data()))
    graph = read_data()
    optimal_path_dp(graph)
# 4 6
# 1 2 20
# 1 3 42
# 1 4 35
# 2 3 30
# 2 4 34
# 3 4 12