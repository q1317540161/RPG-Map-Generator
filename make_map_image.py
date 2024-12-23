from PIL import Image

# File paths for your terrain images
GRASS_IMG = "images/grass.png"
WATER_IMG = "images/river.png"
MOUNTAIN_IMG = "images/mountain.png"


# Terrain mapping
TERRAIN_IMAGES = {
    1: GRASS_IMG,    # Grass
    2: WATER_IMG,    # Water (river)
    3: MOUNTAIN_IMG, # Mountain
}

# Generate a map image
def generate_map_image(map_data, terrain_images, output_file="generated_map.png"):
    # Load terrain images
    terrain_images = {key: Image.open(path) for key, path in terrain_images.items()}
    tile_width, tile_height = next(iter(terrain_images.values())).size

    # Create a blank canvas for the map
    map_height = len(map_data)
    map_width = len(map_data[0])
    map_image = Image.new("RGB", (map_width * tile_width, map_height * tile_height))

    # Draw the map
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            tile = terrain_images[cell]
            map_image.paste(tile, (x * tile_width, y * tile_height))

    # Save the map image
    map_image.save(output_file)
    print(f"Map image saved as {output_file}")

def load_map(file_name):
    with open(file_name, "r") as file:
        map_data = [list(map(int, line.split())) for line in file]
    return map_data

# Generate the map image
if __name__ == "__main__":
    map_name = input("file name:")
    map_data = load_map(map_name)

    generate_map_image(map_data, TERRAIN_IMAGES)
