from tkinter import *
from ClientSideDoorSensor import *

# Mock data status of door states
status_dct = {'coleman': 'NULL', 'bush': 'NULL', 'schaper': 'NULL', 'mota': 'NULL'}

coleman = status_dct['coleman']
bush = status_dct['bush']
schaper = status_dct['schaper']
mota = status_dct['mota']

door_states = [coleman, bush, schaper, mota]

coleman_text = "Dr. Coleman's door is:\n" + coleman
bush_text = "Dr. Bush's door is:\n" + bush
schaper_text = "Dr. Schaper's door is:\n" + schaper
mota_text = "Dr. Mota's door is:\n" + mota

# Mock data color of door states
top_left_color = "orange"
top_right_color = "orange"
bottom_left_color = "orange"
bottom_right_color = "orange"

door_color = [top_left_color, top_right_color, bottom_left_color, bottom_right_color]


class DoorDisplay:
    def __init__(self, master):
        self.master = master
        top_frame = Frame(master)
        bottom_frame = Frame(master)
        border_x_frame = Frame(master, bg="black", width=2, height=2)
        border_y1_frame = Frame(top_frame, bg="black", width=2, height=2)
        border_y2_frame = Frame(bottom_frame, bg="black", width=2, height=2)

        # Pack frames onto display
        top_frame.pack(side=TOP, fill=BOTH, expand=True)
        bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
        border_x_frame.pack(fill=BOTH, expand=False)

        # Setup labels with text, background color, and width
        self.top_left = Label(top_frame, text=coleman_text, bg=top_left_color, width=20)
        self.top_right = Label(top_frame, text=bush_text, bg=top_right_color, width=20)
        self.bottom_left = Label(bottom_frame, text=schaper_text, bg=bottom_left_color, width=20)
        self.bottom_right = Label(bottom_frame, text=mota_text, bg=bottom_right_color, width=20)

        # Set text font and size
        self.top_left.config(font=("Courier", 45))
        self.top_right.config(font=("Courier", 45))
        self.bottom_left.config(font=("Courier", 45))
        self.bottom_right.config(font=("Courier", 45))

        # Pack labels and frames onto display
        self.top_left.pack(side=LEFT, fill=BOTH, expand=True)
        border_y1_frame.pack(side=LEFT, fill=BOTH, expand=False)
        self.top_right.pack(side=RIGHT, fill=BOTH, expand=True)
        self.bottom_left.pack(side=LEFT, fill=BOTH, expand=True)
        border_y2_frame.pack(side=LEFT, fill=BOTH, expand=False)
        self.bottom_right.pack(side=RIGHT, fill=BOTH, expand=True)

        # Initiate update method calls
        self.update()

    def update(self):
        # Changes label text to new global assigned variables
        self.top_left['text'] = "Dr. Coleman's door is:\n" + coleman
        self.top_right['text'] = "Dr. Bush's door is:\n" + bush
        self.bottom_left['text'] = "Dr. Schaper's door is:\n" + schaper
        self.bottom_right['text'] = "Dr. Mota's door is:\n" + mota

        # Changes label background color to new global assigned color
        self.top_left['bg'] = top_left_color
        self.top_right['bg'] = top_right_color
        self.bottom_left['bg'] = bottom_left_color
        self.bottom_right['bg'] = bottom_right_color

        # Repeatedly calls itself every 5000 milliseconds to update display
        root.after(5000, self.update)


def data_change(root):
    # Receives global variables
    global coleman, bush, schaper, mota, top_left_color, top_right_color, bottom_left_color, bottom_right_color

    # Mock door status from flask server and update global door status values

    door_status = {}
    infile = open('mock_status.txt', 'r')
    for line in infile:
        line = line.strip()
        professor, doorState = line.split(',')
        door_status[professor] = doorState
    infile.close()

    coleman = door_status['coleman']
    bush = door_status['bush']
    schaper = door_status['schaper']
    mota = door_status['mota']

    # For loop to update colors after changing door status states
    doors = [coleman, bush, schaper, mota]
    door_position = [top_left_color, top_right_color, bottom_left_color, bottom_right_color]
    for i in range(0, len(doors)):
        if doors[i] == "CLOSED":
            door_position[i] = "red"
        elif doors[i] == "OPEN":
            door_position[i] = "green"
        else:
            door_position[i] = "orange"

    # Assigns new string color values to global variables to be called in update method
    top_left_color = door_position[0]
    top_right_color = door_position[1]
    bottom_left_color = door_position[2]
    bottom_right_color = door_position[3]

    root.after(4500, data_change, root)


# Initializes display, sets to full-screen mode
root = Tk()
root.attributes("-fullscreen", True)
app = DoorDisplay(root)
data_change(root)
root.mainloop()
