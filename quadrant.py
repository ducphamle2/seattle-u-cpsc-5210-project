from basic_structure import Point, Position, QuadrantData, KlingonShip, Entity
from typing import List, Tuple
from helper import fnr,klingon_shield_strength
import random

class Quadrant:
    def __init__(
        self,
        point: Point,  # position of the quadrant
        population: QuadrantData,
        ship_position: Position,
    ) -> None:
        """Populate quadrant map"""
        assert 0 <= point.x <= 7 and 0 <= point.y <= 7
        self.name = Quadrant.quadrant_name(point.x, point.y, False)

        self.nb_klingons = population.klingons
        self.nb_bases = population.bases
        self.nb_stars = population.stars

        # extra delay in repairs at base
        self.delay_in_repairs_at_base: float = 0.5 * random.random()

        # Klingons in current quadrant
        self.klingon_ships: List[KlingonShip] = []

        # Initialize empty: save what is at which position
        self.data = [[Entity.void for _ in range(8)] for _ in range(8)]

        self.populate_quadrant(ship_position)

    @classmethod
    def quadrant_name(cls, row: int, col: int, region_only: bool = False) -> str:
        """Return quadrant name visible on scans, etc."""
        region1 = [
            "ANTARES",
            "RIGEL",
            "PROCYON",
            "VEGA",
            "CANOPUS",
            "ALTAIR",
            "SAGITTARIUS",
            "POLLUX",
        ]
        region2 = [
            "SIRIUS",
            "DENEB",
            "CAPELLA",
            "BETELGEUSE",
            "ALDEBARAN",
            "REGULUS",
            "ARCTURUS",
            "SPICA",
        ]
        modifier = ["I", "II", "III", "IV"]

        quadrant = region1[row] if col < 4 else region2[row]

        if not region_only:
            quadrant += " " + modifier[col % 4]

        return quadrant

    def set_value(self, x: float, y: float, entity: Entity) -> None:
        self.data[round(x)][round(y)] = entity

    def get_value(self, x: float, y: float) -> Entity:
        return self.data[round(x)][round(y)]

    def find_empty_place(self) -> Tuple[int, int]:
        """Find an empty location in the current quadrant."""
        while True:
            row, col = fnr(), fnr()
            if self.get_value(row, col) == Entity.void:
                return row, col

    def populate_quadrant(self, ship_position: Position) -> None:
        self.set_value(ship_position.sector.x, ship_position.sector.y, Entity.ship)
        for _ in range(self.nb_klingons):
            x, y = self.find_empty_place()
            self.set_value(x, y, Entity.klingon)
            self.klingon_ships.append(
                KlingonShip(
                    Point(x, y), klingon_shield_strength * (0.5 + random.random())
                )
            )
        if self.nb_bases > 0:
            # Position of starbase in current sector
            starbase_x, starbase_y = self.find_empty_place()
            self.starbase = Point(starbase_x, starbase_y)
            self.set_value(starbase_x, starbase_y, Entity.starbase)
        for _ in range(self.nb_stars):
            x, y = self.find_empty_place()
            self.set_value(x, y, Entity.star)

    def __str__(self) -> str:
        quadrant_string = ""
        for row in self.data:
            for entity in row:
                quadrant_string += entity.value
        return quadrant_string