MARGIN = 2

class SelectionArea:
    def __init__(self, dpi_scale):
        self.dpi_scale = dpi_scale

        self.x_start = 0
        self.y_start = 0
        self.x_end = 0
        self.y_end = 0

    def set_start(self, x, y):
        self.x_start = x + self.dpi_scale + MARGIN
        self.y_start = y + self.dpi_scale + MARGIN

    def set_end(self, x, y):
        self.x_end = x + self.dpi_scale - MARGIN
        self.y_end = y + self.dpi_scale - MARGIN

    def get_area(self):
        return self.x_start, self.y_start, self.x_end, self.y_end
