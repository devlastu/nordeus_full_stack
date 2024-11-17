// Initialize variables to store coordinates and difficulty settings
let selectedCoords = null;
let originalWidth, originalHeight;
let attemptsLeft = 3;
let currentDifficulty = "regular";



// // Update the number of lives based on the selected difficulty
// localStorage.setItem('attempts-left', attemptsLeft);
// document.getElementById("attempts-left-text").innerText = parseInt(localStorage.getItem("attempts-left"), 10);
//
// localStorage.setItem('currentDifficulty', currentDifficulty);
// document.getElementById("currentDifficulty").innerText = localStorage.getItem("currentDifficulty");

// When the window loads, store the original image dimensions in localStorage
window.onload = function() {

    document.getElementById("currentDifficulty").innerText = localStorage.getItem("currentDifficulty");
    document.getElementById("attempts-left-text").innerText = parseInt(localStorage.getItem("attempts-left"), 10);

    // Remove any previously stored dimensions from localStorage
    localStorage.removeItem('originalWidth');
    localStorage.removeItem('originalHeight');

    const img = document.getElementById('map');

    // Check if image dimensions already exist in localStorage
    if (!localStorage.getItem('originalWidth') || !localStorage.getItem('originalHeight')) {
        // Get the original dimensions of the image
        originalWidth = img.naturalWidth;
        originalHeight = img.naturalHeight;

        // Save the image dimensions to localStorage
        localStorage.setItem('originalWidth', originalWidth);
        localStorage.setItem('originalHeight', originalHeight);
    } else {
        // If dimensions are already stored in localStorage, retrieve them
        originalWidth = parseFloat(localStorage.getItem('originalWidth'));
        originalHeight = parseFloat(localStorage.getItem('originalHeight'));
    }
};

// Initialize variables for integer coordinates (defaults to 0)
const intX = 0; // Use Math.round() if you want to round to the nearest integer
const intY = 0;

// Add event listener for clicks on the map
document.getElementById("map").addEventListener("click", function(event) {
    // Get the clicked position on the map
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left; // X-coordinate relative to the image
    const y = event.clientY - rect.top;  // Y-coordinate relative to the image

    // Scale the clicked coordinates from the resized image to the original image dimensions
    const scaledX = (x / rect.width) * originalWidth;
    const scaledY = (y / rect.height) * originalHeight;

    // Convert scaled coordinates to integer values
    const intX = Math.floor(scaledX); // Use Math.round() for rounding
    const intY = Math.floor(scaledY);

    // Display the clicked coordinates on the screen
    document.getElementById("coord-text").innerText = `X: ${scaledX.toFixed(2)}, Y: ${scaledY.toFixed(2)}`;

    // Save the selected coordinates
    // We need to invert them because of backend
    selectedCoords = { x: intY, y: intX };
});

// Handle the submission of coordinates
document.getElementById("send-coordinates").addEventListener("click", function() {
    // Check if coordinates have been selected
    if (!selectedCoords) {
        alert("Please click on the map to select coordinates first.");
        return;
    }

    // Send the selected coordinates to the server via POST request
    axios.post("/make-guess", selectedCoords)
        .then(response => {
            const result = response.data;

            // Log the result and result.status for debugging
            console.log("Result:", result);
            console.log("Result Status:", result.status);

            // Determine the appropriate color based on the game status
            let alertColor = "#716add"; // Default color
            let alertTitle = result.message;
            let backdropText = ""; // Initialize backdrop text

            // Define the SweetAlert title and color based on the result status
            if (result.status === "finished_win") {
                alertTitle = "Congratulations! You guessed correctly!";
                alertColor = "green";
                backdropText = `rgba(253, 227, 167, 0.4) url("/frontend/static/images/well_done.webp") left top no-repeat`;
            } else if (result.status === "finished_lose") {
                alertTitle = "Game Over! You lost. Try again!";
                alertColor = "red";
                backdropText = `rgba(189, 195, 199, 0.4) url("/frontend/static/images/sad.webp") left top no-repeat`;
            } else if (result.status === "in_progress") {
                alertTitle = result.message || "Keep trying! You still have a chance!";
                alertColor = "black";
                backdropText = `rgba(205, 209, 228, 0.4) url("/frontend/static/images/no_surrender.webp") left top no-repeat`;
            } else {
                alertTitle = "Unexpected status from server.";
                alertColor = "red";
            }

            // Show the SweetAlert popup with custom styling
            Swal.fire({
                title: alertTitle,
                width: 600,
                padding: "3em",
                color: alertColor,
                background: "#fff url(/images/trees.png)",  // Custom background image
                backdrop: backdropText,
            }).then(() => {
                // After the first alert, if the game is finished, ask to play again
                if (result.status === "finished_win" || result.status === "finished_lose") {
                    showPlayAgainPrompt(); // Call function to ask if the user wants to play again
                }
            });

            // Update attempts left if available
            if (result.attempts_left !== undefined) {
                document.getElementById("attempts-left-text").innerText = result.attempts_left; // Update the attempts left text
            }

            // Reset selected coordinates after the response
            selectedCoords = null;
            console.log("Selected coordinates cleared:", selectedCoords);

        })
        .catch(error => {
            // Handle any errors from the server request
            console.error("There was an error!", error);

            // Show SweetAlert with error message
            Swal.fire({
                title: "An error occurred!",
                text: "There was an issue processing your request. Please try again.",
                icon: "error",
                width: 600,
                padding: "3em",
                color: "red",
                background: "#fff url(/images/trees.png)",  // Custom background image
                backdrop: `rgba(0,0,123,0.4) url("/images/nyan-cat.gif") left top no-repeat`,
            });

            // Reset the result text
            document.getElementById("result-text").innerText = "An error occurred while processing the request.";
            document.getElementById("result-text").style.color = "red";
        });
});

