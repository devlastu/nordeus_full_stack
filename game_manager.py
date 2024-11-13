from models.game_state import GameState, Coordinates


class GameManager:

    def check_guess(self, guess: Coordinates, game_state: GameState):
        # Logika za proveru korisničkog unosa
        correct = game_state.selected_island == guess
        if correct:
            game_state.attempts += 1
            return {"result": "correct", "attempts": game_state.attempts}
        else:
            game_state.attempts += 1
            return {"result": "incorrect", "attempts": game_state.attempts}