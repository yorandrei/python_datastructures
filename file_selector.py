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
# DONE: fix run from entry field
# DONE: Add hot key combo to entry to display loaded file Ctrl+Return
# TODO: Starting position in sliders is viewed as zero.  Need to allow reducing it
# DONE: Also image scale needs to indicate real position, accounting for skipped rows
# TODO: Add subframes with bazel around entries in options
# TODO: Reduce width of skip fields
# TODO: Add aspect ratio input
# DONE: Add a checkbox for saving out png
# DONE: add current open file label
# DONE: Add entry field for skip header / footer
# TODO: Keep focus on entry or switch focus to display when file is selected
# DONE: fix display file name
# DONE: finish open_file check if file is valid 
# TODO: package gui
# TODO: add check if packages are installed and install them
# TODO: Explore if it's better to display inside gui or outside
# DONE: Adjust window size

    def display(self, event):
        h = self.header_skip.get()
        f = self.footer_skip.get()
        s = self.save_output.get()
        graph = Graph(self.input_file_name.get(), h, f, s)

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
        
        # Update current file name
        self.cur_file_name.set(self.file_path.split('/')[-1])

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

        self.cur_file_name.set(file_name.split('/')[-1])
        self.input_file_name.set(file_name)
        self.content_text.delete(1.0, END)
        with open(file_name) as _file:
            self.content_text.insert(1.0, _file.read())
        self.display(event)

    # Options display will show currently selected file, save png checkbox 
    # and header / footer skip fields
    def setup_options_display(self):
        frame = Frame(root)
        frame.pack(anchor='w', fill='x', padx=5, pady=2)

        # Current file
        Label(frame, text='File Selected').pack(side=LEFT, padx=3, pady=5)
        self.cur_file_name = StringVar()
        self.cur_file_field = Entry(frame, textvariable=self.cur_file_name) 
        self.cur_file_field.pack(side=LEFT)

        # Save output image file
        self.save_output = BooleanVar()
        check = Checkbutton(frame, text='Save Output Image')
        check.pack(side=LEFT, padx=3, pady=5) #varialble=save_output

        # Skip header
        Label(frame, text='Header Skip Lines').pack(side=LEFT, padx=3, pady=5)
        self.header_skip = IntVar()
        self.header_field = Entry(frame, textvariable=self.header_skip, width=5)
        self.header_field.pack(side=LEFT)
        self.header_skip.set(1)

        # Skip footer
        Label(frame, text='Footer Skip Lines').pack(side=LEFT, padx=3, pady=5)
        self.footer_skip = IntVar()
        self.footer_field = Entry(frame, textvariable=self.footer_skip, width=5)
        self.footer_field.pack(side=LEFT)
        self.footer_skip.set(1)

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
        self.browse_button.bind("<Control-Return>", self.display)
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
        self.setup_options_display()
        self.setup_text()


class Graph:

    def __init__(self, filename='data/fpga_in_20.csv', 
                    head=1, tail=0, save=0):
        self.filename = filename 
        skiph = head 
        skipf = tail 
        self.save = save
        self.ratio = 0.26
        self.outfilename = self.filename.split('.')[0] + '.png'

        data = genfromtxt(self.filename, 
                            delimiter=',', 
                            skip_header=skiph, 
                            skip_footer=skipf,
                            dtype=np.int16)

        # These numbers will be used for correct scale display
        top_sample = skiph - 1
        bottom_sample = top_sample + data.shape[0] - 1

        minVal = data.min()
        maxVal = data.max()
        byte_array = np.round(255.0 * (data - minVal) /
                            (maxVal - minVal - 1.0)).astype(np.uint8)
        if save:
            imageio.imsave(self.outfilename, byte_array)

        fig, self.ax = plt.subplots(figsize=(5, 9))
        im = self.ax.imshow(data, 
            aspect=self.ratio, 
            extent=[0, 128, bottom_sample, top_sample]) 
            #, cmap='gray')
            
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
        # Scales
        top_sample = skiph - 1
        bottom_sample = top_sample + data.shape[0] - 1

        minVal = data.min()
        maxVal = data.max()
        byte_array = np.round(255.0 * (data - minVal) /
                            (maxVal - minVal - 1.0)).astype(np.uint8)
        if self.save:
            imageio.imsave(self.outfilename, byte_array)
        im = self.ax.imshow(data, 
            aspect=self.ratio, 
            extent=[0, 128, bottom_sample, top_sample]) 
            #, cmap='gray')
        plt.subplots_adjust(bottom=0.25)


if __name__ == '__main__':
    root = Tk()
    Inspector(root)
    root.mainloop()