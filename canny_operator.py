import numpy as np
import pylab as plt
import mahotas as mh

sobelx = np.array([-1.0,0,1,-2,0,2,-1,0,1])
sobely = np.array([-1.0,-2,-1,0,0,0,1,2,1])
sobelx = np.reshape(sobelx,(9,1))
sobely = np.reshape(sobely,(9,1))
threshold_H = 0
threshold_L = 0
def Convolution(kernel,source):
    size = kernel.size
    if size != source.size:
        return None
    return np.sum(kernel * source)

def kernel(sigma,size):
    N = size // 2
    x = np.linspace(-N,N,2*N+1)
    y = np.linspace(-N,N,2*N+1)
    xv,yv = np.meshgrid(x,y,indexing='xy')
    H = np.exp(-(np.square(xv)+np.square(yv))/(2*sigma*sigma))
    H = H / H.sum()
    return H

def Sobel(wind):
    global sobel
    x = np.sum(sobelx*wind[::-1])
    y = np.sum(sobely*wind[::-1])
    return np.sqrt(x*x+y*y)

def track(imgx,tx,ty):
    global threshold_H
    global threshold_L
    global  M,N
    global trackmatrix
    if tx>M-1 or ty>N-1 or tx<0 or ty<0:
        return
    if trackmatrix[tx][ty]:return
    if imgx[tx][ty] < threshold_L:
        return
    
    trackmatrix[tx][ty] = 255
    track(imgx,tx+1,ty)
    track(imgx,tx,ty+1)
img = mh.imread('./resources/Man.png')
M,N = img.shape
# imgsmooth = mh.gaussian_filter(img,2);
sigma = 1
W = 3
Kernel = kernel(sigma,W)
w = W // 2
imgmax = 0
Kernel = np.reshape(Kernel,(W*W,1))
imgsmooth = np.zeros((M,N))
imgsobel = np.zeros((M,N))
for i in range(0,M):
    for j in range(0,N):
        if i<w or j<w or i>M-1-w or j>N-1-w:
            imgsmooth[i][j] = img[i][j]
            continue
        # print(imgsmooth[i][j])
        # print(img[i][j])
        # print('\n')
        imgsmooth[i][j]=Convolution(Kernel,np.reshape(img[i-w:i+1+w,j-w:j+1+w],(W*W,1)))

# print(imgsmooth[23:26,89:92])
for i in range(0,M):
    for j in range(0,N):
        if i<1 or j<1 or i>M-2 or j>N-2:
            imgsobel[i][j] = 0
            continue
        imgsobel[i][j] = Sobel(np.reshape(imgsmooth[i-1:i+2,j-1:j+2],(9,1)))
        # print(imgsobel[i][j])
        imgmax = max(imgmax,imgsobel[i][j])

# normalization = 255 / imgmax
# imgsobel = imgsobel *normalization 
threshold_L = 29
threshold_H = imgmax - 500 
trackmatrix = np.zeros((M,N))
print(imgmax,threshold_H,threshold_L)
print('sobel operator done\n')

for i  in range(0,M):
    for j in range(0,N):
         # if i<200 and i>180:
         #     print(i,j,imgsobel[i][j])
        if trackmatrix[i][j]>0 or imgsobel[i][j]<threshold_H:continue
        track(imgsobel,i,j)
         
plt.imshow(trackmatrix)
plt.gray()
plt.show()
