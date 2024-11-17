import heapq
from services.api_service import MapService
from map_maker.island_detector import IslandDetector

class Dimensions():
    width: int
    height: int

class Map:
    """
        The Map class manages the map's data, including fetching the map matrix, detecting islands,
        and determining the winning island (island with the highest average height). It uses a
        Singleton pattern to ensure only one map instance exists throughout the game.

        Key features:
        - Fetches and processes the map matrix.
        - Detects islands and calculates their average height.
        - Determines and stores the winning island.
        - Caches map matrices and their corresponding winning islands.
        - Handles map restart and regeneration based on difficulty.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Map, cls).__new__(cls, *args, **kwargs)
            cls._instance.islands = []
            cls._instance.cell_size = 0
            cls._instance.matrix = None
            cls._instance.map_path = None
            cls._instance.winning_island = None
            cls._instance.map_dimensions = Dimensions()  # Store map dimensions here
            cls._instance.matrix_winning_island_map = {}  # Hash map to store matrix: winning_island pairs
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.islands = []
            self.cell_size = 0
            self.matrix = None
            self.map_path = None
            self.winning_island = None
            self.map_dimensions = Dimensions()  # Initialize map dimensions
            self.matrix_winning_island_map = {}  # Hash map to store matrix: winning_island pairs
            self.initialized = True
            # Fetch and initialize matrix and related data during construction
            self.set_matrix()

    def restart(self, difficulty = "regular"):
        """
        Reset the Map instance to its initial state and regenerate the map matrix.
        """
        # Reset all attributes to their initial state
        self.islands = []
        self.cell_size = 0
        self.matrix = None
        self.map_path = None
        self.winning_island = None
        self.map_dimensions = Dimensions()
        self.matrix_winning_island_map = {}

        # Fetch a new matrix and reinitialize the map
        print("Restarting the map and regenerating data...")
        self.set_matrix(difficulty)

        # Log success
        print("Map has been successfully restarted.")

    def set_matrix(self,  difficulty="regular", matrix=None):
        """
        Sets the map's matrix and updates the islands.
        If no matrix is provided, fetches a new one.
        """
        if matrix is None:
            matrix = MapService().get_map_matrix()  # Fetch the matrix using MapService
            if matrix is None:
                raise Exception("Failed to fetch map matrix.")

        # Convert the matrix to a hashable tuple of tuples
        matrix_key = self.matrix_to_tuple(matrix)

        # Check if the matrix is already in the hash map
        if matrix_key in self.matrix_winning_island_map:
            # If the matrix exists in the hash map, retrieve the winning island from the map
            self.winning_island = self.matrix_winning_island_map[matrix_key]
            print(f"Found matrix in cache, using existing winning island: {self.winning_island}")
        else:
            # If the matrix is not in the cache, process it
            self.matrix = matrix
            # Update the islands based on the matrix
            self.update_islands()
            # Generate the map image and capture the path, width, and height
            self.map_path, width, height = MapService().generate_map_image(self.matrix, difficulty)
            # Calculate the cell size
            self.cell_size = self.calculate_cell_size(width, height)

            # Store the dimensions in the map_dimensions attribute
            self.map_dimensions.width = width
            self.map_dimensions.height = height

            # Precompute the winning island
            self.set_winning_island()

            # Store the matrix and winning island pair in the hash map (dictionary)
            self.matrix_winning_island_map[matrix_key] = self.winning_island
            print(f"Matrix not found in cache, computed and stored new winning island: {self.winning_island}")

    def update_islands(self):
        """Update the islands based on the current matrix."""
        if self.matrix:
            island_detector = IslandDetector()
            # print_matrix(self.matrix)
            detected_islands = island_detector.find_islands(self.matrix)

            # Reset and populate the min-heap
            self.islands = []
            for island_obj in detected_islands:
                # Add the `Island` object to the min-heap using its `avg_height`
                heapq.heappush(self.islands,
                               (-island_obj.avg_height, island_obj))  # Use negative avg_height for max-heap

    def set_winning_island(self):
        """Set the island with the maximum average height."""
        if self.islands:
            # Root of the heap contains the island with the maximum average height
            self.winning_island = self.islands[0][1]
            # print(self.winning_island)

    def matrix_to_tuple(self, matrix):
        """Converts the matrix into a tuple of tuples, which is hashable."""
        return tuple(tuple(row) for row in matrix)

    def get_cell_size(self):
        return self.cell_size

    def get_matrix(self):
        """Get the map matrix."""
        return self.matrix

    def get_islands(self):
        """Return the islands sorted by their average height."""
        # Return a list of Island objects sorted by average height in descending order
        return [island_obj[1] for island_obj in sorted(self.islands, key=lambda x: -x[0])]

    def get_map_path(self):
        """Get the path to the generated map image."""
        return self.map_path

    def get_winning_island(self):
        """Get the island with the maximum average height."""
        return self.winning_island

    def get_map_dimensions(self):
        """Get the dimensions of the generated map (width, height)."""
        return self.map_dimensions

    def calculate_cell_size(self, width, height):
        """
        Calculates the size of each cell in a 30x30 matrix based on the width and height of the map.
        If the width is greater than the height, the size of each cell is based on the width.
        If the height is greater than or equal to the width, the size of each cell is based on the height.

        Args:
            width (int): The width of the generated map.
            height (int): The height of the generated map.

        Returns:
            int: The calculated size of each cell in the matrix.
        """
        # If the width is greater than the height, calculate cell size based on width
        if width > height:
            cell_size = width / 30
        else:
            cell_size = height / 30

        return cell_size

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell).rjust(3, ' ') for cell in row))
