import tkinter as tk
from models.area_selection import SelectionArea
from view.selection_view import SelectionView
from controllers.screenshot_controller import ScreenshotController
import platform
import ctypes


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.25)
        self.configure(background='black')

        self.__set_priority()

        self.dpi_scale = self.winfo_fpixels('1i') / 96

        selection_area = SelectionArea(self.dpi_scale)
        controller = ScreenshotController(selection_area)

        SelectionView(self, selection_area, controller.take_screenshot)

    def __set_priority(self):
        self.focus_force()
        self.lift()
        self.attributes('-topmost', True)


if __name__ == "__main__":
    from pynput import keyboard

    if platform.system() == "Windows":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)

    def on_press(key):
        if key == keyboard.Key.print_screen:
            app = MainApp()
            app.mainloop()

    def start_keyboard_listener():
        with keyboard.Listener(on_press= on_press) as listener:
            listener.join()

    start_keyboard_listener()
