import random

def print_forest(forest):
    for row in forest:
        print(" ".join(row))
    print()

def generate_forest_15x15(
        obstacle_prob=0.18,
        small_fire_prob=0.10,
        large_fire_prob=0.06,
        seed=None):
    """
    Generate a 15x15 forest grid with:
    - Start ’S’ at (0,0)
    - Goal ’*’ at (14,14)
    - Obstacles ’#’
    - Small fires ’f’
    - Large fires ’F’
    - Open ground ’.’
    Notes:
    - Probabilities are applied only to non-start/non-goal cells.
    - This function does NOT guarantee solvability, but it avoids placing
    obstacles on S and *.
    """
    if seed is not None:
        random.seed(seed)

    size = 15
    forest = [['.' for _ in range(size)] for _ in range(size)]
    forest[0][0] = 'S'
    forest[size - 1][size - 1] = '*'

    for r in range(size):
        for c in range(size):
            if (r, c) in [(0, 0), (size - 1, size - 1)]:
                continue
            x = random.random()
            if x < obstacle_prob:
                forest[r][c] = '#'
            elif x < obstacle_prob + large_fire_prob:
                forest[r][c] = 'F'
            elif x < obstacle_prob + large_fire_prob + small_fire_prob:
                forest[r][c] = 'f'
            else:
                forest[r][c] = '.'

    return forest