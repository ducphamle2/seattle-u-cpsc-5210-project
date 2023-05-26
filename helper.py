import random
from typing import Final

def fnr() -> int:
    """Generate a random integer from 0 to 7 inclusive."""
    return random.randint(0, 7)

def get_user_float(prompt: str) -> float:
    """Get input from user and return it."""
    while True:
        answer = input(prompt)
        try:
            answer_float = float(answer)
            return answer_float
        except ValueError:
            pass

klingon_shield_strength: Final = 200
# 8 sectors = 1 quadrant
dirs: Final = [  # (down-up, left,right)
    [0, 1],  # 1: go right (same as #9)
    [-1, 1],  # 2: go up-right
    [-1, 0],  # 3: go up  (lower x-coordines; north)
    [-1, -1],  # 4: go up-left (north-west)
    [0, -1],  # 5: go left (west)
    [1, -1],  # 6: go down-left (south-west)
    [1, 0],  # 7: go down (higher x-coordines; south)
    [1, 1],  # 8: go down-right
    [0, 1],  # 9: go right (east)
]  # vectors in cardinal directions