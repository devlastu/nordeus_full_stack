from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routes.game_routes import router as game_router  # Import rute

app = FastAPI()
MAP_PATH = ''
# Montiraj statičke fajlove
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")  # za frontend statičke fajlove
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")  # za statičke fajlove kao što su CSS, JS, slike
app.mount("/frontend/static/maps", StaticFiles(directory="frontend/static/maps"), name="maps")  # za slike mape
# Dodavanje game_routes u glavnu aplikaciju
app.include_router(game_router, prefix="", tags=[""])