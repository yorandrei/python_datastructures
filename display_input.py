import imageio
import matplotlib.pyplot as plt 
import numpy as np
from numpy import genfromtxt
from matplotlib.widgets import Slider

filename = 'data/fpga_in_20.csv'
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
#imageio.imsave('data/echos.png', byte_array)
fig, ax = plt.subplots(figsize=(5, 9))
im = ax.imshow(data)#, cmap='gray')
plt.title(filename.split('/')[1])
#plt.pcolor(vmin=minVal, vmax=maxVal)
#plt.colorbar(im)
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
    im = ax.imshow(data)#, cmap='gray')
    plt.subplots_adjust(bottom=0.25)


slstart.on_changed(update)
slstop.on_changed(update)


plt.show()
