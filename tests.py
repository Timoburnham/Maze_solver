import unittest
from window import Maze
import random

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_maze_create_cells_different_size(self):
        num_cols = 5
        num_rows = 8
        m2 = Maze(0, 0, num_rows, num_cols, 15, 15)
        self.assertEqual(len(m2._cells), num_rows)
        self.assertEqual(len(m2._cells[0]), num_cols)

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        maze._break_entrance_and_exit()


        entrance_cell = maze._cells[0][0]
        self.assertFalse(entrance_cell.has_top_wall)

        exit_cell = maze._cells[num_rows-1][num_cols-1]
        self.assertFalse(exit_cell.has_bottom_wall)



    def test_all_cells_visited(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        maze._break_walls_r(0, 0)  
        
        all_visited = True
        for row in maze._cells:
            for cell in row:
                if not cell.visited:
                    all_visited = False
                    break
            if not all_visited:
                break

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)

        maze._cells[0][0].visited = True
        maze._cells[1][1].visited = True

        maze.reset_cells_visited()

        for row in maze._cells:
            for cell in row:
                self.assertFalse(cell.visited, "Not all cells were reset properly")

        self.assertFalse(cell.visited, "Not all cells were visited during maze generation")

if __name__ == "__main__":
    unittest.main()
