from basic_structure import Position, Point
from typing import List, Tuple
from helper import fnr

class Ship:
    energy_capacity: int = 3000
    torpedo_capacity: int = 10

    def __init__(self) -> None:
        self.position = Position(Point(fnr(), fnr()), Point(fnr(), fnr()))
        self.energy: int = Ship.energy_capacity
        self.devices: Tuple[str, ...] = (
            "WARP ENGINES",
            "SHORT RANGE SENSORS",
            "LONG RANGE SENSORS",
            "PHASER CONTROL",
            "PHOTON TUBES",
            "DAMAGE CONTROL",
            "SHIELD CONTROL",
            "LIBRARY-COMPUTER",
        )
        self.damage_stats: List[float] = [0] * len(self.devices)
        self.shields = 0
        self.torpedoes = Ship.torpedo_capacity
        self.docked: bool = False  # true when docked at starbase

    def refill(self) -> None:
        self.energy = Ship.energy_capacity
        self.torpedoes = Ship.torpedo_capacity

    def maneuver_energy(self, n: int) -> None:
        """Deduct the energy for navigation from energy/shields."""
        self.energy -= n + 10

        if self.energy <= 0:
            print("SHIELD CONTROL SUPPLIES ENERGY TO COMPLETE THE MANEUVER.")
            self.shields += self.energy
            self.energy = 0
            self.shields = max(0, self.shields)

    def shield_control(self) -> None:
        """Raise or lower the shields."""
        if self.damage_stats[6] < 0:
            print("SHIELD CONTROL INOPERABLE")
            return

        while True:
            energy_to_shield = input(
                f"ENERGY AVAILABLE = {self.energy + self.shields} NUMBER OF UNITS TO SHIELDS? "
            )
            if len(energy_to_shield) > 0:
                x = int(energy_to_shield)
                break

        if x < 0 or self.shields == x:
            print("<SHIELDS UNCHANGED>")
            return

        if x > self.energy + self.shields:
            print(
                "SHIELD CONTROL REPORTS  'THIS IS NOT THE FEDERATION "
                "TREASURY.'\n"
                "<SHIELDS UNCHANGED>"
            )
            return

        self.energy += self.shields - x
        self.shields = x
        print("DEFLECTOR CONTROL ROOM REPORT:")
        print(f"  'SHIELDS NOW AT {self.shields} UNITS PER YOUR COMMAND.'")