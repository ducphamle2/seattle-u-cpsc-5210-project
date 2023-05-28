from world import World
from ship import Ship
from superstartrek import Game
from quadrant import Quadrant
from basic_structure import Point, QuadrantData, KlingonShip, Entity
from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from parameterized import parameterized
import helper

class TestNavigationProcess(TestCase):
    def setUp(self):
        self.game = Game()
        self.world = World()
        self.ship = self.world.ship

    @patch.object(Quadrant, 'set_value')
    def test_navigation_klingon_ship_move(self, mock):
        for klingon_ship in self.world.quadrant.klingon_ships:
            klingon_ship.shield = 5 # value not equal to zero
        self.game.navigation_klingon_ship_move(self.world.quadrant, self.world.quadrant.klingon_ships)
        self.assertTrue(mock.called)

    

    

        




        
    
    
    
    

    

    