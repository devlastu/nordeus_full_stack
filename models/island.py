import heapq
from typing import List, Set

from observers.game_state import Coordinates


class Island:
    def __init__(self, coordinates: Set[tuple[int, int]], matrix: List[List[int]]):
        """
        Initialize the Island object.

        Parameters:
            coordinates (List[Coordinates]): List of Coordinates objects representing the island.
            matrix (List[List[int]]): The height matrix of the map.
        """
        # Convert Coordinates to a set of tuples for efficient membership checks
        self.coordinates: coordinates = coordinates
        self.matrix = matrix
        self.avg_height = self.calculate_avg_height()  # Calculate avg_height upon creation
        self.area = self.calculate_area()  # Calculate area upon creation
        self.mst = []  # MST will be calculated when the island is created
        self.create_minimum_spanning_tree()

    def __repr__(self):
        return f"Island(avg_height={self.avg_height}, area={self.area}, coordinates={self.coordinates} cells)"

    def calculate_avg_height(self) -> float:
        """Calculate and return the average height of the island."""
        if not all(isinstance(coord[0], int) and isinstance(coord[1], int) for coord in self.coordinates):
            raise TypeError("Coordinates must be integers.")
        total_height = sum(self.matrix[coord[0]][coord[1]] for coord in self.coordinates)
        return total_height / len(self.coordinates)

    def calculate_area(self) -> int:
        """Calculate and return the area of the island (number of non-zero land cells)."""
        return len([coord for coord in self.coordinates if self.matrix[coord[0]][coord[1]] > 0])

    def create_minimum_spanning_tree(self):
        """Create a Minimum Spanning Tree (MST) for this island."""
        island_cells = [(coord[0], coord[1]) for coord in self.coordinates]

        if not island_cells:
            return

        self.mst = self._prim_algorithm(island_cells)

    def _prim_algorithm(self, island_cells):
        """
            Implementation of Prim's Algorithm to generate the MST.

        """
        mst_edges = []
        visited = set()
        min_heap = []

        start = island_cells[0]
        visited.add(start)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = start[0] + dx, start[1] + dy
            if (nx, ny) in island_cells and (nx, ny) not in visited:
                heapq.heappush(min_heap, ((start, (nx, ny))))

        while min_heap:
            cell1, cell2 = heapq.heappop(min_heap)
            if cell2 not in visited:
                visited.add(cell2)
                mst_edges.append((cell1, cell2))

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cell2[0] + dx, cell2[1] + dy
                    if (nx, ny) in island_cells and (nx, ny) not in visited:
                        heapq.heappush(min_heap, (cell2, (nx, ny)))

        return mst_edges

    # Getter methods
    def get_avg_height(self) -> float:
        """Getter for the average height of the island."""
        return self.avg_height

    def get_area(self) -> int:
        """Getter for the area of the island (number of land cells)."""
        return self.area

    def get_coordinates(self) -> Set[tuple[int, int]]:
        """Getter for the coordinates of the island."""
        return self.coordinates

    def get_mst(self) -> List:
        """Getter for the Minimum Spanning Tree (MST) of the island."""
        return self.mst
