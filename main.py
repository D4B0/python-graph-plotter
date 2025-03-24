import re
import math
from typing import Callable


def eqn_line(x: float | int) -> float | int:
    a = + 1.0
    b = + 0.0
    y = (a * x) + b
    return y


def eqn_trig(x: float | int) -> float | int:
    a = + 1.0
    b = + 1.0 / (180/math.pi)
    func = math.tan
    c = + 0.0
    return (a * func(b * x)) + c


def eqn_quad(x: float | int) -> float | int:
    a = + 1.0
    b = + 0.0
    c = + 0.0
    return (a * (x ** 2)) + (b * x) + c


def eqn_cube(x: float | int) -> float | int:
    a = +1.0
    b = +0.0
    c = +0.0
    d = +0.0
    return (a * (x ** 3)) + (b * (x ** 2)) + (c * x) + d


def eqn_exp(x: float | int) -> float | int:
    a = math.e
    return a ** x


class Plotter:
    """
    A graph plotter in python with a few configurable attributes
    :TODO: Add documentation for plotter attributes and methods
    """
    def __init__(self, size: int) -> None:
        self.graph: list[list[str]] = []
        self.origin: list[float | int] = [0, 0]
        self.offset: list[float | int] = [0, 0]
        self.scale: list[float | int] = [1, 1]

        size += int(size % 2 == 0)

        self.create(size)

    def create(self, size: int) -> None:
        """
        Initialise the plotter and its variables
        :param size: Set the size of the plotter
        :returns: None
        """

        # Fill 2D-Array with blank points
        for row in range(size):
            self.graph.append([])
            for col in range(size):
                self.graph[row].append(" ")  # · •

        # Get default origin of array
        self.origin[0] = round(size / 2)
        self.origin[1] = round(size / 2)

    def restore(self) -> None:
        """
        Restore the plotter to its original state upon creation
        Clears all points on the plotter, even those of borders
        :returns: None
        """

        size = len(self.graph)

        # Reset each cell in the plotter
        for row in range(size):
            for col in range(size):
                self.graph[row][col] = " "

    def display(self) -> None:
        """
        Output all points in current 2D-array
        :returns: None
        """

        for row in self.graph:
            print(*(" " * 0, *row), sep="  ")

    def borders(self) -> None:
        """
        Draw the border of the plotter
        :returns: None
        """

        size = len(self.graph)

        col_border = -1
        row_border = -1

        for i in range(size):
            rel_col, rel_row = self.getRelCoordinates(i, i)

            if rel_col == 0:
                col_border = i

            if rel_row == 0:
                row_border = i

        if col_border < 0:
            col_border = 0 - (self.offset[0] < 0)

        if row_border < 0:
            row_border = 0 - (self.offset[1] > 0)

        for i in range(size):
            self.graph[i][col_border] = "\033[90m·\033[0m"
            self.graph[row_border][i] = "\033[90m·\033[0m"

    def getRelCoordinates(self, abs_x: int | float = 0, abs_y: int | float = 0) -> tuple[float | int, float | int]:
        """
        Return the relative coordinates of a given set of 'absolute' coordinates
        :param abs_x: The absolute col to get relative coordinates for
        :param abs_y: The absolute row to get relative coordinates for
        :returns: Relative X and Y coordinates
        """

        rel_x: float = (abs_x - self.origin[0] + self.offset[0]) / self.scale[0]  # X is col
        rel_y: float = (abs_y - self.origin[1] - self.offset[1]) / self.scale[1]  # Y is row
        return rel_x, -rel_y

    def getAbsCoordinates(self, rel_x: float | int = 0, rel_y: float | int = 0) -> tuple[int | float, int | float]:
        """
        Return the absolute coordinates of a given set of 'relative' coordinates
        :param rel_x: The relative col to get absolute coordinates for
        :param rel_y: The relative row to get absolute coordinates for
        :returns: Absolute X and Y coordinates
        """

        abs_x: int = int((rel_x * self.scale[0]) + self.origin[0] - self.offset[0])
        abs_y: int = int((rel_y * self.scale[1]) + self.origin[1] + self.offset[1])
        return abs_x, abs_y

    def plotSimpleFunction(self, f: Callable[[float | int], float | int]) -> None:
        """
        Plot the graph of a simple function on the plotter
        :param f: The equation the x value is parsed into
        :returns: None
        """

        for col in range(len(self.graph)):
            x = self.getRelCoordinates(col, 0)[0]
            self.plotSimpleFunctionPoint(x, f)

    def plotSimpleFunctionPoint(self, x: float, f: Callable[[float | int], float | int]) -> None:
        """
        Plot a point on the plotter of a given function
        :param x: The absolute column coordinate to use
        :param f: The equation the x value is parsed into
        :returns: None
        """

        margin_x = 1 / ( 2 * self.scale[0])

        this_y: float | int = f(x)
        prev_y: float | int = f(x - margin_x)
        next_y: float | int = f(x + margin_x)

        for row in range(len(self.graph)):
            y: float | int = self.getRelCoordinates(0, row)[1]
            if (prev_y <= y <= next_y) or (y == this_y) or (prev_y >= y >= next_y):
                self.graph[row][self.getAbsCoordinates(x, 0)[0]] = f"\033[0m·\033[0m"  # ⁘


