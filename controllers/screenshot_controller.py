from PIL import ImageGrab
from utils.clipboard_util import image_to_clipboard
from utils.coordinates import normalize_coordinates


class ScreenshotController:
    def __init__(self, selection_area):
        self.selection_area = selection_area

    def take_screenshot(self):
        x_start, y_start, x_end, y_end = self.selection_area.get_area()
        x_start, y_start, x_end, y_end = normalize_coordinates(x_start, y_start, x_end, y_end)

        screenshot = ImageGrab.grab(bbox=(x_start, y_start, x_end, y_end))
        image_to_clipboard(screenshot)
