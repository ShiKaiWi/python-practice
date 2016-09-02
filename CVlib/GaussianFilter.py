import numpy as np
import pylab as plt
import mahotas as mh

class GaussianFilter:
    def __init__(self,img,sigma = 1,windsize = 3):
        self.img = mh.imread(img)
        self.M,self.N = self.img.shape
        self.windsize = windsize 
        self.sigma = sigma
        self.gaussian_kernel = self.kernel()
        self.halfsize = self.windsize // 2

    def convolution(self,window):
        size = self.gaussian_kernel.size
        if size != window.size:
            return None
        return np.sum(self.gaussian_kernel * window)

    def kernel(self):
        N = self.windsize // 2
        x = np.linspace(-N,N,2*N+1)
        y = np.linspace(-N,N,2*N+1)
        xv,yv = np.meshgrid(x,y,indexing='xy')
        H = np.exp(-(np.square(xv)+np.square(yv))/(2*self.sigma*self.sigma))
        H = H / H.sum()
        return np.reshape(H,(self.windsize*self.windsize,1))

    def filter(self):
        imgnew = np.zeros((self.M,self.N))
        w = self.halfsize
        for i in range(0,self.M):
            for j in range(0,self.N):
                if i<w or j<w or i>self.M-1-w or j>self.N-1-w:
                    imgnew[i][j] = self.img[i][j]
                    continue
                imgnew[i][j]= self.convolution(np.reshape(self.img[i-w:i+1+w,j-w:j+1+w],(self.windsize*self.windsize,1)))
        return imgnew        

    def demo(self):
        plt.imshow(self.filter())
        plt.gray()
        plt.show()

