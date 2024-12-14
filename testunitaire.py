import unittest
import pygame
from jeu import Player, Block, Fire, get_block, load_sprite_sheets

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player = Player(100, 100, 50, 50)

    def tearDown(self):
        pygame.quit()

    def test_initial_position(self):
        self.assertEqual(self.player.rect.x, 100)
        self.assertEqual(self.player.rect.y, 100)

    def test_jump(self):
        self.player.jump()
        self.assertLess(self.player.y_vel, 0)  # Vérifie que la vitesse verticale est négative

    def test_move_left(self):
        self.player.move_left(5)
        self.assertEqual(self.player.x_vel, -5)

    def test_move_right(self):
        self.player.move_right(5)
        self.assertEqual(self.player.x_vel, 5)

    def test_hit(self):
        self.player.make_hit()
        self.assertTrue(self.player.hit)

class TestBlock(unittest.TestCase):
    def setUp(self):
        self.block = Block(100, 100, 50)

    def tearDown(self):
        pygame.quit()


class TestFire(unittest.TestCase):
    def setUp(self):
        self.fire = Fire(100, 100, 16, 32)

    def tearDown(self):
        pygame.quit()


class TestGetBlockFunction(unittest.TestCase):
    def test_get_block(self):
        block_surface = get_block(50)
        self.assertIsNotNone(block_surface)  # Vérifie que la surface n'est pas None


if __name__ == '__main__':
    unittest.main()