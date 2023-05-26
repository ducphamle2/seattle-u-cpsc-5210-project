from basic_structure import QuadrantData
import random
from typing import List
from ship import Ship
from helper import fnr
from quadrant import Quadrant

class World:
    def __init__(
        self,
        total_klingons: int = 0,  # Klingons at start of game
        bases_in_galaxy: int = 0,
    ) -> None:
        self.ship = Ship()
        self.initial_stardate = 100 * random.randint(20, 39)
        self.stardate: float = self.initial_stardate
        self.mission_duration = random.randint(25, 34)

        # Enemy
        self.remaining_klingons = total_klingons

        # Player starbases
        self.bases_in_galaxy = bases_in_galaxy

        self.galaxy_map: List[List[QuadrantData]] = [
            [QuadrantData(0, 0, 0) for _ in range(8)] for _ in range(8)
        ]
        self.charted_galaxy_map: List[List[QuadrantData]] = [
            [QuadrantData(0, 0, 0) for _ in range(8)] for _ in range(8)
        ]

        # initialize contents of galaxy
        for x in range(8):
            for y in range(8):
                r1 = random.random()

                if r1 > 0.98:
                    quadrant_klingons = 3
                elif r1 > 0.95:
                    quadrant_klingons = 2
                elif r1 > 0.80:
                    quadrant_klingons = 1
                else:
                    quadrant_klingons = 0
                self.remaining_klingons += quadrant_klingons

                quadrant_bases = 0
                if random.random() > 0.96:
                    quadrant_bases = 1
                    self.bases_in_galaxy += 1
                self.galaxy_map[x][y] = QuadrantData(
                    quadrant_klingons, quadrant_bases, 1 + fnr()
                )

        if self.remaining_klingons > self.mission_duration:
            self.mission_duration = self.remaining_klingons + 1

        if self.bases_in_galaxy == 0:  # original has buggy extra code here
            self.bases_in_galaxy = 1
            self.galaxy_map[self.ship.position.quadrant.x][
                self.ship.position.quadrant.y
            ].bases += 1

        curr = self.ship.position.quadrant
        self.quadrant = Quadrant(
            self.ship.position.quadrant,
            self.galaxy_map[curr.x][curr.y],
            self.ship.position,
        )

    def remaining_time(self) -> float:
        return self.initial_stardate + self.mission_duration - self.stardate

    def has_mission_ended(self) -> bool:
        return self.remaining_time() < 0