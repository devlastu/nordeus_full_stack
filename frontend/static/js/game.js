// Initialize variables to store coordinates
let selectedCoords = null;
let originalWidth, originalHeight;

// When the window loads, store the original image dimensions in localStorage
window.onload = function() {
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
                backdropText = `
                    rgba(253, 227, 167, 0.4)
                    url("/frontend/static/images/well_done.webp")
                    left top
                    no-repeat
                `;
            } else if (result.status === "finished_lose") {
                alertTitle = "Game Over! You lost. Try again!";
                alertColor = "red";
                backdropText = `
                    rgba(189, 195, 199, 0.4)
                    url("/frontend/static/images/sad.webp")
                    left top
                    no-repeat
                `;
            } else if (result.status === "in_progress") {
                alertTitle = result.message || "Keep trying! You still have a chance!";
                alertColor = "black";
                backdropText = `
                    rgba(205, 209, 228, 0.4)
                    url("/frontend/static/images/no_surrender.webp")
                    left top
                    no-repeat
                `;
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
                console.log(result.attempts_left);
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
                backdrop: `
                    rgba(0,0,123,0.4)
                    url("/images/nyan-cat.gif")
                    left top
                    no-repeat
                `,
            });

            // Reset the result text
            document.getElementById("result-text").innerText = "An error occurred while processing the request.";
            document.getElementById("result-text").style.color = "red";
        });
});

// New function to ask the user if they want to play again
function showPlayAgainPrompt() {
    Swal.fire({
        title: "Do you want to play again?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
    }).then((response) => {
        if (response.isConfirmed) {
            // User wants to play again, reset the game (you can implement this reset logic here)
            console.log("Starting a new game...");
            // Example: Reload the page to restart the game
            window.location.reload();  // Or implement specific game reset logic
        } else {
            console.log("Game over, user doesn't want to play again.");
        }
    });
}




