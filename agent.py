class SearchAgent:
    def __init__(self, start, goal, grid):
        self.start = start # tuple (row, col) for start position
        self.goal = goal # tuple (row, col) for goal position
        self.grid = grid # 2D list representing the forest
        self.rows = len(grid)
        self.cols = len(grid[0])

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

    def print_path(self, path):
        """Utility to display the path on the grid (P marks the path)."""
        temp_grid = [row[:] for row in self.grid]  # copy the grid
        for (r, c) in path[1:-1]:  # exclude start and goal from marking
            temp_grid[r][c] = 'P'
        for row in temp_grid:
            print(" ".join(row))

    def bfs(self):
        # TODO: Implement BFS to find lowest-step path (unweighted shortest path).
        # Return a tuple (path_length, nodes_expanded, total_cost),
        # or indicate failure if no path is found.
        pass

    def dfs(self):
        # TODO: Implement DFS to find a path (not necessarily optimal).
        # Return (path_length, nodes_expanded, total_cost) similar to BFS.
        pass

    def ucs(self):
        # TODO: Implement Uniform Cost Search for optimal path with costs.
        # Use a priority queue (e.g., heapq) to always expand the lowest-cost node.
        # Return (path_length, nodes_expanded, total_cost).
        pass

    def astar(self, heuristic=None):
        # If no heuristic is provided, use Manhattan distance by default.
        if heuristic is None:
            def heuristic(pos):
                return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])
        # TODO: Implement A* search using the given heuristic function.
        # Use a priority queue similar to UCS, but prioritize by g(n)+h(n).
        # Return (path_length, nodes_expanded, total_cost).
        pass