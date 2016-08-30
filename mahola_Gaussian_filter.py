import numpy as np
import pylab as plt
import mahotas as mh
img = mh.imread('./resources/Man.png')
imgnew = mh.gaussian_filter(img,5);
plt.imshow(imgnew)
plt.gray()
plt.show()
