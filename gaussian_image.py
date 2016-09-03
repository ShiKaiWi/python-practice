import pylab as plt
import numpy as np
N = 15
x = np.linspace(-N,N,2*N+1)
y = np.linspace(-N,N,2*N+1)
xv,yv = np.meshgrid(x,y,indexing='xy')
H = np.exp(-(np.square(xv)+np.square(yv))/2)
H = H * 255.0 
plt.imshow(H)
plt.gray()
plt.show()