// New function to ask the user if they want to play again
function showPlayAgainPrompt() {
    difficultyLevel = localStorage.getItem("currentDifficulty")
    Swal.fire({
        title: "Do you want to play again?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
    }).then((response) => {
        if (response.isConfirmed) {
            // User wants to play again, send the restart request to the server
            axios.post('/restart', { difficulty: difficultyLevel })
                .then(res => {
                    console.log("Server response after restart:", res.data);
                    // Reset game logic or reload the page after successful restart
                    window.location.reload();  // Reload the page to restart the game
                })
                .catch(error => {
                    console.error("There was an error restarting the game:", error);
                    Swal.fire({
                        title: "Error",
                        text: "There was an issue restarting the game. Please try again.",
                        icon: "error",
                    });
                });
        } else {
            axios.post('/restart', { difficulty: 'regular' })
                .then(res => {
                    console.log("Server response after restart:", res.data);
                    // Reset game logic or reload the page after successful restart
                    window.location.href = 'index';    // Reload the page to restart the game
                })
                .catch(error => {
                    console.error("There was an error restarting the game:", error);
                    Swal.fire({
                        title: "Error",
                        text: "There was an issue restarting the game. Please try again.",
                        icon: "error",
                    });
                });
        }
    });
}

// Initialize Bootstrap Modal functionality
document.getElementById('about-info-btn').addEventListener('click', function() {
    var modal = new bootstrap.Modal(document.getElementById('aboutInfoModal'));
    modal.show();
});

// Difficulty Map and Attempts Left Logic
const difficultyMap = {
    "1": "easy",
    "2": "regular",
    "3": "intermediate",
    "4": "hard",
    "5": "master"
};

const attemptsLeftMap = {
    "easy": "5",
    "regular": "3",
    "intermediate": "2",
    "hard": "2",
    "master": "1"
};

// Function to get the number of attempts based on the difficulty string
function getAttemptsLeft(difficulty) {
    return attemptsLeftMap[difficulty] || "Invalid difficulty"; // Default message if difficulty is not found
}

// Get all difficulty buttons (those with class 'social-icon-item')
const difficultyButtons = document.querySelectorAll('.social-icon-item button');
difficultyButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        // Get the difficulty level number from the data-difficulty attribute
        const difficultyNumber = event.target.getAttribute('data-difficulty');  // "1", "2", etc.

        // Map the number to the corresponding difficulty string
        const difficultyLevel = difficultyMap[difficultyNumber];

        if (difficultyLevel) {
            // Update the active difficulty button
            difficultyButtons.forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');  // Highlight the selected button

            // Update attempts based on difficulty level
            attemptsLeft = getAttemptsLeft(difficultyLevel);


            // Send the updated difficulty to the server
            axios.post('/change-difficulty', { difficulty: difficultyLevel })
                .then(response => {
                    // Update the difficulty in localStorage
                    localStorage.setItem('currentDifficulty', difficultyLevel);
                    localStorage.setItem('attempts-left', attemptsLeft);


                    console.log('Difficulty level changed successfully:', response.data);
                    // Reload the page to apply the changes
                    window.location.reload();
                })
                .catch(error => {
                    console.error('Error changing difficulty level:', error);
                });
        } else {
            console.error('Invalid difficulty level');
        }
    });
});
