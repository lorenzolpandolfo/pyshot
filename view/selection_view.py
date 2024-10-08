import tkinter as tk

class SelectionView:
    def __init__(self, root, selection_area, take_screenshot_callback):
        self.root = root
        self.canvas = tk.Canvas(root, cursor="cross", bg="gray", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.selection_area = selection_area
        self.take_screnshoot_callback = take_screenshot_callback

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        root.bind("<Escape>", self.finish)

    def on_mouse_down(self, event):
        self.selection_area.set_start(event.x, event.y)

    def on_mouse_drag(self, event):
        self.selection_area.set_end(event.x, event.y)
        self.canvas.delete("rect")
        self.canvas.create_rectangle(self.selection_area.x_start, self.selection_area.y_start, event.x, event.y, outline='red', width=2, tag="rect")

    def on_mouse_release(self, event):
        self.selection_area.set_end(event.x, event.y)
        self.root.attributes('-alpha', 0)
        self.take_screnshoot_callback()
        self.finish()

    def finish(self, e=None):
        self.root.destroy()
