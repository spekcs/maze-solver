from tkinter import Tk, BOTH, Canvas
from time import sleep


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.wm_title("Maze")
        self.__canvas = Canvas(height=height, width=width)
        self.__canvas.pack()
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
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)


class Cell:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, window = None, has_left_wall: bool = True, has_right_wall: bool = True, has_top_wall: bool = True, has_bottom_wall: bool = True) -> None:
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window

    def draw(self, break_bottom: bool = False, break_top: bool = False, break_left: bool = False, break_right: bool = False):
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x2, self._y2)
        p3 = Point(self._x1, self._y2)
        p4 = Point(self._x2, self._y1)
        l_top = Line(p1, p4)
        l_bottom = Line(p3, p2)
        l_left = Line(p1, p3)
        l_right = Line(p4, p2)
        if self._win:
            if self.has_top_wall:
                self._win.draw_line(l_top, "white" if break_top else "black")
            if self.has_bottom_wall:
                self._win.draw_line(l_bottom, "white" if break_bottom else "black")
            if self.has_right_wall:
                self._win.draw_line(l_right, "white" if break_right else "black")
            if self.has_left_wall:
                self._win.draw_line(l_left, "white" if break_left else "black")

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"
        p1 = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        p2 = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)
        if self._win:
            self._win.draw_line(Line(p1, p2), color)

class Maze:
    def __init__(self, x1: int, y1: int, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int, win = None) -> None:
        if num_rows < 1 or num_cols < 1:
            raise Exception("Maze must have at least one row and column")
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for row in range(self._num_rows):
            self._cells.append([])
            for col in range(self._num_cols):
                self._cells[row].append(Cell(x1=self._x1 + self._cell_size_x * col, y1=self._y1 + self._cell_size_y * row,
                                        x2= self._x1 + self._cell_size_x * (col + 1), y2=self._y1 + self._cell_size_y * (row + 1), window=self._win))


        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self._win:
            self._win.redraw()
            sleep(0.02)


def main():
    win = Window(800, 600)
    _ = Maze(10, 10, 15, 15, 20, 20, win)
    win.wait_for_close()

if __name__ == "__main__":
    main()
