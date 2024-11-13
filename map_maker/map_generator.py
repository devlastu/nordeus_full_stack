# Generate the map when the application starts
import os

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter


matplotlib.use("TkAgg")


def generate_map(matrix=None, sigma=0.5):
    # Ako matrica nije prosleđena, povući ćemo mapu


    if matrix is None:
        return None  # Ako mapa nije uspešno povučena, vrati None

    # Primena Gaussian blur-a na matricu visine radi omekšavanja ivica
    matrix_smoothed = gaussian_filter(matrix, sigma=sigma)

    # Osnovne boje sa dodatnim nijansama za prirodne prelaze
    colors = [
        (0, 105, 148),  # #006994 - Plava (More)
        (229, 217, 194),  # #E5D9C2 - Tamnija bež
        (181, 186, 97),  # #B5BA61 - Svetla maslinasta zelena
        (133, 159, 61),  # #859F3D - Prigušena zelena
        (124, 141, 76),  # #7C8D4C - Tamna maslinasta zelena

        # Dodate nijanse između tamne maslinaste i tamno zelene
        (104, 118, 62), (90, 101, 54), (77, 86, 46), (65, 73, 39), (57, 64, 33),
        (49, 81, 30),     # #31511E - Tamno zelena

        # Dodate nijanse između srednje smeđe i tamno smeđe
        (123, 106, 74), (109, 93, 64),

        (114, 84, 40),  # #725428 - Topla smeđa
        (101, 69, 31),  # #65451F - Tamno smeđa
        (192, 192, 192),  # #C0C0C0 - Svetlo siva
        (128, 128, 128),  # #808080 - Srednje siva
        (80, 80, 80),  # #505050 - Tamno siva
        (255, 255, 255),  # #FFFFFF - Bela
    ]

    # Generisanje proširene liste boja sa interpolacijom
    extended_colors = []
    for i in range(len(colors) - 1):
        color1 = colors[i]
        color2 = colors[i + 1]

        # Dodajemo početnu boju
        extended_colors.append(color1)

        # Interpoliramo 4 dodatne nijanse između color1 i color2
        for j in range(1, 6):
            interpolated_color = tuple(
                int(color1[k] + (color2[k] - color1[k]) * j / 6) for k in range(3)
            )
            extended_colors.append(interpolated_color)

    extended_colors.append(colors[-1])  # Dodajemo poslednju boju

    # Kreiranje prilagođene colormap
    cmap = ListedColormap([tuple(c / 255.0 for c in color) for color in extended_colors])

    # Nivoi visina od 0 do 1000, u koraku od 50
    levels = np.linspace(0, 1000, len(extended_colors))

    # Plotovanje terenske mape sa zamućenom matricom
    plt.figure(figsize=(6, 6))
    plt.contourf(matrix_smoothed, levels=levels, cmap=cmap)
    plt.axis("off")  # Sakrivanje osi za čist prikaz

    # Definiši putanju do fajla
    map_path = "frontend/static/maps/map.png"

    # Proveri da li direktorijum postoji, ako ne, kreiraj ga
    directory = os.path.dirname(map_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(map_path, bbox_inches="tight", pad_inches=0)
    plt.close()

    return map_path