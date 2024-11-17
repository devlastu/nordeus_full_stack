from abc import ABC, abstractmethod

class GameStateObserver(ABC):
    """
    Interface for observers that track changes in the game's state.
    The observer should receive the necessary data when notified,
    rather than having direct knowledge of the GameState.
    """

    @abstractmethod
    def update(self, **kwargs):
        """Method that is called when the game state changes."""
        pass


class GameStatusObserver(GameStateObserver):
    """
    Observer that tracks only the game's status (whether it is finished or ongoing).
    """

    def update(self, **kwargs):
        game_status = kwargs.get('game_status')
        if game_status == "finished":
            print("The game has finished.")
        else:
            print("The game is still in progress.")
        print(f"Current game status: {game_status}")


class AttemptObserver(GameStateObserver):
    """
    Observer that tracks the number of attempts and their results.
    """

    def update(self, **kwargs):
        total_attempts = kwargs.get('total_attempts')
        correct_attempts = kwargs.get('correct_attempts')
        incorrect_attempts = kwargs.get('incorrect_attempts')
        result = kwargs.get('result')
        remaining_attempts = kwargs.get('remaining_attempts')

        print(f"\n--- Attempt Update ---")
        print(f"Total attempts made: {total_attempts}")
        print(f"Correct attempts: {correct_attempts}")
        print(f"Incorrect attempts: {incorrect_attempts}")
        print(f"Result of the last attempt: {result}")
        print(f"Remaining attempts: {remaining_attempts}")


class WinningIslandObserver(GameStateObserver):
    """
    Observer that tracks the winning island.
    """

    def update(self, **kwargs):
        winning_island_coordinates = kwargs.get('winning_island_coordinates')

        if winning_island_coordinates:
            print(f"\n--- Winning Island Update ---")
            print(f"The winning island is at coordinates: "
                  f"({winning_island_coordinates[0]}, {winning_island_coordinates[1]})")
        else:
            print("\n--- Winning Island Update ---")
            print("The winning island has not been set yet.")
