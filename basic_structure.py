from dataclasses import dataclass
from enum import Enum

class Entity(Enum):
    klingon = "+K+"
    ship = "<*>"
    empty = "***"
    starbase = ">!<"
    star = " * "
    void = "   "


@dataclass
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x + 1} , {self.y + 1}"


@dataclass
class Position:
    """
    Every quadrant has 8 sectors

    Hence the position could also be represented as:
    x = quadrant.x * 8 + sector.x
    y = quadrant.y * 8 + sector.y
    """

    quadrant: Point
    sector: Point


@dataclass
class QuadrantData:
    klingons: int
    bases: int
    stars: int

    def num(self) -> int:
        return 100 * self.klingons + 10 * self.bases + self.stars


@dataclass
class KlingonShip:
    sector: Point
    shield: float