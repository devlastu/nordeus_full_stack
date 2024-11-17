from pprint import pprint

import requests


from map_maker.map_generator import generate_map


class MapService:
    def get_map_matrix(self):
        # URL sa koga ćemo povući mapu
        url = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"

        # Slanje GET zahteva na URL
        response = requests.get(url)

        # Provera da li je zahtev uspešan
        if response.status_code == 200:
            # Ovdje dobijamo mapu u formi stringa
            map_data = response.text

            # Pretvaranje stringa u 2D matricu
            map_matrix = [list(map(int, row.split())) for row in map_data.strip().split("\n")]
            # pprint(map_matrix, width=200)
            return map_matrix
        else:
            print(f"Failed to retrieve map. Status code: {response.status_code}")
            return None

    def generate_map_image(self, matrix):
        """
        This method will call the generate_map function
        to generate and save the map image based on the matrix.
        """
        # Call generate_map function to generate and save the map
        map_path = generate_map(matrix)

        if map_path is None:
            return None  # Return None if map generation fails

        return map_path