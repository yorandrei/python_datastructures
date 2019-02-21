import imageio
import matplotlib.pyplot as plt 
import numpy as np
from numpy import genfromtxt
from matplotlib.widgets import Slider

# TODO: add file selection gui
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
        plt.title(self.filename.split('/')[1])
        plt.tight_layout()

        # Add sliders 
        plt.subplots_adjust(bottom=0.25)
        axcolor = 'lightgoldenrodyellow'
        axstart = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        axstop = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

        self.slstart = Slider(axstart, "Skip Top", skiph, 700, valinit=0, valstep=1)
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
    graph = Graph('data/fpga_in_20.csv', 150, 200)
