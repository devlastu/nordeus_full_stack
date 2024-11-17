import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter


def generate_map(matrix=None, difficulty = "regular", target_width=600, target_height=600):
    # If no matrix is provided, return None
    sigma = 0.2
    if matrix is None:
        return None  # If the map isn't successfully fetched, return None

    if difficulty == "hard":
        sigma = 1.5
    elif difficulty == "master":
        sigma = 3
    else:
        sigma = 0.2
    print(difficulty)
    # Apply Gaussian blur on the height matrix to soften edges
    matrix_smoothed = gaussian_filter(matrix, sigma=sigma)

    # Basic colors with additional shades for natural transitions
    colors = [
        (38, 221, 255),  # Blue (Water)
        (255,255,204),     # Darker beige
        (221, 221, 187),
        # (204, 204, 170),

        (201,234,136),
        (167,205,115),
        (133,175,94),
        (98,146,73),
        (64, 116, 52),

        (190, 158, 128),
        (166, 138, 112),
        (143, 119, 96),
        (119, 99, 80),
        (107, 88, 70),

        (228, 220, 209),
        (247, 244, 241),
        (255, 255, 255),     # White
    ]

    # Generate extended list of colors with interpolation
    extended_colors = []
    for i in range(len(colors) - 1):
        color1 = colors[i]
        color2 = colors[i + 1]
        extended_colors.append(color1)
        for j in range(1, 6):  # Interpolate 4 more shades
            interpolated_color = tuple(
                int(color1[k] + (color2[k] - color1[k]) * j / 6) for k in range(3)
            )
            extended_colors.append(interpolated_color)

    extended_colors.append(colors[-1])  # Add the last color

    # Create the custom colormap
    cmap = ListedColormap([tuple(c / 255.0 for c in color) for color in extended_colors])

    # Set height levels from 0 to 1000 in steps of 50
    levels = np.linspace(0, 1000, len(extended_colors))

    # Plot the terrain map with the blurred matrix
    plt.figure(figsize=(6, 6))
    plt.contourf(matrix_smoothed, levels=levels, cmap=cmap)

    # Invert the y-axis so that the image is not upside down
    plt.gca().invert_yaxis()

    plt.axis("off")  # Hide axes for a cleaner display

    # Define the file path for saving the map
    map_path = "frontend/static/maps/map.png"

    # Check if the directory exists, if not, create it
    directory = os.path.dirname(map_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the figure
    plt.savefig(map_path, bbox_inches="tight", pad_inches=0)
    plt.close()

    # Use PIL to open the image and get its dimensions (width and height in pixels)
    try:
        with Image.open(map_path) as img:
            width, height = img.size
            print(f"Original image dimensions: {width}x{height}")

            # Check if resizing is necessary
            if width != target_width or height != target_height:
                img_resized = img.resize((target_width, target_height), Image.LANCZOS)
                img_resized.save(map_path)
                print(f"Image resized to: {target_width}x{target_height}")

    except Exception as e:
        print(f"Error handling image: {e}")
        return None

    return map_path, target_width, target_height