class Controller:
    """
    A simple, terminal-based controller for the Plotter
    :TODO: Add documentation for attributes and methods
    """
    def __init__(self, size, f: Callable[[float | int], float | int]) -> None:
        # Create plotter
        self.f: Callable[[float | int], float | int] = f
        self.plotter: Plotter = Plotter(size)

        self.scale: list[float | int] = [0, 0]

        self.display_plotter()
        self.output_help()

        isActive: bool | None = True
        while not isActive is False:
            request = input("> ").lower().strip()
            isActive = self.handle_input(request)

    @staticmethod
    def output_help() -> None:
        print(
            f"Modify Plotter Zoom lvl: (+ or -) followed by (x or y)",
            f"Modify Plotter Position: (x or y) followed by (+ or -)",
            f"Output help menu: -h",
            f"Exit the program: --",
            sep="\n"
        )

    def handle_input(self, request) -> bool | None:
        request = re.sub(" ", "", request)
        params: list[str] = []

        for num in range(0, len(request), 2):
            params.append(request[num:num+2])

        scale: list[int | float] = [0, 0]
        shift: list[int | float] = [0, 0]


        for param in params:
            # Increase/Decrease Scale if found
            if re.match("^[+-]x$", param):
                scale[0] = int(param[0] + "1")
                continue
            if re.match("^[+-]y$", param):
                scale[1] = int(param[0] + "1")
                continue

            # Increase/Decrease Shift if found
            if re.match("^x[+-]$", param):
                shift[0] = int(param[1] + "1")
                continue
            if re.match("^y[+-]$", param):
                shift[1] = int(param[1] + "1")
                continue

            #  Show help menu if -h called
            if param == "-h":
                return self.output_help()  # yes, I'm supremely lazy

            # Exit if exit code is entered
            if param == "--":
                return False

        # If scale values have changed call scale function
        if scale[0] != 0 or scale[1] != 0:
            self.scale_plotter(*scale)

        # If shift values have changed call shift function
        if shift[0] != 0 or shift[1] != 0:
            self.shift_plotter(*shift)

        return True

    def shift_plotter(self, x, y) -> None:
        """
        Increase the offset attribute of the plotter
        :param x: The x value to offset the plotter by
        :param y: The x value to offset the plotter by
        :returns: None
        """
        self.plotter.offset = [
            self.plotter.offset[0] + (x * self.plotter.origin[0]),
            self.plotter.offset[1] + (y * self.plotter.origin[1]),
        ]

        self.display_plotter()

        print(f"Plotter shift => X: {self.plotter.offset[0]}, Y: {self.plotter.offset[1]}")
        print(f"X-Axis: moved {self.plotter.offset[0] / self.plotter.scale[0]:.2f} units away from centre")
        print(f"Y-Axis: moved {self.plotter.offset[1] / self.plotter.scale[1]:.2f} units away from centre")

    def scale_plotter(self, x: int, y: int):
        """
        Increase the scale attribute of the plotter
        :param x: How x should be modified => [+1 -> +, 0 -> None, -1 -> -]
        :param y: How x should be modified => [+1 -> +, 0 -> None, -1 -> -]
        :returns: None
        """

        self.scale = [self.scale[0] + x, self.scale[1] + y]

        self.plotter.scale = [
            2 ** self.scale[0],
            2 ** self.scale[1],
        ]

        self.display_plotter()

        print(f"Plotter scale => {self.plotter.scale[0]}x -> {self.plotter.scale[1]}y")
        print(f"X-Axis: {self.plotter.scale[0]:.2f}, i.e 1x => {1 / self.plotter.scale[0]:.2f}, units")
        print(f"Y-Axis: {self.plotter.scale[1]:.2f}, i.e 1y => {1 / self.plotter.scale[1]:.2f}, units")

    def display_plotter(self):
        self.plotter.restore()
        self.plotter.borders()
        self.plotter.plotSimpleFunction(self.f)
        self.plotter.display()


if __name__ == "__main__":
    application = Controller(43, eqn_trig)
