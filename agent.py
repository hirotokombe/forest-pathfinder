from collections import deque
import heapq

class SearchAgent:
    def __init__(self, start, goal, grid):
        self.start = start # tuple (row, col) for start position
        self.goal = goal # tuple (row, col) for goal position
        self.grid = grid # 2D list representing the forest
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.last_path = None # tracks the last complete path

    def is_valid(self, position):
        """Check if a position is within bounds and not an obstacle."""
        r, c = position
        return (0 <= r < self.rows) and (0 <= c < self.cols) \
            and (self.grid[r][c] != '#')

    def get_cost(self, position):
        """Return the traversal cost for stepping into a given cell."""
        cell = self.grid[position[0]][position[1]]
        if cell == 'f': # small fire
            return 3
        elif cell == 'F': # large fire
            return 5
        else:
            return 1 # open ground, start, or goal

    def get_neighbors(self, position):
        """Return a list of valid neighboring cells."""
        r, c = position
        candidates = [
            (r - 1, c),  # up
            (r + 1, c),  # down
            (r, c - 1),  # left
            (r, c + 1)  # right
        ]
        return [p for p in candidates if self.is_valid(p)]

    def print_path(self, path):
        """Utility to display the path on the grid (P marks the path)."""
        temp_grid = [row[:] for row in self.grid]  # copy the grid
        for (r, c) in path[1:-1]:  # exclude start and goal from marking
            temp_grid[r][c] = 'P'
        for row in temp_grid:
            print(" ".join(row))

    def bfs(self):
        """
        Performs Breadth-First Search (BFS) to find a path from the start cell
        to the goal cell.

        Returns:
            (path_length, nodes_expanded, total_cost) if a path is found,
            otherwise None.
        """
        visited = set()
        queue = deque([self.start])
        parent = {self.start: None}
        nodes_expanded = 0

        visited.add(self.start)

        while queue:
            node = queue.popleft()
            nodes_expanded += 1

            if node == self.goal:
                # Reconstruct path using parent pointers
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()

                path_length = len(path) - 1
                total_cost = sum(self.get_cost(p) for p in path[1:])

                self.print_path(path)
                self.last_path = path
                return (path_length, nodes_expanded, total_cost)

            # Expand neighbors in FIFO order
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    queue.append(neighbor)

        return None

    def dfs(self):
        """
        Performs Depth-First Search (DFS) using an explicit stack to find any valid
        path from the start cell to the goal cell.

        Returns:
            (path_length, nodes_expanded, total_cost) if a path is found,
            otherwise None.
        """
        visited = set()
        stack = [self.start]
        parent = {self.start: None}
        nodes_expanded = 0

        visited.add(self.start)

        while stack:
            node = stack.pop()  # LIFO order for depth-first exploration
            nodes_expanded += 1

            if node == self.goal:
                # Reconstruct path by following parent pointers backward
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()

                path_length = len(path) - 1
                total_cost = sum(self.get_cost(p) for p in path[1:])

                self.print_path(path)
                self.last_path = path
                return (path_length, nodes_expanded, total_cost)

            # Expand neighbors in a fixed order for reproducibility
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    stack.append(neighbor)

        return None

    def ucs(self):
        """
        Performs Uniform Cost Search (UCS) to find the minimum-cost path from the
        start cell to the goal cell. Nodes are expanded in order of increasing
        cumulative path cost g(n).

        Returns:
            (path_length, nodes_expanded, total_cost) if a path is found,
            otherwise None.
        """
        priority_queue = [(0, self.start)]
        parent = {self.start: None}
        best_cost = {self.start: 0}
        nodes_expanded = 0

        while priority_queue:
            cost, node = heapq.heappop(priority_queue)

            # Skip outdated entries if a cheaper path to this node was found later
            if cost != best_cost.get(node, float("inf")):
                continue

            nodes_expanded += 1

            if node == self.goal:
                # Reconstruct minimum-cost path using parent pointers
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()

                path_length = len(path) - 1
                total_cost = cost

                self.print_path(path)
                self.last_path = path
                return (path_length, nodes_expanded, total_cost)

            # Check neighbors and update costs if a cheaper path is found
            for neighbor in self.get_neighbors(node):
                new_cost = cost + self.get_cost(neighbor)
                if new_cost < best_cost.get(neighbor, float("inf")):
                    best_cost[neighbor] = new_cost
                    parent[neighbor] = node
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        return None

    def astar(self, heuristic=None):
        """
        Perform A* search from self.start to self.goal.
        Uses a priority queue ordered by f(n) = g(n) + h(n).

        Parameters:
            heuristic (callable, optional):
                A function h(pos) that estimates the distance from pos to the goal.
                If None, Manhattan distance is used by default.

        Returns:
            tuple (path_length, nodes_expanded, total_cost) if a path is found,
            or None if no path exists.
        """
        if heuristic is None:
            def heuristic(pos):
                return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

        priority_queue = [(heuristic(self.start), 0, self.start)]
        parent = {self.start: None}
        best_cost = {self.start: 0}
        nodes_expanded = 0

        while priority_queue:
            f, cost, node = heapq.heappop(priority_queue)

            # Skip outdated entries if a cheaper path to this node was found later
            if cost != best_cost.get(node, float("inf")):
                continue

            nodes_expanded += 1

            # Reconstruct path using parent pointers
            if node == self.goal:
                path = []
                cur = node
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()

                path_length = len(path) - 1
                total_cost = cost

                self.print_path(path)
                self.last_path = path
                return (path_length, nodes_expanded, total_cost)

            # Check neighbors and update costs if a cheaper path is found
            for neighbor in self.get_neighbors(node):
                new_cost = cost + self.get_cost(neighbor)
                if new_cost < best_cost.get(neighbor, float("inf")):
                    best_cost[neighbor] = new_cost
                    parent[neighbor] = node
                    heapq.heappush(priority_queue, (new_cost + heuristic(neighbor), new_cost, neighbor))

        return None

