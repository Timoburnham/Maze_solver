from window import Window, Line, Point, Cell, Maze
import time



def main():

	
	num_rows = 10
	num_cols = 10
	margin = 50
	screen_x = 800
	screen_y = 600
	cell_size_x = (screen_x - 2 * margin) / num_cols
	cell_size_y = (screen_y - 2 * margin) / num_rows

	win = Window(screen_x, screen_y)

	maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
	maze.create_maze()
	maze.draw()
	is_solved = maze.solve()
	print(f"Maze solved: {is_solved}")

	

	win.wait_for_close()



if __name__ == "__main__":
    main()
