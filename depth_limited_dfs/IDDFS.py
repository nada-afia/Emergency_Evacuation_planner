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

# ========== 2. Depth-Limited DFS ==========
def depth_limited_dfs(node, goal, limit, path, visited, expansion_order):
    expansion_order.append(node)

    if node == goal:
        return path

    if limit == 0:
        return None

    visited.add(node)

    for neigh in graph[node]:
        if neigh not in visited:
            result = depth_limited_dfs(
                neigh,
                goal,
                limit - 1,
                path + [neigh],
                visited,
                expansion_order
            )
            if result is not None:
                return result

    return None

# ========== 3. Iterative Deepening DFS ==========
def iterative_deepening_dfs(start, goal):
    if start == goal:
        return [start], [[start]], 0, 1

    max_depth = len(graph)
    expansions_total = 0
    path_found = None
    depth_expansion_list = []  # List of expansions for each depth

    for depth in range(max_depth):
        visited = set()
        expansion_order = []
        result = depth_limited_dfs(
            start,
            goal,
            depth,
            [start],
            visited,
            expansion_order
        )

        depth_expansion_list.append(expansion_order.copy())
        expansions_total += len(expansion_order)

        if result is not None:
            path_found = result
            cost = len(result) - 1
            return path_found, depth_expansion_list, cost, expansions_total

    return None, depth_expansion_list, None, expansions_total

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
    path, depth_expansions, cost, expansions_total = iterative_deepening_dfs(s, g)
    end_time = time.perf_counter()

    real_time = end_time - start_time

    if path is None:
        print("No path found to the goal.")
    else:
        print("Path:", " -> ".join(path))
        print("Cost:", cost)
        print("Total Expansions:", expansions_total)
        print(f"Real Time: {real_time:.8f} seconds")

    # طباعة الـ expansion لكل depth
    print("\nExpansion Order by Depth:")
    for depth, nodes in enumerate(depth_expansions):
        print(f"Depth {depth}: {' -> '.join(nodes)}")

    print("====================\n")
