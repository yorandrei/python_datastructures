from tkinter import *

PROGRAM_NAME = ' File Inspector '

class Inspector:
    def __init__(self, root):
        self.root = root
        self.root.geometry('350x350')
        self.root.title(PROGRAM_NAME)
        self.init_gui()

# The gui displays a file selector, data preview, a display button
# the echo display field and its controls can go into gui as well
# at a later stage.

# Initially the text field will display the list of files in current directory
# When user selects the file to read it is previewed in text field instead.
# When user clicks "display data" the plt displays it
    def open_file(self):
        pass
        #input_file_name =  

    def init_gui(self):
        self.content_text = Text(root, wrap='none')

if __name__ == '__main__':
    root = Tk()
    Inspector(root)
    root.mainloop()