#! C:\Python34\python.exe

# Imports
import os
import re
import sys
import json
import tkinter

# Configuration
#log_file_path = "C:/Users/" + os.getenv('username') + "/Documents/My Games/Binding of Isaac Rebirth/log.txt"
log_file_path = "C:/Users/" + os.getenv('username') + "/Documents/My Games/Binding of Isaac Afterbirth/log.txt"
progress_file_name = 'progress.txt'

# The Item1001Tracker class
class Item1001Tracker(tkinter.Frame):
    def __init__(self, parent):
        # Class variables
        self.file_array_position = 0
        self.items_remaining_list = []

        # Welcome message
        print('Starting 1001% item tracker...')

        # Get a sorted list of all item IDs
        with open('items.json', 'r') as items_file:
            items_json = json.load(items_file)
        all_item_ids = []
        for item_id, item_details in items_json.items():
            all_item_ids.append(item_id)
        all_item_ids.sort()

        # Initialize the photo dictionary
        self.photos = {}
        for item_id in all_item_ids:
            image_path = 'collectibles/collectibles_' + item_id + '.png'
            self.photos[item_id] = tkinter.PhotoImage(file=image_path)

        # Check for the existance of the progress file
        if os.path.isfile(progress_file_name):
            # Import the collected items
            with open(progress_file_name) as progress_file:
                for line in progress_file:
                    self.items_remaining_list.append(line.strip())
            print('Imported the "' + progress_file_name + '" file. ' + str(len(self.items_remaining_list)) + ' items remaining.')
        else:
            # Make a new list with every item
            all_item_ids = []
            for item_id, item_details in items_json.items():
                all_item_ids.append(item_id)
            all_item_ids.sort()
            self.items_remaining_list = all_item_ids
            f = open(progress_file_name,'w')
            file_contents = ''
            for item_id in all_item_ids:
                file_contents += str(item_id) + '\n'
            f.write(file_contents)
            f.close()
            print('Made a new "' + progress_file_name + '" file with ' + str(len(all_item_ids)) + ' entries.')


        # Initialize a new GUI window
        self.parent = parent
        self.window = tkinter.Toplevel(self.parent)
        self.window.title('1001% Tracker')  # Set the GUI title
        self.icon = tkinter.PhotoImage(file='collectibles/collectibles_076.png')
        self.window.tk.call('wm', 'iconphoto', self.window._w, self.icon)  # Set the GUI icon
        self.window.protocol('WM_DELETE_WINDOW', sys.exit)  # Close the main GUI when the window is closed
        self.left_label = tkinter.Label(self.window, font='font 20 bold')
        self.left_label.grid(row=0)
        self.canvas = tkinter.Canvas(self.window, width=500)
        self.canvas.grid(row=1)

        # Initialization
        self.drawUI()
        self.parseLog()

    def drawUI(self):
        items_remaining = str(len(self.items_remaining_list)) + ' items remaining.'
        self.left_label.configure(text=items_remaining)

        self.canvas.delete("all")

        draw_x = 32
        draw_y = 32
        for item_id in self.items_remaining_list:
            self.canvas.create_image((draw_x, draw_y), image=self.photos[item_id])

            draw_x += 48
            if draw_x == 32 + (48 * 10):
                draw_x = 32
                draw_y += 64

    def parseLog(self):
        # Read the log into a variable
        try:
            with open(log_file_path, 'r') as f:
                file_contents = f.read()
        except Exception:
            print("Failed to open the log file at \"" + log_file_path + "\".")
            sys.exit(1)

        # Convert it to an array
        file_array = file_contents.splitlines()

        # Return to the start if we go past the end of the file (which occurs when the log file is truncated)
        if self.file_array_position > len(file_array):
            self.file_array_position = 0

        # Process the log's new output
        for line in file_array[self.file_array_position:]:

            # Debug
            #print(line)

            # A new item was picked up
            if line.startswith('Adding collectible'):
                item_id = re.search(r'Adding collectible (\d+) ', line).group(1)
                item_id = item_id.zfill(3)

                # Remove it from the items array
                if item_id in self.items_remaining_list:
                    self.items_remaining_list.remove(item_id)
                    print("Removed item from list:", item_id)

                # Redraw the UI
                self.drawUI()

        # Set that we have read the log up to this point
        self.file_array_position = len(file_array)
        
        # Schedule another log parse in 0.25 seconds
        self.parent.after(250, self.parseLog)


# The main program
if __name__ == '__main__':
    # Initialize the root GUI
    root = tkinter.Tk()
    root.withdraw()  # Hide the GUI

    # Show the GUI
    Item1001Tracker(root)
    root.mainloop()
