from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse, HTMLResponse
from game_manager import GameManager
from models.game_state import GameState, Coordinates
from services.api_service import MapService

router = APIRouter()

# Initialize services and manager
game_manager = GameManager()
map_service = MapService()

@router.get("/", response_class=HTMLResponse)
async def index():
    # Početna stranica sa dugmetom Play
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@router.get("/game", response_class=HTMLResponse)
async def game():
    # Stranica koja prikazuje mapu
    with open("frontend/game.html", "r") as f:
        return HTMLResponse(content=f.read())

@router.get("/get-map")
async def get_map():
    """
    Ova ruta generiše mapu i vraća je kao PNG fajl.
    """
    # Generiši matricu mape
    matrix = map_service.get_map_matrix()

    if matrix is None:
        return {"message": "Failed to generate map."}

    # Generiši sliku mape koristeći matricu
    map_path = map_service.generate_map_image(matrix)

    if map_path is None:
        return {"message": "Failed to generate map image."}

    # Vraćanje mape kao odgovor
    return FileResponse(map_path, media_type="image/png")




@router.post("/make-guess")
async def make_guess(guess: Coordinates):
    """
    Ruta za unos korisničke pretpostavke.
    Na osnovu unetih podataka, proverava da li je pretpostavka tačna
    i vraća rezultat.
    """
    print(f"Received guess: {guess}")  # Ispisivanje podataka za debugging
    # game_state = GameState()
    # Provera da li su koordinate validne
    if not isinstance(guess.x, (int, float)) or not isinstance(guess.y, (int, float)):
        raise HTTPException(status_code=422, detail="Invalid coordinates.")

    result = {
        "status": "success",
        "message": "Bravo, pogodili ste tačne koordinate!"
    }
    return result
