# nordeus_full_stack
# Island Height Guessing Game: Island Game🌊🏝️

Welcome to the **Island Game**, a fun and interactive game where players guess which island has the highest average height on a 30x30 grid! Test your intuition and strategic thinking to identify the tallest island before you run out of attempts.

## Features
- 🗺️ **Interactive Map**: Click on the map to select your guess coordinates.
- 🎯 **Limited Attempts**: Players have different amount of attempts(depending on difficulty level) to identify the island with the greatest average height.
- 🔄 **Dynamic Difficulty Levels**: Choose from *easy*, *regular*, *intermediate*, *hard*, or *master* modes.
- 📊 **Score Tracking**: Keep track of your attempts and scores throughout the game.
- 🔥 **Immersive Feedback**: Enjoy vibrant animations and feedback based on your gameplay results.
- 🚀 **Responsive Design**: Play on both desktop and mobile devices.

## How to Play
1. Open the game in your browser.
2. Click on the map to select the coordinates of your guess.
3. Hit the **Submit Guess** button to make your choice.
4. The game will provide feedback, including your remaining attempts.
5. Win by correctly identifying the island with the highest average height. Lose if you run out of attempts.

## Difficulty Levels
Each difficulty level adjusts the number of attempts and gameplay intensity:
- **Easy**: 5 attempts
- **Regular**: 3 attempts
- **Intermediate**: 2 attempts
- **Hard**: 2 attempts, blured map
- **Master**: 1 attempt, more blured map

## Project Structure

## nordeus_full_stack
- **main.py**: Main entry point for the application
- **game_manager.py**: Manages the game logic and state

### /tests/
- **test_game_manager.py**: Tests for the game manager logic

### /services/
- **api_service.py**: Handles API calls for the game

### /routes/
- **game_routes.py**: Defines routes for game actions

### /observers/ (part of future upgrades)
- **game_observer.py**: Observer class for game state changes
- **game_state.py**: Game state management
- **publisher.py**: Manages subscribing and notifying observers

### /models/
- **coordinates.py**: Coordinates model for game grid
- **map.py**: Map model for the game grid and terrain
- **island.py**: Island model representing a set of land cells

### /map_maker/
- **island_detector.py**: Detects and identifies islands on the map
- **map_generator.py**: Generates the game map with heights

### /frontend/
- **/static/**: Static files (images, maps, etc.)
- **index.html**: HTML file for rendering the game

- **requirements.txt**: List of project dependencies
- **app.py**: Main entry point for the backend (Flask/FastAPI)
- **README.md**: Project documentation


### Explanation of the Project Structure:

- **main.py & game_manager.py**: The core logic of the game, including managing the state and flow.
- **tests**: Tests for critical components like the game manager. (Utilized in the early state of developing)
- **services**: Defines the backend services like API routes for the game. (Spesificially for getting random test matrix)
- **routes**: Manages backend routing for different game actions.
- **observer**: Implements the observer pattern to update game state and notify subscribers (observers). (For future upgrades)
- **models**: Contains the game's data models (coordinates, islands, maps).
- **map_maker**: Responsible for generating the map and detecting islands.
- **frontend**: The frontend static files and HTML for rendering the game UI.


## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/island-height-guessing-game.git

2. Navigate to the project directory:
   ```bash
   cd nordeus_full_stack

3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv

4. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate

5. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Run the application(this covers for command line, but you can setup fastApi run configuration):
   ```bash
   uvicorn app:app --reload

7. Access the game:
   Open your browser and navigate to http://127.0.0.1:8000 (or another port if specified by your framework) to start playing the Island Height Guessing Game.




## Dependencies
This project requires the following Python packages:

- **fastapi**: The FastAPI framework for building APIs.
- **uvicorn**: ASGI server for running the FastAPI application.
- **numpy**: A core library for numerical computing.
- **Pillow**: Python Imaging Library (PIL) for handling images.
- **matplotlib**: A library for creating visualizations and plots.
- **scipy**: A library for scientific computing, including `gaussian_filter`.
- **starlette**: A toolkit for building web applications, which is a dependency of FastAPI for handling static files.
