import numpy as np
import pylab as plt
import mahotas as mh

def Convolution(kernel,source):
    size = kernel.size
    if size != source.size:
        return None
    result = 0
    for i in range(0,size):
        result += kernel[i]*source[size-i-1]
    return result

def kernel(sigma,size):
    N = size // 2
    x = np.linspace(-N,N,2*N+1)
    y = np.linspace(-N,N,2*N+1)
    xv,yv = np.meshgrid(x,y,indexing='xy')
    H = np.exp(-(np.square(xv)+np.square(yv))/(2*sigma*sigma))
    H = H / H.sum()
    return H

img = mh.imread('./resources/Man.png')
M,N = img.shape
# imgnew = mh.gaussian_filter(img,2);
sigma = 3
W = 17
Kernel = kernel(sigma,W)
w = W // 2
Kernel = np.reshape(Kernel,(W*W,1))
imgnew = np.zeros((M,N))
for i in range(0,M):
    for j in range(0,N):
        if i<w or j<w or i>M-1-w or j>N-1-w:
            imgnew[i][j] = img[i][j]
            continue
        # print(imgnew[i][j])
        # print(img[i][j])
        # print('\n')
        imgnew[i][j]=Convolution(Kernel,np.reshape(img[i-w:i+1+w,j-w:j+1+w],(W*W,1)))

plt.imshow(imgnew)
plt.gray()
plt.show()
