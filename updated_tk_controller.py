import tkinter as tk
import threading
import JoyLocal  # Importing the JoyLocal module to interact with the CAN bus

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Wheelchair Controller")
        self.geometry("300x200")

        self.x_value = tk.IntVar(value=0)
        self.y_value = tk.IntVar(value=0)

        self.create_widgets()

    def create_widgets(self):
        self.x_label = tk.Label(self, text="X Value:")
        self.x_label.pack()
        self.x_display = tk.Label(self, textvariable=self.x_value)
        self.x_display.pack()

        self.x_up_button = tk.Button(self, text="X Up", command=self.x_up)
        self.x_up_button.pack()
        self.x_down_button = tk.Button(self, text="X Down", command=self.x_down)
        self.x_down_button.pack()

        self.y_label = tk.Label(self, text="Y Value:")
        self.y_label.pack()
        self.y_display = tk.Label(self, textvariable=self.y_value)
        self.y_display.pack()

        self.y_up_button = tk.Button(self, text="Y Up", command=self.y_up)
        self.y_up_button.pack()
        self.y_down_button = tk.Button(self, text="Y Down", command=self.y_down)
        self.y_down_button.pack()

        self.send_button = tk.Button(self, text="Send to CAN bus", command=self.send_to_can)
        self.send_button.pack()

    def x_up(self):
        self.x_value.set(self.x_value.get() + 1)

    def x_down(self):
        self.x_value.set(self.x_value.get() - 1)

    def y_up(self):
        self.y_value.set(self.y_value.get() + 1)

    def y_down(self):
        self.y_value.set(self.y_value.get() - 1)

    
    def send_to_can(self):
        x = self.x_value.get()
        y = self.y_value.get()
        # Create an instance of the X360 class and update the joystick values
        x360_controller = JoyLocal.X360()
        x360_controller.update_joystick_values(x, y)

        x = self.x_value.get()
        y = self.y_value.get()
        # Assuming send_joystick_canframe takes x and y values as arguments
        JoyLocal.send_joystick_canframe(x, y)

# Create and run the GUI in a separate thread
gui_thread = threading.Thread(target=lambda: GUI().mainloop())
gui_thread.start()
