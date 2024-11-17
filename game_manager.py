from observers.game_state import GameState
from models.map import Map


class GameManager:
    def __init__(self, difficulty="regular"):
        """
            Initializes the GameManager with the given difficulty level.

            Args:
                difficulty (str): The difficulty level for the game (default is "regular").
        """
        self.difficulty_levels = {
            "easy": 5,
            "regular": 3,
            "intermediate": 2,
            "hard": 2,
            "master": 1
        }

        self.num_of_lives = self.difficulty_levels.get(difficulty, 3)  # Default to regular if difficulty is unknown
        self.map = Map()  # Use the Singleton instance of Map
        self.game_state = GameState()
        self.game_state.num_of_lives = self.num_of_lives# Pass num_of_lives to the GameState
        self.set_winning_island()
        self.difficulty = difficulty

    def get_map(self):
        """Return the map image from MapService."""
        return self.map.get_matrix()

    def get_matrix(self):
        """Return the matrix of the map."""
        return self.map.get_matrix()

    def set_matrix(self, matrix):
        """Set the new matrix for the map."""
        self.map.set_matrix(matrix)

    def get_map_image(self):
        return self.map.get_map_path()

    def check_guess(self, coordinates):
        """
            Check the player's guess and update the game state based on the selected coordinates.

            Args:
                coordinates (tuple): The coordinates of the guessed island (x, y).

            Returns:
                dict: A dictionary containing the result of the guess and the remaining attempts.
        """
        self.game_state.set_selected_island(coordinates, cell_size=self.map.cell_size)
        return {"result": self.game_state.get_result(), "attempts_left": self.game_state.num_of_lives}

    def get_island_data(self):
        """Get island data using IslandDetector."""
        return self.map.get_islands()  # Uses the Map's island detection

    def set_winning_island(self):
        """Set the winning island."""
        winning_island = self.map.get_winning_island()  # Directly fetch the winning island
        if winning_island:
            self.game_state.winning_island = winning_island

    def get_winning_island(self):
        return self.game_state.winning_island

    def get_game_status(self):
        """Return the current status of the game."""
        return self.game_state.game_status

    def reset_game(self, difficulty="regular"):
        """Reset the game state to start over."""
        self.map.restart(difficulty)  # Reset the map (singleton will reinitialize)
        self.num_of_lives = self.difficulty_levels.get(difficulty, 3)
        # print(f"Num of lives: {self.num_of_lives}")
        self.game_state.restart(self.num_of_lives)
        self.set_winning_island()


    def get_levels(self):
        return self.difficulty_levels

    def set_difficulty(self, difficulty: str):
        """
        Sets the game's difficulty.
        """
        self.difficulty = difficulty
        # print(difficulty)
        self.reset_game(difficulty)

        # Adjust other game parameters based on the difficulty
        # self.adjust_game_parameters()


# Helper functions for testing purposes
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell).rjust(3, ' ') for cell in row))

def print_matrix_map(matrix):
    for row in matrix:
        print(" ".join("1" if cell > 0 else "0" for cell in row))


def test_game_manager():
    game_manager = GameManager()  # Initialize the GameManager


    # Set the winning island
    game_manager.set_winning_island()  # Set the winning island based on max height

    winning_island = game_manager.game_state.winning_island

    print(winning_island)

    # Simulate a guess attempt
    result = game_manager.check_guess()  # This will simulate a guess attempt
    print(f"\nRezultat pokušaja: {result['result']}, Broj pokušaja: {result['attempts']}")

# # Run the test
# test_game_manager()

