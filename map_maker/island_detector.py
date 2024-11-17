from numpy.testing.print_coercion_tables import print_coercion_table

from models.island import Island
from observers.game_state import Coordinates
from typing import List

class IslandDetector:
    """
    Utility class to detect islands.
    """

    def dfs(self, i: int, j: int, matrix: List[List[int]], visited: List[List[bool]], island_cells: List[tuple]):
        """
        Perform Depth First Search (DFS) to find all connected cells of an island.

        Args:
            i (int): The starting row index.
            j (int): The starting column index.
            matrix (list of list of int): The input matrix representing land heights.
            visited (list of list of bool): A matrix to track visited cells.
            island_cells (list of tuple): List to store coordinates of cells in the current island.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        stack = [(i, j)]
        visited[i][j] = True
        island_cells.append((i, j))

        while stack:
            x, y = stack.pop()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and not visited[nx][ny] and matrix[nx][ny] > 0:
                    visited[nx][ny] = True
                    stack.append((nx, ny))
                    island_cells.append((nx, ny))

    def find_islands(self, matrix: List[List[int]]) -> List[Island]:
        """
        Find all islands in the given matrix.

        Args:
            matrix (list of list of int): The input matrix representing land heights.

        Returns:
            list of Island: A list of Island objects representing all detected islands.
        """
        visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
        islands = []

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                # print(matrix[i][j])
                if matrix[i][j] > 0 and not visited[i][j]:
                    island_cells = []
                    self.dfs(i, j, matrix, visited, island_cells)
                    if len(island_cells) > 1:  # Filter out too small islands
                        # Create an Island object, passing the matrix and cells
                        islands.append(Island(
                            coordinates=set([(cell[0], cell[1]) for cell in island_cells]),
                            matrix=matrix
                        ))

        return islands
