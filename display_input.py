import imageio
import matplotlib.pyplot as plt 
import numpy as np
from numpy import genfromtxt

data = genfromtxt('fpga_in_43.csv', 
                    delimiter=',', 
                    skip_header=450, 
                    skip_footer=400,
                    dtype=np.int16)
minVal = data.min()
maxVal = data.max()
byte_array = np.round(255.0 * (data - minVal) /
                    (maxVal - minVal - 1.0)).astype(np.uint8)
imageio.imsave('echos.png', byte_array)
img = imageio.imread('echos.png')
fig, ax = plt.subplots(figsize=(20, 60))
#fig, ax = plt.subplots()
im = ax.imshow(img)#, cmap='gray')
plt.tight_layout()

plt.show()
