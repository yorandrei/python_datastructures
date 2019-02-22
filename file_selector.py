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

'''
# The gui displays a file selector, data preview, a display button
# the echo display field and its controls can go into gui as well
# at a later stage.

# Initially the text field will display the list of files in current directory
# When user selects the file to read it is previewed in text field instead.
# When user clicks "Display" the plt displays it
'''
# TODO: Starting position in sliders is viewed as zero.  Need to allow reducing it
# TODO: Keep focus on entry or switch focus to display when file is selected
# TODO: package gui
# TODO: add check if packages are installed and install them
# TODO: Explore if it's better to display inside gui or outside
# TODO: Remove import * and import only what's needed
# TODO: Refactor Graph class to eliminate duplication
# TODO: Clean up names for variables to make sure that they make sense

    def display(self, event):
        h = self.header_skip.get()
        f = self.footer_skip.get()
        s = self.save_output.get()
        ae = self.aspect_ratio_enable.get()
        ar = self.aspect_ratio_val.get()
        graph = Graph(self.input_file_name.get(), h, f, s, ae, ar)

    def open(self, event):
        ftypes = [('CSV Files)', '*.csv'), 
                ('Excel Fiels', '*.xlsx'),
                ('Images', '*.png'),
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
        frame.pack(anchor='w', fill='x', padx=5)
        xpad = 3
        ypad = 3

        # Current file
        lf1 = LabelFrame(frame, text='File Selected', padx=xpad, pady=ypad)
        lf1.pack(side=LEFT, padx=xpad, pady=ypad)
        self.cur_file_name = StringVar()
        cur_file_field = Entry(lf1, textvariable=self.cur_file_name) 
        cur_file_field.pack(side=LEFT)

        # Save output image file
        lf4 = LabelFrame(frame, text='Save Output Image', padx=xpad)
        lf4.pack(side=LEFT, padx=xpad)
        self.save_output = IntVar()
        check = Checkbutton(lf4, variable=self.save_output)
        check.pack(side=LEFT, padx=xpad) #varialble=save_output
        self.save_output.set(0)

        # Skip header
        lf2 = LabelFrame(frame, text='Header Skip Lines', padx=xpad, pady=ypad)
        lf2.pack(side=LEFT, padx=xpad, pady=ypad)
        self.header_skip = IntVar()
        header_field = Entry(lf2, textvariable=self.header_skip, width=5)
        header_field.pack(side=LEFT)
        self.header_skip.set(1)

        # Skip footer
        lf3 = LabelFrame(frame, text='Footer Skip Lines', padx=xpad, pady=ypad)
        lf3.pack(side=LEFT, padx=xpad, pady=ypad)
        self.footer_skip = IntVar()
        footer_field = Entry(lf3, textvariable=self.footer_skip, width=5)
        footer_field.pack(side=LEFT)
        self.footer_skip.set(1)

        # Set aspect ratio 
        lf5 = LabelFrame(frame, text='Set Aspect Ratio', padx=xpad)
        lf5.pack(side=LEFT, padx=xpad)
        self.aspect_ratio_enable = IntVar() 
        check2 = Checkbutton(lf5, variable=self.aspect_ratio_enable)
        check2.pack(side=LEFT, padx=xpad)
        self.aspect_ratio_enable.set(1)

        self.aspect_ratio_val = DoubleVar()
        asp_ratio = Entry(lf5, textvariable=self.aspect_ratio_val, width=8)
        asp_ratio.pack(side=LEFT)
        self.aspect_ratio_val.set(0.26)


    def setup_fileselect(self):
        top_frame = Frame(root)
        top_frame.pack(anchor='w', fill='x', padx=5, pady=2)

        Label(top_frame, text='Select Input File').pack(side=LEFT, padx=3, pady=5)

        self.input_file_name = StringVar()
        file_name_field = Entry(top_frame, textvariable=self.input_file_name)
        file_name_field.pack(side=LEFT, fill='x', expand='yes')
        file_name_field.bind("<Return>", self.open_file)

        photo = PhotoImage(file="resources/arrow_icon.png")
        browse_button = Label(top_frame, image=photo)
        browse_button.image = photo
        browse_button.config(image=photo, width="20", height="20")
        browse_button.bind("<Button-1>", self.open)
        browse_button.bind("<Return>", self.open)
        browse_button.bind("<Control-Return>", self.display)
        browse_button.pack(side=LEFT, anchor='w')

        open_button = Button(top_frame, text='Display')
        open_button.pack(side=RIGHT, padx=3, pady=5)
        open_button.bind("<Button-1>", self.display)
        open_button.bind("<Return>", self.display)



    def setup_text(self):
        self.content_text = Text(root, wrap='none')
        self.content_text.pack(expand='yes', fill='both')

        yscroll_bar = Scrollbar(self.content_text)
        self.content_text.configure(yscrollcommand=yscroll_bar.set)
        yscroll_bar.config(command=self.content_text.yview)
        yscroll_bar.pack(side='right', fill='y')

        xscroll_bar = Scrollbar(self.content_text, orient=HORIZONTAL)
        self.content_text.configure(xscrollcommand=xscroll_bar.set)
        xscroll_bar.config(command=self.content_text.xview)
        xscroll_bar.pack(side='bottom', fill='x')

        self.show_contents()

    def init_gui(self):
        self.setup_fileselect()
        self.setup_options_display()
        self.setup_text()


class Graph:

    def __init__(self, filename='data/fpga_in_20.csv', 
                    head=1, tail=0, save=0, ar_en=0, ar_val=0.26):
        self.filename = filename 
        skiph = head 
        skipf = tail 
        self.save = save
        self.ratio_enable = ar_en
        self.ratio = ar_val 
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

        if self.ratio_enable:
            im = self.ax.imshow(data, 
                aspect=self.ratio, 
                extent=[0, 128, bottom_sample, top_sample]) 
        else:
            im = self.ax.imshow(data, 
                extent=[0, 128, bottom_sample, top_sample]) 
            
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
#        im = self.ax.imshow(data, 
#            aspect=self.ratio, 
#            extent=[0, 128, bottom_sample, top_sample]) 
        if self.ratio_enable:
            im = self.ax.imshow(data, 
                aspect=self.ratio, 
                extent=[0, 128, bottom_sample, top_sample]) 
        else:
            im = self.ax.imshow(data, 
                extent=[0, 128, bottom_sample, top_sample]) 
        plt.subplots_adjust(bottom=0.25)


if __name__ == '__main__':
    root = Tk()
    Inspector(root)
    root.mainloop()