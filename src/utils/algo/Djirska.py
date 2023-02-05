import heapq


class PathFinder:
    """
    Dijkstra's algorithm
    Useful to find the shortest path around on obstacle to reach the given destination [mazes, obstacles, ...]
    Works better when obstacles are nearer and not too complex.
    """
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

    def get_valid_neighbors(self, curr):
        x, y = curr
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        valid_neighbors = [(x, y) for x, y in neighbors if
                           0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] != "#"]
        return valid_neighbors

    def get_shortest_path(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        heap = [(0, start_x, start_y)]
        visited = set()
        while heap:
            (cost, x, y) = heapq.heappop(heap)  # smallest
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) == (end_x, end_y):
                break
            for neighbor in self.get_valid_neighbors((x, y)):
                nx, ny = neighbor
                heapq.heappush(heap, (cost + 1, nx, ny))

        return visited
