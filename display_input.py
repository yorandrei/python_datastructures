import imageio
import matplotlib.pyplot as plt 
import numpy as np
from numpy import genfromtxt
from matplotlib.widgets import Slider

filename = 'data/fpga_in_43.csv'
skiph = 1
skipf = 0

data = genfromtxt(filename, 
                    delimiter=',', 
                    skip_header=skiph, 
                    skip_footer=skipf,
                    dtype=np.int16)
minVal = data.min()
maxVal = data.max()
byte_array = np.round(255.0 * (data - minVal) /
                    (maxVal - minVal - 1.0)).astype(np.uint8)
imageio.imsave('data/echos.png', byte_array)
img = imageio.imread('data/echos.png')
fig, ax = plt.subplots(figsize=(5, 9))
im = ax.imshow(img)#, cmap='gray')
plt.tight_layout()

# Add sliders 
plt.subplots_adjust(bottom=0.25)
axcolor = 'lightgoldenrodyellow'
axstart = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axstop = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

slstart = Slider(axstart, "Skip Top", skiph, 700, valinit=0, valstep=1)
slstop = Slider(axstop, "Skip Bottom", skipf, 700, valinit=0, valstep=1)

def update(val):
    skiph = int(slstart.val)
    skipf = int(slstop.val)
    data = genfromtxt(filename, 
                        delimiter=',', 
                        skip_header=skiph, 
                        skip_footer=skipf,
                        dtype=np.int16)
    minVal = data.min()
    maxVal = data.max()
    byte_array = np.round(255.0 * (data - minVal) /
                        (maxVal - minVal - 1.0)).astype(np.uint8)
    imageio.imsave('data/echos.png', byte_array)
    img = imageio.imread('data/echos.png')
    im = ax.imshow(img)#, cmap='gray')
    #fig.canvas.draw_idle()


slstart.on_changed(update)
slstop.on_changed(update)


plt.show()
