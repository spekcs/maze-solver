import unittest
from maze import Maze
from maze import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual( len(maze._cells), num_rows)
        self.assertEqual(len(maze._cells[0]), num_cols)
        
    def test_maze_create_cells_invalid(self):
        num_rows = -1
        num_cols = 0
        with self.assertRaises(Exception):
            maze = Maze(0, 0, num_rows, num_cols, 10, 10)

if __name__ == "__main__":
    unittest.main()
