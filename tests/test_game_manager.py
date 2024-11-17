import unittest
from observers.game_state import Coordinates
from map_maker.island_detector import IslandDetector
from services.api_service import MapService
from game_manager import GameManager


class TestGameManager(unittest.TestCase):

    def test_set_winning_island(self):
        map_service = MapService()
        matrix = map_service.get_map_matrix()

        # Inicijalizuj IslandDetector
        island_detector = IslandDetector(matrix)

        # Inicijalizuj GameManager
        game_manager = GameManager(island_detector)

        # Postavi pobedničko ostrvo
        game_manager.set_winning_island()

        # Provera da li je pobedničko ostrvo postavljeno
        winning_island = game_manager.game_state.winning_island
        print("\nPobedničko ostrvo je postavljeno na koordinate:", winning_island)
        self.assertIsInstance(winning_island, Coordinates)  # Pobedničko ostrvo treba da bude instanca Coordinates
        self.assertGreater(winning_island.x, 0)  # Proveri da li je koordinate validne
        self.assertGreater(winning_island.y, 0)  # Proveri da li je koordinate validne

    def test_get_game_status(self):
        map_service = MapService()
        matrix = map_service.get_map_matrix()

        # Inicijalizuj IslandDetector
        island_detector = IslandDetector(matrix)

        # Inicijalizuj GameManager
        game_manager = GameManager(island_detector)

        # Provera početnog statusa igre
        game_status = game_manager.get_game_status()
        print("\nPočetni status igre:", game_status)
        self.assertEqual(game_status, "in_progress")  # Početni status treba biti "in_progress"

    def test_check_guess(self):
        map_service = MapService()
        matrix = map_service.get_map_matrix()

        # Inicijalizuj IslandDetector
        island_detector = IslandDetector(matrix)

        # Inicijalizuj GameManager
        game_manager = GameManager(island_detector)

        # Postavi pobedničko ostrvo
        game_manager.set_winning_island()

        # Postavi selektovano ostrvo kao pogodjeno
        game_manager.game_state.selected_island = game_manager.game_state.winning_island

        # Provera da li je guess tačan
        result = game_manager.check_guess()
        print("\nRezultat provere pokušaja:", result)
        self.assertEqual(result["result"], "correct")  # Ako je guess tačan, rezultat treba biti "correct"

    def test_reset_game(self):
        map_service = MapService()
        matrix = map_service.get_map_matrix()

        # Inicijalizuj IslandDetector
        island_detector = IslandDetector(matrix)

        # Inicijalizuj GameManager
        game_manager = GameManager(island_detector)

        # Postavi pobedničko ostrvo
        game_manager.set_winning_island()

        # Resetovanje igre
        game_manager.reset_game()

        # Provera da li je stanje igre resetovano
        game_status = game_manager.get_game_status()
        print("\nStatus igre nakon reseta:", game_status)
        self.assertEqual(game_status, "in_progress")  # Status treba biti "in_progress" nakon reseta

    def test_print_matrix(self):
        map_service = MapService()
        matrix = map_service.get_map_matrix()

        print("\nPrikaz matrice:")
        self.print_matrix(matrix)

    def print_matrix(self, matrix):
        for row in matrix:
            print(" ".join(str(cell).rjust(3, ' ') for cell in row))


if __name__ == '__main__':
    unittest.main()
