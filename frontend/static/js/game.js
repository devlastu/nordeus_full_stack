// Inicijalizuj varijable koje će čuvati koordinate
let selectedCoords = null;
let originalWidth, originalHeight;

// Kada se slika učita, sačuvaj originalne dimenzije u localStorage
window.onload = function() {
    const img = document.getElementById('map');

    // Proveri da li dimenzije slike već postoje u localStorage
    if (!localStorage.getItem('originalWidth') || !localStorage.getItem('originalHeight')) {
        originalWidth = img.naturalWidth;
        originalHeight = img.naturalHeight;

        // Spremi dimenzije slike u localStorage
        localStorage.setItem('originalWidth', originalWidth);
        localStorage.setItem('originalHeight', originalHeight);
    } else {
        // Ako su dimenzije već sačuvane u localStorage, učitaj ih
        originalWidth = parseFloat(localStorage.getItem('originalWidth'));
        originalHeight = parseFloat(localStorage.getItem('originalHeight'));
    }
};

document.getElementById("map").addEventListener("click", function(event) {
    // Pronađi koordinate kliknutog mesta na mapi
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Skaliraj koordinate sa smanjene slike na originalnu sliku
    const scaledX = (x / rect.width) * originalWidth;
    const scaledY = (y / rect.height) * originalHeight;


    // Prikazivanje koordinata na ekranu
    document.getElementById("coord-text").innerText = `X: ${scaledX.toFixed(2)}, Y: ${scaledY.toFixed(2)}`;

    // Spremi koordinate
    selectedCoords = { x: scaledX, y: scaledY };
});

document.getElementById("send-coordinates").addEventListener("click", function() {
    // Proveri da li su koordinate selektovane
    if (!selectedCoords) {
        alert("Please click on the map to select coordinates first.");
        return;
    }

    // Pošaljemo skalirane koordinate serveru putem Axios POST poziva
    axios.post("/make-guess", selectedCoords)
        .then(response => {
            const result = response.data;
            // Prikazivanje odgovora sa servera u zavisnosti od statusa
            if (result.status === "success") {
                document.getElementById("result-text").innerText = result.message;  // Bravo poruka
                document.getElementById("result-text").style.color = "green";
            } else {
                document.getElementById("result-text").innerText = result.message;  // Failure poruka
                document.getElementById("result-text").style.color = "red";
            }
        })
        .catch(error => {
            console.error("There was an error!", error);
        });
});
