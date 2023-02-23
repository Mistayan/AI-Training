import os

base_dir = os.getcwd().split("\\")
i = 0
for i, b in enumerate(base_dir):
    if b == "AI-Training":
        break
base_dir = os.path.join("\\".join(base_dir[0: i + 1]))


def FACTORS(grid_size: int):
    return {  # Lower PENALTY values increases factor
        'DIST_PENALTY': 0.73,
        'LIFE_PENALTY': 18,
        'AMMO_PENALTY': 1.5,
        'MAP_MAX_DISTANCE': (grid_size ** 2 + grid_size ** 2) ** 0.5
    }
