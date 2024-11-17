from typing import Optional, List
from pydantic import BaseModel, Field
from models.coordinates import Coordinates
from models.island import Island
from observers.publisher import Publisher  # Make sure to import Publisher

missed_msg = "Not correct guess this time. Wish you more luck next time!!!"
guessed_msg = "Congratulations!! You've guessed it!!"

class GameState(BaseModel):
    selected_island: Optional[Coordinates] = None
    attempts: int = 0
    correct_attempts: int = 0
    incorrect_attempts: int = 0
    result: Optional[str] = None
    game_status: str = "in_progress"
    winning_island: Optional[Island] = None
    num_of_lives: int = 3  # Number of remaining lives based on difficulty
    attempts_history: List[Coordinates] = Field(default_factory=list)  # History of attempts

    publisher: Publisher = Publisher()  # The GameState now knows only about the Publisher

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types

    def record_attempt(self, guess: Coordinates, cell_size: float):
        """
        Record a player's attempt and update the game state.

        Parameters:
            guess (Coordinates): The guessed coordinates.
            cell_size (float): The size of a single cell in the map grid.
        """
        is_correct = False

        if self.winning_island:
            # Scale the guess as specified
            scaled_x = int((30 * guess.x) / 600)
            scaled_y = int((30 * guess.y) / 600)

            print(self.winning_island.coordinates)
            print(f"X: {scaled_x}, Y: {scaled_y}")


            # Extract x and y coordinates from the winning island's coordinates
            x_coords = {coord[0] for coord in self.winning_island.coordinates}
            y_coords = {coord[1] for coord in self.winning_island.coordinates}
            print(f"X coords: {x_coords} and Y coords: {y_coords}")


            # Check if scaled_x is in x_coords and scaled_y is in y_coords
            is_correct = scaled_x in x_coords and scaled_y in y_coords
            print(f"{scaled_x in x_coords}, {scaled_y in y_coords}")

        # Record the result of the guess
        self.result = missed_msg
        self.attempts_history.append(guess)
        self.attempts += 1
        self.num_of_lives -= 1
        print("decremented")
        # Check if the number of remaining lives is less than the incorrect attempts
        if self.num_of_lives < 0:
            # If number of lives is zero or negative and there have been incorrect attempts,
            # the game should end with a loss
            self.result = missed_msg
            self.game_status = "finished_lose"
            self.incorrect_attempts += 1
        elif is_correct:
            self.result = guessed_msg
            self.game_status = "finished_win"
            self.correct_attempts += 1
        else:
            # Decrease lives on incorrect guess
            self.result = missed_msg
            self.game_status = "in_progress"
            self.incorrect_attempts += 1

            # After each incorrect guess, check if we should finish the game
            if self.num_of_lives <= 0:
                self.game_status = "finished_lose"

        # Notify publisher after each update
        self.publisher.notify(
            game_status=self.game_status,
            total_attempts=self.attempts,
            correct_attempts=self.correct_attempts,
            incorrect_attempts=self.incorrect_attempts,
            result=self.result,
            remaining_attempts=self.num_of_lives,  # Remaining lives (not max attempts)
            winning_island_coordinates=(
                self.winning_island.coordinates
            ) if self.winning_island else None
        )

    def set_winning_island(self, island: Island):
        """Set the winning island."""
        self.winning_island = island
        self.publisher.notify(
            game_status=self.game_status,
            total_attempts=self.attempts,
            correct_attempts=self.correct_attempts,
            incorrect_attempts=self.incorrect_attempts,
            result=self.result,
            remaining_attempts=self.num_of_lives,
            winning_island_coordinates=self.winning_island.coordinates
        )

    def set_selected_island(self, island: Coordinates, cell_size: float):
        """Set the selected island and record the attempt."""
        self.selected_island = island
        self.record_attempt(island, cell_size)

    def get_result(self):
        """Get the result of the attempt checking."""
        return self.result

    def initialize(self, num_of_lives: int = 3):
        """Reinitialize game state with the given number of lives."""
        self.num_of_lives = num_of_lives
        self.attempts = 0
        self.correct_attempts = 0
        self.incorrect_attempts = 0
        self.result = None
        self.game_status = "in_progress"
        self.attempts_history.clear()

    def restart(self, num_of_lives: int = 3):
        """
        Reset the game state to its initial configuration.

        Parameters:
            num_of_lives (int): The number of lives to start with (default: 3).
        """
        self.selected_island = None
        self.attempts = 0
        self.correct_attempts = 0
        self.incorrect_attempts = 0
        self.result = None
        self.game_status = "in_progress"
        self.winning_island = None
        self.num_of_lives = num_of_lives
        self.attempts_history.clear()


        # Notify observers that the game state has been reset
        self.publisher.notify(
            game_status=self.game_status,
            total_attempts=self.attempts,
            correct_attempts=self.correct_attempts,
            incorrect_attempts=self.incorrect_attempts,
            result=self.result,
            remaining_attempts=self.num_of_lives,
            winning_island_coordinates=None
        )

    def set_num_of_lives(self, num_of_lives: int):
        self.num_of_lives = num_of_lives