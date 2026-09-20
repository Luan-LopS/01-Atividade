import unittest


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_left(self):
        self.x -= 10

    def move_right(self):
        self.x += 10

    def get_position(self):
        return (self.x, self.y)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(100, 100)

    def test_initial_position(self):
        self.assertEqual(self.player.get_position(), (100, 100))

    def test_move_left(self):
        self.player.move_left()
        self.assertEqual(self.player.get_position(), (90, 100))

    def test_move_right(self):
        self.player.move_right()
        self.assertEqual(self.player.get_position(), (110, 100))


if __name__ == "__main__":
    unittest.main()
