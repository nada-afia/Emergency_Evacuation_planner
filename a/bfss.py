from collections import deque
import time

building = [
    ["S", "A", "B", "X", "C"],
    ["D", "F", "E", "K", "G"],
    ["H", "I", "J", "L", "M"]
]

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
    "J": ["E", "I", "L"],
    "L": ["J", "M"],      
    "M": ["G", "L"],
}

fires = ["X", "F", "K"]
start = "S"
goal = "E"

g_table = {
    "S":0, "A":1, "B":2, "C":3, "D":1, "E":3,
    "G":4, "H":2, "I":3, "J":4, "L":5, "M":5
}

def bfs_nodes(start, goal):
    start_time = time.time()  

    queue = deque()
    queue.append( (start, [start], ["Start"], 0) )  
    visited = set()
    
    print("---- BFS Exploration ----")
    
    while queue:
        node, path, moves, g = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        print(f"Visiting {node} | g={g} | Move: {moves[-1]}")
        if node == goal:
            end_time = time.time()  
            elapsed = end_time - start_time
            return path, moves, visited, elapsed
        for neighbor in nodes[node]:
            if neighbor not in visited and neighbor not in fires:
                queue.append( (neighbor, path + [neighbor], moves + [f"{node}->{neighbor}"], g + 1) )
    
    end_time = time.time()
    return None, None, visited, end_time - start_time
path, path_dirs, visited_nodes, runtime = bfs_nodes(start, goal)

if path:
    print("\nBFS Path with moves:")
    for node, move in zip(path, path_dirs):
        print(f"{node} <- {move}")
    
    print("\nAll path:")
    print(" → ".join(path))

    path_cost = sum(g_table[n] for n in path)
    print(f"\nPath Cost = {path_cost}")
    print(f"Time Taken = {runtime:.6f} seconds")
else:
    print("\nNo safe path found")

print("\nAll visited nodes:", visited_nodes)
