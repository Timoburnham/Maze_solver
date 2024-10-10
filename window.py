from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
	def __init__(self, width, height):
		self.__root = Tk()
		self.__root.title("My Window")
		self.__canvas = Canvas(self.__root, width=width, height=height)
		self.__canvas.pack(fill=BOTH, expand=True)
		self.__running = False
		self.__root.protocol("WM_DELETE_WINDOW", self.close)

	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update()

	def wait_for_close(self):
		self.__running = True
		while self.__running:
			self.redraw()

	def close(self):
		self.__running = False


	def draw_line(self, line, fill_color):
		line.draw_window(self.__canvas, fill_color)


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Line:
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2


	def draw_window(self, canvas, fill_color):
		canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)


class Cell:
	
	

	def __init__(self, _x1, _x2, _y1, _y2, win = None):
		self.has_left_wall = True
		self.has_right_wall = True
		self.has_bottom_wall = True
		self.has_top_wall = True
		self._x1 = _x1
		self._x2 = _x2
		self._y1 = _y1
		self._y2 = _y2
		self.win = win
		self.visited = False

	def draw(self, win, fill_color):
		if win is None:
			return

		line_color = "black"
		background_color = fill_color

		p1 = Point(self._x1, self._y1)
		p2 = Point(self._x1, self._y2)
		p3 = Point(self._x2, self._y1)
		p4 = Point(self._x2, self._y2)

		left_wall = Line(p1, p2)
		right_wall = Line(p3, p4)
		top_wall = Line(p1, p3)
		bottom_wall = Line(p2, p4)

		win.draw_line(left_wall, fill_color)
		win.draw_line(right_wall, fill_color)
		win.draw_line(top_wall, fill_color)
		win.draw_line(bottom_wall, fill_color)

		if self.has_left_wall:
			win.draw_line(left_wall, line_color)
		else:
			win.draw_line(left_wall, background_color)

		if self.has_right_wall:
			win.draw_line(right_wall, line_color)
		else:
			win.draw_line(right_wall, background_color)

		if self.has_top_wall:
			win.draw_line(top_wall, line_color)
		else:
			win.draw_line(top_wall, background_color)

		if self.has_bottom_wall:
			win.draw_line(bottom_wall, line_color)
		else:
			win.draw_line(bottom_wall, background_color)
	

	def draw_move(self, to_cell, undo=False):
		color = "gray" if undo else "red"
	
	
		current_center_x = (self._x1 + self._x2) / 2
		current_center_y = (self._y1 + self._y2) / 2
	
		to_center_x = (to_cell._x1 + to_cell._x2) / 2
		to_center_y = (to_cell._y1 + to_cell._y2) / 2
	
	
		line = Line(Point(current_center_x, current_center_y), Point(to_center_x, to_center_y))
		self.win.draw_line(line, color)



class Maze:
	def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
		self.x1 = x1
		self.y1 = y1
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y
		self.win = win
		self._cells = []
		self._create_cells()
		self.visited = False
		if seed is not None:
			random.seed(seed)

	def draw(self):
		for i in range(self.num_rows):
			for j in range(self.num_cols):
				self._cells[i][j].draw(self.win, fill_color="white")
		self._animate()

	def _create_cells(self):
		for rows_index in range(self.num_rows):

			row = []
			for col_index in range(self.num_cols):
				x1 = self.x1 + col_index * self.cell_size_x
				y1 = self.y1 + rows_index * self.cell_size_y
				x2 = x1 + self.cell_size_x
				y2 = y1 + self.cell_size_y
				cell = Cell(x1, x2, y1, y2, win =  self.win)
				row.append(cell)
			self._cells.append(row)


	def _draw_cell(self, i, j, win = None, fill_color= None):
		if self.win is not None:

			x = self.x1 + j * self.cell_size_x
			y = self.y1 + i * self.cell_size_y

			self._cells[i][j].draw(self.win, fill_color)

			self._animate()


	def _animate(self):
		self.win.redraw()

		time.sleep(0.05)



	def _break_entrance_and_exit(self):
		
		entrance_cell = self._cells[0][0]
		entrance_cell.has_top_wall = False
		self._draw_cell(0, 0)


		exit_row = self.num_rows - 1
		exit_col = self.num_cols - 1
		exit_cell = self._cells[exit_row][exit_col]
		exit_cell.has_bottom_wall = False
		self._draw_cell(exit_row, exit_col)




	def _break_walls_r(self, i, j):
		self._cells[i][j].visited = True

		while True:
			directions = [("up", -1, 0), ("down", 1, 0), ("left", 0, -1), ("right", 0, 1)]
			unvisited_neighbors = []

			for direction, di, dj in directions:
				ni, nj = i + di, j + dj
				if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols:
					if not self._cells[ni][nj].visited:
						unvisited_neighbors.append((direction, ni, nj))

			if len(unvisited_neighbors) == 0:
				self._draw_cell(i, j)
				return

			chosen_direction, ni, nj = random.choice(unvisited_neighbors)

			if chosen_direction == "up":
				self._cells[i][j].has_top_wall = False
				self._cells[ni][nj].has_bottom_wall = False
			elif chosen_direction == "down":
				self._cells[i][j].has_bottom_wall = False
				self._cells[ni][nj].has_top_wall = False
			elif chosen_direction == "left":
				self._cells[i][j].has_left_wall = False
				self._cells[ni][nj].has_right_wall = False
			elif chosen_direction == "right":
				self._cells[i][j].has_right_wall = False
				self._cells[ni][nj].has_left_wall = False

			self._break_walls_r(ni, nj)


	def reset_cells_visited(self):
		for i in range(self.num_rows):
			for j in range(self.num_cols):
				self._cells[i][j].visited = False


	def solve(self):
		for i in range(self.num_rows):
			for j in range(self.num_cols):
				self._cells[i][j].visited = False
	
		return self._solve_r(i=0, j=0)


	def _solve_r(self, i, j):
		self._animate()

		self._cells[i][j].visited = True
		if i == self.num_rows - 1 and j == self.num_cols - 1:
			return True
	
		directions = [("up", -1, 0), ("right", 0, 1), ("down", 1, 0), ("left", 0, -1)]

		for direction, di, dj in directions:
			ni, nj = i + di, j + dj
			if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols and not self._cells[ni][nj].visited:
				if (
					(direction == "up" and not self._cells[i][j].has_top_wall) or
					(direction == "right" and not self._cells[i][j].has_right_wall) or
					(direction == "down" and not self._cells[i][j].has_bottom_wall) or
					(direction == "left" and not self._cells[i][j].has_left_wall)
				):
					self._draw_move(i, j, direction)
					if self._solve_r(ni, nj):
						return True
					self._draw_move(i, j, direction, undo=True)

		return False




	def create_maze(self):
		if not self._cells:
			self._create_cells()
		self._break_walls_r(0, 0)


	def _draw_move(self, i, j, direction, undo=False):
		current_cell = self._cells[i][j]
	
		if direction == "up":
			to_cell = self._cells[i-1][j]
		elif direction == "right":
			to_cell = self._cells[i][j+1]
		elif direction == "down":
			to_cell = self._cells[i+1][j]
		elif direction == "left":
			to_cell = self._cells[i][j-1]
		else:
			return  

		current_cell.draw_move(to_cell, undo)
