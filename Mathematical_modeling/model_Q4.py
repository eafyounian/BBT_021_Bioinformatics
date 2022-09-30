# import imageio
import os
import numpy as np
import matplotlib.pyplot as plt

# Name each cell type (index corresponds to cell type):
CELL_TYPES = ["Blue", "Red"]

# Set the cell division times for each cell type (index corresponds to cell type):
CELL_DIVISION_TIMES = [25, 50] 

# Set the initial number cells for each cell type (index corresponds to cell type):
NINITIAL = [5,10]

# Set plot markers for each cell type (index corresponds to cell type):
CELL_MARKERS = ["o", "."]




# You do not need to edit anything under this line. 

# You can make a gif using this commented-out section if imageio is imported. The last line in this file aslo needs to be uncommented. 
# def make_gif():
#     GIF_NAME = "animation.gif"
#     GIF_INTERVAL = 0.5
#     images = sorted(os.listdir("images"))
#     with imageio.get_writer(GIF_NAME, mode="I", duration=GIF_INTERVAL) as writer:
#         for filename in images:
#             image = imageio.imread(f"images/{filename}")
#             writer.append_data(image)


class Cell:
    
    def __init__(self, x_pos, y_pos, cell_type):
        self.x = x_pos
        self.y = y_pos
        self.cell_type = cell_type
        self.marker = self.determine_marker(cell_type)
        self.division_time = self.determine_division_time(cell_type)

    def move(self, x_new, y_new) -> None:
        self.x = x_new
        self.y = y_new

    def determine_marker(self, cell_type) -> str:
        return {c_type: marker for c_type, marker in zip(CELL_TYPES, CELL_MARKERS)}[cell_type]

    def determine_division_time(self, cell_type) -> int:
        return {c_type: division_time for c_type, division_time in zip(CELL_TYPES, CELL_DIVISION_TIMES)}[cell_type]

    def ready_to_divide(self, t) -> bool:
        if t % self.division_time != 0 or t==0:
            return False
        else:
            return True

    def __repr__(self):
        return f"Cell(Position:({self.x}, {self.y}), Type:{self.cell_type})"


class CellGrid:

    GRID_SIZE_X = 1000
    GRID_SIZE_Y = 1000
    T_MAX = 100
    JUMP_SIZE = 3
    DIVISION_DISTANCE = 1
    SAMPLING_FREQUENCY = 10

    def __init__(self, NINITIAL, cell_types):
        self.cell_types = cell_types
        self.cells = []
        for ninit, cell_type in zip(NINITIAL, cell_types):
            for _ in range(ninit):
                new_cell = Cell(np.random.randint(0, self.GRID_SIZE_X),
                                np.random.randint(0, self.GRID_SIZE_Y),
                                cell_type)
                self.cells.append(new_cell)

    def cells_by_type(self, cell_type):
        return [c for c in self.cells if c.cell_type==cell_type]

    def divide_cell(self, cell) -> None:
        x_new, y_new = (cell.x + self.DIVISION_DISTANCE * np.random.randint(-1, 2) ) % self.GRID_SIZE_X,\
                       (cell.y + self.DIVISION_DISTANCE * np.random.randint(-1, 2) ) % self.GRID_SIZE_Y
        new_cell = Cell(x_new, y_new, cell.cell_type)
        if self.allowed_coordinates(x_new, y_new):
            self.cells.append(new_cell)
        else:
            self.divide_cell(new_cell)

    def random_move(self, cell) -> None:
        x_new, y_new = (cell.x + self.JUMP_SIZE * np.random.randint(-1, 2) ) % self.GRID_SIZE_X,\
                       (cell.y + self.JUMP_SIZE * np.random.randint(-1, 2) ) % self.GRID_SIZE_Y
        if self.allowed_coordinates(x_new, y_new):
            cell.move(x_new, y_new)

    def evolve(self) -> None:
        for t in range(0, self.T_MAX + 1):
            iterating_cells = self.cells.copy()
            for cell in iterating_cells:
                self.random_move(cell)
                if cell.ready_to_divide(t):
                    self.divide_cell(cell)
            if t % self.SAMPLING_FREQUENCY == 0: 
                cell_numbers_message = ", \n".join([f"number of {c_type} cells={len(self.cells_by_type(c_type))}" for c_type in self.cell_types])
                title = f"time = {t} hours, \n{cell_numbers_message}" 
                self.plot(filename=f"plot_{t:04}.png", title=title)

    def allowed_coordinates(self, x, y) -> bool:
        for c in self.cells:
            if (c.x == x) and (c.y == y):
                return False
        else:
            return True
            
    def plot(self, filename=None, title=None) -> None:
        for c in self.cells:
            plt.plot(c.x, c.y, marker=c.marker, color=c.cell_type)
        plt.xticks([])
        plt.yticks([])
        plt.title(title)
        plt.tight_layout() 
        if filename is None:
            plt.show()
        else:
            if not os.path.isdir('image_output_Q4'): os.mkdir('image_output_Q4')
            plt.savefig(f"image_output_Q4/{filename}")
            plt.close()


if __name__ == "__main__":
    mygrid = CellGrid(NINITIAL, CELL_TYPES)
    mygrid.evolve()
    # If you want to make a gif, uncomment this line:
    # make_gif()
            
            