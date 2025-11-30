import heapq
import time

# ========== 1. Fixed Graph ==========
graph = {
    'a': ['b', 'c'],
    'b': ['a', 'd', 'e'],
    'c': ['a', 'f'],
    'd': ['b'],
    'e': ['b', 'f', 'g'],
    'f': ['c', 'e', 'h'],
    'g': ['e'],
    'h': ['f']
}

# ========== 2. Heuristic Values ==========
heuristic = {
    'a': 10,
    'b': 8,
    'c': 7,
    'd': 6,
    'e': 5,
    'f': 3,
    'g': 1,
    'h': 0
}

# ========== 3. Greedy Best-First Search ==========
def greedy_best_first(start, goal):
    if start == goal:
        return [start], [start], 0, 0

    visited = set()
    pq = []
    heapq.heappush(pq, (heuristic[start], start, [start]))

    expansion_order = []
    expansions = 0

    while pq:
        h, node, path = heapq.heappop(pq)
        expansion_order.append(node)
        expansions += 1

        if node == goal:
            cost = len(path) - 1
            return path, expansion_order, cost, expansions

        visited.add(node)

        for neigh in graph[node]:
            if neigh not in visited:
                heapq.heappush(pq, (heuristic[neigh], neigh, path + [neigh]))

    return None, expansion_order, None, expansions


# ========== 4. Main Program Loop ==========
while True:
    print("\n====================")
    s = input("Start Node (or type 'exit' to quit): ").strip().lower()

    if s == "exit":
        print("Program terminated.")
        break

    g = input("Goal Node: ").strip().lower()

    if g == "exit":
        print("Program terminated.")
        break

    if s not in graph or g not in graph:
        print("Invalid node name. Please try again.")
        continue

    start_time = time.perf_counter()
    path, expanded, cost, expansions = greedy_best_first(s, g)
    end_time = time.perf_counter()

    real_time = end_time - start_time

    if path is None:
        print("No path found to the goal.")
    else:
        print("Path:", " -> ".join(path))
        print("Cost:", cost)
        print("Expansions:", expansions)
        print(f"Real Time: {real_time:.8f} seconds")

    print("Expansion Order:", " -> ".join(expanded))
    print("====================\n")
