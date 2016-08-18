import numpy as np
import pylab
import mahotas as mh

img = mh.imread('./resources/dna.jpeg')
M,N = img.shape
max = img.max()
total = M*N
histogram = np.zeros(max+1,int)
transform = np.zeros(max+1)
for i in range(0,M):
    for j in range(0,N):
        histogram[img[i][j]] += 1
for i in range(0,max+1):
    transform[i] = histogram[i] * 255 // total

for i in range(0,M):
    for j in range(0,N):
        img[i][j] = transform[img[i][j]]

pylab.imshow(img)
pylab.gray()
pylab.show()
    


