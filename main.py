from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routes.game_routes import router as game_router  # Import routes

# Create the FastAPI application instance
app = FastAPI()

# Path for storing map data (to be configured later)
MAP_PATH = ''

# Mount static files for frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")  # Static files for frontend
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")  # Static files like CSS, JS, images
app.mount("/frontend/static/maps", StaticFiles(directory="frontend/static/maps"), name="maps")  # For map images

# Include the game-related routes into the main app
app.include_router(game_router, prefix="", tags=[""])

# Entry point of the application
# This section initializes the FastAPI app and mounts the necessary static files.
# It also includes routes from 'game_routes' to handle the game logic.
