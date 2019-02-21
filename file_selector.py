from tkinter import *
from tkinter import filedialog
import os

import imageio
import matplotlib.pyplot as plt
import numpy as np 
from numpy import genfromtxt
from matplotlib.widgets import Slider
from tkinter import messagebox as mb

PROGRAM_NAME = ' File Inspector '

class Inspector:
    def __init__(self, root):
        self.root = root
        self.root.geometry('750x350')
        self.root.title(PROGRAM_NAME)
        self.init_gui()

# The gui displays a file selector, data preview, a display button
# the echo display field and its controls can go into gui as well
# at a later stage.

# Initially the text field will display the list of files in current directory
# When user selects the file to read it is previewed in text field instead.
# When user clicks "display data" the plt displays it
# TODO: fix run from entry field
# TODO: Add hot key combo to entry to display loaded file
# DONE: fix display file name
# DONE: finish open_file check if file is valid 
# TODO: add current open file label
# TODO: package gui
# TODO: add check if packages are installed and install them
# TODO: Explore if it's better to display inside gui or outside
# TODO: Add a checkbox for saving out png
# DONE: Adjust window size
# TODO: Add entry field for skip header / footer

    def display(self, event):
        graph = Graph(self.input_file_name.get(), 10, 100)

    def open(self, event):
        ftypes = [('CSV Files)', '*.csv'), 
                ('Excel Fiels', '*.xlsx'),
                ('All', '*')]
        self.file_path = filedialog.askopenfilename(defaultextension='.csv', 
                                            filetypes=ftypes)
        if not self.file_path:
            return
        self.input_file_name.set(self.file_path)

        self.content_text.delete(1.0, END)
        with open(self.file_path) as _file:
            self.content_text.insert(1.0, _file.read())

    def show_contents(self):
        cwd = os.getcwd()
        contents = os.listdir()
        self.input_file_name.set(cwd)

        self.content_text.delete(1.0, END)
        for f in contents:
            self.content_text.insert(END, f)
            self.content_text.insert(END, '\n')

    def open_file(self, event):
        file_name = self.input_file_name.get()
        if not file_name:
            mb.showerror(title="Missing File Name", 
                message="Please enter the name of the file you wish to open")
            return

        # Check if file opens
        if not os.path.isfile(file_name):
            mb.showerror(title="Error Opening File", 
                message="Could not open specified file: '%s'" % file_name)
            return

        print("File name passed.  Opening")
        self.input_file_name.set(file_name)
        self.content_text.delete(1.0, END)
        with open(file_name) as _file:
            self.content_text.insert(1.0, _file.read())
        #self.display()
        #cwd = os.getcwd()
        #infile = os.listdir()
        #elif
        #else:
        #    print("File exists")


    def setup_fileselect(self):
        top_frame = Frame(root)
        top_frame.pack(anchor='w', fill='x', padx=5, pady=2)

        Label(top_frame, text='Select Input File').pack(side=LEFT, padx=3, pady=5)
        self.input_file_name = StringVar()

        self.file_name_field = Entry(top_frame, textvariable=self.input_file_name)
        self.file_name_field.pack(side=LEFT, fill='x', expand='yes')
        self.file_name_field.bind("<Return>", self.open_file)

        photo = PhotoImage(file="resources/arrow_icon.png")
        self.browse_button = Label(top_frame, image=photo)
        self.browse_button.image = photo
        self.browse_button.config(image=photo, width="20", height="20")
        self.browse_button.bind("<Button-1>", self.open)
        self.browse_button.bind("<Return>", self.open)
        self.browse_button.pack(side=LEFT, anchor='w')

        self.open_button = Button(top_frame, text='Display')
        self.open_button.pack(side=RIGHT, padx=3, pady=5)
        self.open_button.bind("<Button-1>", self.display)
        self.open_button.bind("<Return>", self.display)



    def setup_text(self):
        self.content_text = Text(root, wrap='none')
        self.content_text.pack(expand='yes', fill='both')

        self.yscroll_bar = Scrollbar(self.content_text)
        self.content_text.configure(yscrollcommand=self.yscroll_bar.set)
        self.yscroll_bar.config(command=self.content_text.yview)
        self.yscroll_bar.pack(side='right', fill='y')

        self.xscroll_bar = Scrollbar(self.content_text, orient=HORIZONTAL)
        self.content_text.configure(xscrollcommand=self.xscroll_bar.set)
        self.xscroll_bar.config(command=self.content_text.xview)
        self.xscroll_bar.pack(side='bottom', fill='x')

        self.show_contents()

    def init_gui(self):
        self.setup_fileselect()
        self.setup_text()


class Graph:

    def __init__(self, filename='data/fpga_in_20.csv', 
                    head=1, tail=0):
        self.filename = filename 
        skiph = head 
        skipf = tail 
        self.outfilename = self.filename.split('.')[0] + '.png'

        data = genfromtxt(self.filename, 
                            delimiter=',', 
                            skip_header=skiph, 
                            skip_footer=skipf,
                            dtype=np.int16)
        minVal = data.min()
        maxVal = data.max()
        byte_array = np.round(255.0 * (data - minVal) /
                            (maxVal - minVal - 1.0)).astype(np.uint8)
        imageio.imsave(self.outfilename, byte_array)
        fig, self.ax = plt.subplots(figsize=(5, 9))
        im = self.ax.imshow(data)#, cmap='gray')
        plt.title(self.filename.split('/')[-1])
        plt.tight_layout()

        # Add sliders 
        plt.subplots_adjust(bottom=0.25)
        axcolor = 'lightgoldenrodyellow'
        axstart = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        axstop = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

        self.slstart = Slider(axstart, "Skip Top", skiph, 900, valinit=0, valstep=1)
        self.slstop = Slider(axstop, "Skip Bottom", skipf, 700, valinit=0, valstep=1)

        self.slstart.on_changed(self.update)
        self.slstop.on_changed(self.update)
        
        plt.show()

    def update(self, val):
        skiph = int(self.slstart.val)
        skipf = int(self.slstop.val)
        data = genfromtxt(self.filename, 
                            delimiter=',', 
                            skip_header=skiph, 
                            skip_footer=skipf,
                            dtype=np.int16)
        minVal = data.min()
        maxVal = data.max()
        byte_array = np.round(255.0 * (data - minVal) /
                            (maxVal - minVal - 1.0)).astype(np.uint8)
        imageio.imsave(self.outfilename, byte_array)
        im = self.ax.imshow(data)#, cmap='gray')
        plt.subplots_adjust(bottom=0.25)


if __name__ == '__main__':
    root = Tk()
    Inspector(root)
    root.mainloop()