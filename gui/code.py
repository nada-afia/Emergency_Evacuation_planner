import tkinter as tk
import random
import heapq
import time
from collections import deque

GRID_SIZE = 20
CELL_SIZE = 30

START = (0, 0)
GOALS = [(19, 19), (19, 0), (0, 19)]
FIRE_COUNT = 50


def ucs_fire(nodes, start, goals, fires, cell_cost):
    pq = []
    heapq.heappush(pq, (cell_cost[start[0]][start[1]], start, [start]))
    visited = set()
    expanded = []

    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        expanded.append(node)

        if node in goals:
            return path, cost, expanded

        for n in nodes[node]:
            if n not in fires and n not in visited:
                r, c = n
                heapq.heappush(pq, (cost + cell_cost[r][c], n, path + [n]))

    return None, None, expanded


def dfs_fire(nodes, start, goals, fires, cell_cost):
    stack = [(start, [start], cell_cost[start[0]][start[1]])]
    visited = set()
    expanded = []

    while stack:
        node, path, cost = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        expanded.append(node)

        if node in goals:
            return path, cost, expanded

        for n in reversed(nodes[node]):
            if n not in visited and n not in fires:
                r, c = n
                stack.append((n, path + [n], cost + cell_cost[r][c]))

    return None, None, expanded


def bfs_fire(nodes, start, goals, fires, cell_cost):
    q = deque([(start, [start], cell_cost[start[0]][start[1]])])
    visited = {start}
    expanded = []

    while q:
        node, path, cost = q.popleft()
        expanded.append(node)

        if node in goals:
            return path, cost, expanded

        for n in nodes[node]:
            if n not in visited and n not in fires:
                r, c = n
                visited.add(n)
                q.append((n, path + [n], cost + cell_cost[r][c]))

    return None, None, expanded


def heuristic_to_goals(node, goals):
    return min(abs(node[0]-g[0]) + abs(node[1]-g[1]) for g in goals)


def astar_fire(start, goals, fires, cell_cost):
    pq = [(heuristic_to_goals(start, goals) + cell_cost[start[0]][start[1]], 
           cell_cost[start[0]][start[1]], start, [start])]
    visited = set()
    expanded = []

    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        expanded.append(node)

        if node in goals:
            return path, g, expanded

        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = node[0]+dr, node[1]+dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and (nr, nc) not in fires:
                ng = g + cell_cost[nr][nc]
                heapq.heappush(
                    pq,
                    (ng + heuristic_to_goals((nr,nc), goals), ng, (nr, nc), path + [(nr, nc)])
                )
    return None, None, expanded


def greedy_fire(start, goals, fires, cell_cost):
    pq = [(heuristic_to_goals(start, goals), start, [start], cell_cost[start[0]][start[1]])]
    visited = set()
    expanded = []

    while pq:
        h, node, path, cost = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        expanded.append(node)

        if node in goals:
            return path, cost, expanded

        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = node[0]+dr, node[1]+dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and (nr, nc) not in fires:
                heapq.heappush(
                    pq,
                    (heuristic_to_goals((nr, nc), goals) + cost + cell_cost[nr][nc],
                     (nr, nc),
                     path + [(nr, nc)],
                     cost + cell_cost[nr][nc])
                )
    return None, None, expanded


def depth_limited_dfs(node, goal, limit, path, visited, expansion_order, nodes, cell_cost, cost):
    expansion_order.append(node)

    if node == goal:
        return path, cost

    if limit == 0:
        return None, None

    visited.add(node)

    for neigh in nodes[node]:
        if neigh not in visited:
            r, c = neigh
            result_path, result_cost = depth_limited_dfs(
                neigh, goal, limit-1, path+[neigh], visited, expansion_order, nodes, cell_cost, cost + cell_cost[r][c]
            )
            if result_path is not None:
                return result_path, result_cost

    return None, None


def iterative_deepening_dfs(start, goal, nodes, cell_cost):
    max_depth = len(nodes)
    expansions_total = 0
    depth_expansion_list = []

    for depth in range(max_depth):
        visited = set()
        expansion_order = []

        result_path, result_cost = depth_limited_dfs(
            start, goal, depth, [start], visited, expansion_order, nodes, cell_cost, cell_cost[start[0]][start[1]]
        )

        depth_expansion_list.append(expansion_order)
        expansions_total += len(expansion_order)

        if result_path is not None:
            return result_path, depth_expansion_list, result_cost, expansions_total

    return None, depth_expansion_list, None, expansions_total



class EvacuationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency_Evacuation_planner")

        self.grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.cells = []
        self.path = []
        self.index = 0

        self.algo = tk.StringVar(value="UCS")

        top = tk.Frame(root)
        top.pack()

        tk.Label(top, text="Algorithm:").pack(side="left")
        tk.OptionMenu(
            top, self.algo,
            "UCS", "DFS", "BFS", "A*", "Greedy", "IDDFS"
        ).pack(side="left")

        tk.Button(top, text="Start", command=self.start).pack(side="left")
        tk.Button(top, text="Clear", command=self.clear).pack(side="left")

        self.info = tk.Label(root, text="")
        self.info.pack()

        self.canvas = tk.Canvas(
            root,
            width=GRID_SIZE*CELL_SIZE,
            height=GRID_SIZE*CELL_SIZE
        )
        self.canvas.pack()

        self.init_fire()
        self.draw_grid()

    def init_fire(self):
        for _ in range(FIRE_COUNT):
            r = random.randint(0, GRID_SIZE-1)
            c = random.randint(0, GRID_SIZE-1)
            if (r, c) != START and (r, c) not in GOALS:
                self.grid[r][c] = 1

    def draw_grid(self):
        self.canvas.delete("all")
        self.cells = []
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                color = "white"
                if (r, c) == START:
                    color = "purple"
                elif (r, c) in GOALS:
                    color = "green"
                elif self.grid[r][c] == 1:
                    color = "red"

                rect = self.canvas.create_rectangle(
                    c*CELL_SIZE, r*CELL_SIZE,
                    (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                    fill=color, outline="black"
                )
                row.append(rect)
            self.cells.append(row)

    def clear(self):
        self.path = []
        self.index = 0
        self.draw_grid()
        self.info.config(text="")

    def build_nodes(self, fires):
        nodes = {}
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) not in fires:
                    nodes[(r, c)] = []
                    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and (nr, nc) not in fires:
                            nodes[(r, c)].append((nr, nc))
        return nodes

    def start(self):
        fires = {(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 1}
        nodes = self.build_nodes(fires)
        cell_cost = [[random.randint(1,5) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        algo = self.algo.get()
        t0 = time.time()

        if algo == "DFS":
            self.path, total_cost, _ = dfs_fire(nodes, START, GOALS, fires, cell_cost)
        elif algo == "BFS":
            self.path, total_cost, _ = bfs_fire(nodes, START, GOALS, fires, cell_cost)
        elif algo == "A*":
            self.path, total_cost, _ = astar_fire(START, GOALS, fires, cell_cost)
        elif algo == "Greedy":
            self.path, total_cost, _ = greedy_fire(START, GOALS, fires, cell_cost)
        elif algo == "IDDFS":
            self.path, _, total_cost, _ = iterative_deepening_dfs(START, GOALS[0], nodes, cell_cost)
        else:
            self.path, total_cost, _ = ucs_fire(nodes, START, GOALS, fires, cell_cost)

        self.index = 0
        self.move()

        self.info.config(
            text=f"{algo} | Path Total Cost: {total_cost if total_cost else 'N/A'} | Steps: {len(self.path) if self.path else 'N/A'} | Time: {time.time()-t0:.3f}s"
        )

    def move(self):
        if self.index >= len(self.path):
            for r, c in self.path:
                if (r, c) != START and (r, c) not in GOALS:
                    self.canvas.itemconfig(self.cells[r][c], fill="purple")
            return

        r, c = self.path[self.index]
        self.index += 1
        self.draw_grid()

        x1 = c*CELL_SIZE + 6
        y1 = r*CELL_SIZE + 6
        x2 = x1 + CELL_SIZE - 12
        y2 = y1 + CELL_SIZE - 12

        self.canvas.create_oval(x1, y1, x2, y2, fill="purple")
        self.root.after(200, self.move)


if __name__ == "__main__":
    root = tk.Tk()
    EvacuationGUI(root)
    root.mainloop()