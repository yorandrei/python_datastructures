from tkinter import *
from tkinter import filedialog
import os

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
# TODO: Display directory contents in textbox on boot
# TODO: Explore if it's better to display inside gui or outside

    def display(self, event):
        print("Calling Display")

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
        #self.content_text.insert(1.0, contents)
        for f in contents:
            self.content_text.insert(END, f)
            self.content_text.insert(END, '\n')

    def open_file(self, event):
        file_name = self.input_file_name.get()
        if not file_name:
            # TODO: Change into a pop-up window
            print("Please specify file name")
        # Check if file opens
        cwd = os.getcwd()
        infile = os.listdir()
        print(infile)
        #elif
        #else:
        #    print("File exists")


    def setup_fileselect(self):
        top_frame = Frame(root)
        top_frame.pack(anchor='w', fill='x', padx=5, pady=2)
        #top_frame.pack(anchor='w', fill='x', expand='yes')

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


if __name__ == '__main__':
    root = Tk()
    Inspector(root)
    root.mainloop()