from pprint import pprint
import requests
from map_maker.map_generator import generate_map


class MapService:
    def get_map_matrix(self):
        """
        This method retrieves a map in the form of a 2D matrix from an external URL.

        It sends a GET request to the specified URL, retrieves the map data as a string,
        and then converts the string into a 2D list (matrix) of integers.

        Returns:
            list: A 2D list (matrix) representing the map if the request is successful.
            None: If the request fails or there is an error retrieving the map.

        Example:
            map_matrix = MapService().get_map_matrix()
        """
        # URL to fetch the map from
        url = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"

        # Sending GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Here we get the map as a string
            map_data = response.text

            # Convert the string into a 2D matrix of integers
            map_matrix = [list(map(int, row.split())) for row in map_data.strip().split("\n")]
            # pprint(map_matrix, width=200)
            return map_matrix
        else:
            print(f"Failed to retrieve map. Status code: {response.status_code}")
            return None

    def generate_map_image(self, matrix, difficulty="regular"):
        """
        This method generates and saves a map image based on the given matrix using the
        generate_map function.

        Args:
            matrix (list): A 2D list (matrix) representing the map's layout.
            difficulty (str): The difficulty level for the map (default is "regular").

        Returns:
            str: The file path to the generated map image if the generation is successful.
            None: If the map image generation fails.

        Example:
            map_image_path = MapService().generate_map_image(matrix, "hard")
        """
        # Call generate_map function to generate and save the map image
        map_path = generate_map(matrix, difficulty)

        if map_path is None:
            return None  # Return None if map generation fails

        return map_path
