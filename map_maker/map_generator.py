import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter


def generate_map(matrix=None, sigma=0.2, target_width=600, target_height=600):
    # If no matrix is provided, return None
    if matrix is None:
        return None  # If the map isn't successfully fetched, return None

    # Apply Gaussian blur on the height matrix to soften edges
    matrix_smoothed = gaussian_filter(matrix, sigma=sigma)

    # Basic colors with additional shades for natural transitions
    colors = [
        (5, 107, 167, 255),  # Blue (Water)
        (229, 217, 194),     # Darker beige
        (181, 186, 97),      # Light olive green
        (133, 159, 61),      # Muted green
        (124, 141, 76),      # Dark olive green
        (104, 118, 62),      # Dark green
        (123, 106, 74),      # Brown
        (114, 84, 40),       # Warm brown
        (101, 69, 31),       # Dark brown
        (192, 192, 192),     # Light gray
        (128, 128, 128),     # Medium gray
        (80, 80, 80),        # Dark gray
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
