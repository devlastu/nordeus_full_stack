from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from starlette.responses import FileResponse, HTMLResponse
from game_manager import GameManager
from observers.game_state import Coordinates

router = APIRouter()
GAME_MANAGER = GameManager()  # Create a fresh game_manager instance



# Difficulty mapping from number to string
difficulty_map = {
    "1": "easy",          # 1 maps to "easy"
    "2": "regular",       # 2 maps to "regular"
    "3": "intermediate",  # 3 maps to "intermediate"
    "4": "hard",          # 4 maps to "hard"
    "5": "master"         # 5 maps to "master"
}

@router.get("/", response_class=HTMLResponse)
async def index():
    """Serves the home page with a 'Play' button."""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@router.get("/index", response_class=HTMLResponse)
async def index():
    """Serves the home page with a 'Play' button."""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@router.get("/game", response_class=HTMLResponse)
async def game():
    """Serves the game page that displays the map."""
    global GAME_MANAGER


    # Initialize the game_manager instance
    GAME_MANAGER.set_matrix(GAME_MANAGER.get_matrix())

    # Read the HTML file
    with open("frontend/index.html", "r") as f:
        html_content = f.read()

    # Replace the placeholder with the actual attempts_left value
    html_content = html_content.replace('id="attempts-left-text"></span>',
                                        f'id="attempts-left-text">{GAME_MANAGER.num_of_lives}</span>')

    # Return the modified HTML content with the injected attempts_left value
    return HTMLResponse(content=html_content)

@router.get("/get-map")
async def get_map():
    global GAME_MANAGER
    """
    This route generates the map and returns it as a PNG file.
    Delegate map handling to game_manager, and use Map class to get the map image.
    """

    map_image = GAME_MANAGER.get_map_image()  # Assume this method handles getting the map image

    if not map_image:
        raise HTTPException(status_code=500, detail="Failed to generate map image.")

    return FileResponse(map_image, media_type="image/png")


@router.post("/make-guess")
async def make_guess(guess: Coordinates):
    """
    Endpoint for handling user guesses. It checks whether the guess is correct
    and returns the result of the guess along with the game status.

    Args:
        guess (Coordinates): The user's guess containing the coordinates to check.

    Returns:
        dict: A dictionary containing the result message and the game status.
            - "finished_win" if the game is won.
            - "finished_lose" if the game is lost.
            - "in_progress" if the game is still ongoing.

    Raises:
        HTTPException: If the guess is invalid or the game state is incorrect.
    """
    # Debugging: print received guess
    print(f"Received guess: {guess}")

    # Call the check_guess method from GameManager to check the guess
    result = GAME_MANAGER.check_guess(guess)
    print(result)
    print(f"{result['attempts_left']}")  # Display attempts left for debugging

    # Handle invalid guess or game state
    if result is None:
        raise HTTPException(status_code=400, detail="Invalid guess or game state.")

    # Prepare the response based on the game status
    game_status = GAME_MANAGER.game_state.game_status
    result_message = ""

    if game_status == "finished_win":
        result_message = "Well done, you've won!"
        return {
            "status": "finished_win",
            "message": result_message
        }
    elif game_status == "finished_lose":
        result_message = "Unfortunately, the game is over."
        return {
            "status": "finished_lose",
            "message": result_message,
            "attempts_left": 0  # No attempts left if the game is lost
        }
    elif game_status == "in_progress":
        result_message = "Keep trying! You still have a chance!" if GAME_MANAGER.game_state.result != "correct" else "Bravo, you've guessed the correct coordinates!"
        return {
            "status": "in_progress",
            "message": result_message,
            "attempts_left": result["attempts_left"]  # Return attempts left
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid game status.")


class DifficultyRequest(BaseModel):
    difficulty: str


@router.post("/change-difficulty")
async def change_difficulty(request: DifficultyRequest):
    """
    Endpoint for changing the difficulty level of the game.

    Args:
        request (DifficultyRequest): The request containing the new difficulty level.

    Returns:
        dict: A dictionary containing a success message with the new difficulty level.

    Raises:
        HTTPException: If the provided difficulty level is invalid.
    """
    difficulty = request.difficulty
    print(f"Received difficulty: {difficulty}")  # Log the received difficulty level

    global GAME_MANAGER

    # Check if the provided difficulty level is valid
    if difficulty not in GAME_MANAGER.difficulty_levels:
        raise HTTPException(status_code=400, detail="Invalid difficulty level")

    # Set the new difficulty level in the GameManager
    GAME_MANAGER.set_difficulty(difficulty)
    return {"message": f"Difficulty level set to {difficulty}"}


@router.post("/restart")
async def restart_game(request: DifficultyRequest):
    """
    Endpoint to restart the game.
    This will reset the game state like attempts left, game status, and selected coordinates.
    """
    try:
        difficulty = request.difficulty
        if difficulty not in GAME_MANAGER.difficulty_levels:
            raise HTTPException(status_code=400, detail="Invalid difficulty level")
        GAME_MANAGER.set_difficulty(difficulty)  # Reset the game state
        return {"message": "Game restarted successfully!", "attempts_left": GAME_MANAGER.num_of_lives}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))