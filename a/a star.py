import time
from heapq import heappush, heappop

building = [
    ["S", "A", "B", "X", "C"],
    ["D", "F", "E", "K", "G"],
    ["H", "I", "J", "L", "M"]
]

fires = ["X", "F", "K"]

nodes = {
    "S": ["A", "D"],
    "A": ["S", "B"],
    "B": ["A", "C", "E"],
    "C": ["B", "G"],      
    "D": ["S", "E", "H"], 
    "E": ["B", "D", "J"], 
    "G": ["C", "M"],      
    "H": ["D", "I"],
    "I": ["H", "J"],      
    "L": ["J", "M"],      
    "M": ["G", "L"],
}

start = "S"
goal = "E"

g_table = {
    "S": 0, "A": 1, "B": 2,
    "C": 3, "D": 1, "E": 3, 
    "G": 4, "H": 2, "I": 3,
    "J": 4, "L": 5, "M": 5
}

h_table = {
    "S": 6, "A": 5, "B": 4,
    "C": 3, "D": 3, "E": 0, 
    "G": 2, "H": 4, "I": 3,
    "J": 1, "L": 1, "M": 2
}

def f_cost(node):
    return g_table[node] + h_table[node]

def astar_nodes_predefined(start, goal):
    start_time = time.time()

    open_heap = []
    heappush(open_heap, (f_cost(start), start, [start])) 
    visited = set()

    while open_heap:
        f, node, path = heappop(open_heap)

        if node in visited:
            continue

        visited.add(node)

        print(f"Visiting {node} | g={g_table[node]} | h={h_table[node]} | f={f}")

        if node == goal:
            end_time = time.time()
            elapsed = end_time - start_time
            return path, visited, elapsed

        for neighbor in nodes[node]:
            if neighbor not in visited:
                heappush(open_heap, (f_cost(neighbor), neighbor, path + [neighbor]))

    end_time = time.time()
    return None, visited, end_time - start_time

path, visited_nodes, runtime = astar_nodes_predefined(start, goal)

if path:
    print("\nA* Path:", " → ".join(path))
    path_cost = sum(g_table[n] for n in path)
    print("Path Cost =", path_cost)

    print(f"Time Taken = {runtime:.6f} seconds")

else:
    print("\nNo safe path found")

print("\nAll visited nodes:", visited_nodes)
