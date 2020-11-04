from tkinter import *
from .door_status import ClientSideDoorStatus


class DoorDisplay:
    def __init__(self, root):
        self.root = root
        self.sensor = ClientSideDoorStatus()
        self.current_status = self.sensor.door_status # Starts with 'NULL' values
        self.colors = {var: 'orange' for var in self.sensor.doors}

        top_frame = Frame(self.root)
        bottom_frame = Frame(self.root)

        # Pack frames onto display
        top_frame.pack(side=TOP, fill=BOTH, expand=True)
        bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        # Setup labels with initial text, background color, and width
        texts = [f"Dr. {name.capitalize()}'s door is:\nNULL" for name in self.sensor.doors]
        colors = [self.colors[door] for door in self.sensor.doors]
        self.top_left = Label(top_frame, text=texts[0], bg=colors[0], width=20, borderwidth=1, relief=SOLID)
        self.top_right = Label(top_frame, text=texts[1], bg=colors[1], width=20, borderwidth=1, relief=SOLID)
        self.bottom_left = Label(bottom_frame, text=texts[2], bg=colors[2], width=20, borderwidth=1, relief=SOLID)
        self.bottom_right = Label(bottom_frame, text=texts[3], bg=colors[3], width=20, borderwidth=1, relief=SOLID)

        # Set text font and size
        self.top_left.config(font=("Courier", 45))
        self.top_right.config(font=("Courier", 45))
        self.bottom_left.config(font=("Courier", 45))
        self.bottom_right.config(font=("Courier", 45))

        # Pack labels and frames onto display
        self.top_left.pack(side=LEFT, fill=BOTH, expand=True)
        self.top_right.pack(side=RIGHT, fill=BOTH, expand=True)
        self.bottom_left.pack(side=LEFT, fill=BOTH, expand=True)
        self.bottom_right.pack(side=RIGHT, fill=BOTH, expand=True)

        # Initiate update method calls
        self.update()

    def update(self):
        # Update label text to current values
        texts = [(door.capitalize(), self.current_status[door]) for door in self.sensor.doors]
        strings = [f"Dr. {texts[i][0]}'s door is:\n{texts[i][1]}" for i in range(4)]
        self.top_left['text'] = strings[0]
        self.top_right['text'] = strings[1]
        self.bottom_left['text'] = strings[2]
        self.bottom_right['text'] = strings[3]

        # Update label background color to match current status
        colors = [self.colors[door] for door in self.sensor.doors]
        self.top_left['bg'] = colors[0]
        self.top_right['bg'] = colors[1]
        self.bottom_left['bg'] = colors[2]
        self.bottom_right['bg'] = colors[3]

        # Repeatedly calls itself every 5000 milliseconds to update display
        self.root.after(5000, self.update)


    def data_change(self):
        # Query door status from flask server and update door status values
        self.current_status = self.sensor.running_status()

        # For loop to update colors after changing door status states
        for door in self.sensor.doors:
            if self.current_status[door] == "CLOSED":
                self.colors[door] = "red"
            elif self.current_status[door] == "OPEN":
                self.colors[door] = "green"
            else:
                self.colors[door] = "orange"
        self.root.after(4500, self.data_change, root)


if __name__ == "__main__":
    # Initializes display, sets to full-screen mode
    root = Tk()
    root.attributes("-fullscreen", True)
    root.config(cursor="none")
    app = DoorDisplay(root)
    app.data_change()
    root.mainloop()
