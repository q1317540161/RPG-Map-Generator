import random
import numpy as np
from itertools import product

# Parameters
ROWS, COLS = 30, 40  # Dimensions of the map
POPULATION_SIZE = 20
GENERATIONS = 30
# P1 = 0.5  # Probability of changing a neighbor
# P2, P3, P4 = 0.33, 0.33, 0.33  # Probabilities for choosing grass, river, or mountain

P1, P2, P3 = 0.3, 0.7, 0.5
# Terrain types
GRASS = 1
RIVER = 2
MOUNTAIN = 3

# Initialize population as empty grassland
def initialize_population():
    map_grid = [np.full((ROWS, COLS), GRASS) for _ in range(POPULATION_SIZE)]
    lake_height = random.randint(3, 6)
    lake_width = random.randint(3, 6)
    start_x = random.randint(0, ROWS-1)
    start_y = random.randint(0, COLS-1)

    for map in map_grid:
        map[0,:] = MOUNTAIN          # Top border
        map[1,:] = MOUNTAIN          # Top border
        map[-1,:] = MOUNTAIN         # Bottom border
        map[-2,:] = MOUNTAIN         # Bottom border
        map[:,0] = MOUNTAIN          # Left border
        map[:,1] = MOUNTAIN          # Left border
        map[:,-1] = MOUNTAIN         # Right border
        map[:,-2] = MOUNTAIN         # Right border

        for i in range(start_x, start_x + lake_height):
            for j in range(start_y, start_y + lake_width):
                if (0 <= i < ROWS) and (0 <= j < COLS):
                    map[i][j] = RIVER

        

    return map_grid

# Fitness function
def fitness_function(map_grid):
    fitness = 0

    # Contiguity of rivers and mountains
    for terrain in [GRASS, RIVER, MOUNTAIN]:
        regions = count_discrete_regions(map_grid, terrain)
        if regions == 1:
            fitness += 50
        else:
            fitness -= regions * 20

    # Reward variety and balance between terrains
    unique, counts = np.unique(map_grid, return_counts=True)
    terrain_counts = dict(zip(unique, counts))
    fitness += min(terrain_counts.get(RIVER, 0), terrain_counts.get(MOUNTAIN, 0)) * 2

    return fitness

# Count discrete regions using flood-fill
def count_discrete_regions(map_grid, terrain):
    visited = np.zeros((ROWS, COLS), dtype=bool)
    count = 0

    def flood_fill(x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if not (0 <= cx < ROWS and 0 <= cy < COLS):
                continue
            if visited[cx][cy] or map_grid[cx][cy] != terrain:
                continue
            visited[cx][cy] = True
            stack.extend([(cx + dx, cy + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

    for i, j in product(range(ROWS), range(COLS)):
        if not visited[i][j] and map_grid[i][j] == terrain:
            count += 1
            flood_fill(i, j)

    return count

# Mutation process
def mutate(map_grid):
    new_map = map_grid.copy()
    stack = []
    map_visit = np.zeros((ROWS,COLS), dtype=int)

    # Select three random 3x3 blocks and mutate
    for _ in range(5):
        x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        stack.append((x, y))

        while stack:
            cx, cy = stack.pop()
            map_visit[cx, cy] = 1
            terrain_type = map_grid[cx, cy]

            # Apply P1: Decide whether to change the cell
            if terrain_type == GRASS:
                p = P1
            elif terrain_type == RIVER:
                p = P2
            else:
                p = P3
            if random.random() < p:                
                new_map[cx][cy] = terrain_type

                # Push neighbors onto the stack
                neighbors = [(cx + dx, cy + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                for nx, ny in neighbors:
                    if (0 <= nx < ROWS) and (0 <= ny < COLS) and (not map_visit[nx, ny]):
                        new_map[nx][ny] = terrain_type
                        stack.append((nx, ny))

    return new_map

# Roulette wheel selection
def roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    return random.choices(population, probabilities, k=POPULATION_SIZE)

# Genetic Algorithm with mutation-only process
def genetic_algorithm():
    population = initialize_population()

    for generation in range(GENERATIONS):
        # Evaluate fitness
        fitness_scores = [fitness_function(map_grid) for map_grid in population]

        # Select parents
        parents = roulette_wheel_selection(population, fitness_scores)

        # Generate next generation using mutation
        next_generation = [mutate(parent) for parent in parents]

        population = next_generation

        # Output the best fitness of this generation
        best_fitness = max(fitness_scores)
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

    # Return the best map
    best_index = fitness_scores.index(max(fitness_scores))
    return population[best_index]

# Run the Genetic Algorithm


# Save the best map to a .txt file
def save_map_to_txt(map_grid, file_name):
    with open(file_name, "w") as file:
        for row in map_grid:
            file.write(" ".join(map(str, row)) + "\n")

if __name__ == "__main__":
    best_map = genetic_algorithm()
    save_map_to_txt(best_map, "map1.txt")
